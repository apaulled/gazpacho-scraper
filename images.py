from selenium import webdriver
from bs4 import BeautifulSoup


def get_first_google_image_link(query, headless=False, timeout=10):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f'https://www.google.com/search?q={query}&sca_esv=6f4cffb8fcc6cffb&sxsrf=AHTn8zr4BurUxfDSDr1TO7aNc1xT3jhcBA:1746546779584&source=hp&biw=620&bih=694&ei=WzAaaNfoIODg0PEPyr-0mQ8&iflsig=ACkRmUkAAAAAaBo-a6Ua8egjeemTldP08acFBuIz7kLj&ved=0ahUKEwiXgoPjmY-NAxVgMDQIHcofLfMQ4dUDCBc&uact=5&oq=puppies&gs_lp=EgNpbWciB3B1cHBpZXMyBxAjGCcYyQIyCBAAGIAEGLEDMggQABiABBixAzIFEAAYgAQyCBAAGIAEGLEDMgUQABiABDIIEAAYgAQYsQMyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQNI7BFQwwRY5hFwAXgAkAEAmAGWAaAB8wKqAQMzLjG4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ5gCBaACkwOoAgrCAgoQIxgnGMkCGOoCwgILEAAYgAQYsQMYgwHCAg4QABiABBixAxiDARiKBZgDD5IHAzQuMaAHlBmyBwMzLjG4B4QD&sclient=img&udm=2')

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        content = soup.find_all('div', class_='wIjY0d')[0]
        image = content.find_all('img')[0]
        return image['src']

    finally:
        driver.quit()


if __name__ == "__main__":
    link = get_first_google_image_link("puppies")
    print("First image URL:", link)
