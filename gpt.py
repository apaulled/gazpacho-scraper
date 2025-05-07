from openai import OpenAI
import requests
import json
from images import get_first_google_image_link
import yaml

with open('conf.yaml') as file:
    conf = yaml.safe_load(file)
    email = conf['backend-email']
    password = conf['backend-password']
    openai_key = conf['openai-key']

login_response = requests.post(
    'http://localhost:8080/users/login',
    json={
        'email': email,
        'password': password
    }
)
token = login_response.json()['accessToken']

search_response = requests.get(
    'http://localhost:8080/recipes/search?q=&type=name',
    headers={'Authorization': f'Bearer {token}'}
)

names = [recipe['name'] for recipe in search_response.json()]
name_string = ', '.join(names)

example_recipe = """
                 {
                    "name": "Pasta Carbonara",
                    "steps": [
                        "Boil pasta in salted water until al dente",
                        "Fry pancetta until crispy",
                        "Beat eggs and mix with grated Parmesan cheese",
                        "Drain pasta and quickly mix with pancetta and egg mixture",
                        "Season with freshly ground black pepper"
                    ],
                    "ingredients": [
                        {
                            "name": "Pasta",
                            "allergens": []
                        },
                        {
                            "name": "Eggs",
                            "allergens": [
                                "Eggs"
                            ]
                        },
                        {
                            "name": "Pancetta",
                            "allergens": []
                        },
                        {
                            "name": "Parmesan Cheese",
                            "allergens": []
                        },
                        {
                            "name": "Black Pepper",
                            "allergens": []
                        },
                        {
                            "name": "Salt",
                            "allergens": []
                        }
                    ],
                    "description": "A classic Italian pasta dish with a creamy sauce and crispy pancetta."
                 }
                 """

prompt = f"""
          I know the following recipes already: {name_string}.
          Give me 10 more recipes that are not included in this list. 
          You must format these recipes in JSON according to this example:
          {example_recipe}
          As such, there must be a list of recipe objects. 
          These recipe objects must contain the following:
          - a name
          - steps (a list of strings explaining how to make the recipe)
          - a description
          - a list of ingredients, where each ingredient is itself an object with a name and a list of allergens (strings)
          You must give me exactly 10 new recipes in this format, and you must not repeat any recipes I already know. There will be dire consequences.
          """

print('Prompt:')
print(prompt, end='\n\n')

client = OpenAI(api_key=openai_key)

response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)

text = response.output_text

print('Response:')
print(text, end='\n\n')

start_index = text.find('[')
end_index = text.rfind(']') + 1
json_string = text[start_index:end_index]

try:
    recipes = json.loads(json_string)
    print('Successfully Extracted JSON from Response')

    for recipe in recipes:
        try:
            recipe['image'] = get_first_google_image_link(recipe['name'])
        except Exception as e:
            print(f'Error fetching image: {e}')

    with open('recipe_holder.json', 'w') as file:
        file.write(json.dumps(recipes, indent=4))

    put_response = requests.put(
        'http://localhost:8080/recipes/batch',
        headers={'Authorization': f'Bearer {token}'},
        json=recipes
    )

    print('Successfully')
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"Error making web request to backend: {e}")
