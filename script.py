# import modules
from bs4 import BeautifulSoup as bs
import requests
import os
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
# from user_agent import random_header
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

# web driver configuration
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.headless = True
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
ua = UserAgent()
userAgent = ua.random
chrome_options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

def login_user(email, password):
    """
    Logins user to the websites
    """
    # set url
    url = 'https://giphy.com/login'

    # call open browser function
    driver.get(url)

    # login to website

    login = driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)
    password = driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    submit = driver.find_element(By.XPATH, '//button[text()="Log in"]').click()
    sleep(4)

    try:
        logout_button = driver.find_element(By.XPATH, '//a[text()="Log Out"]')
        print('Successfully logged in')
        driver.save_screenshot('login_screenshot.png')

    except Exception as e:
        print('Incorrect login/password')


def get_all_images():
    """
    Returns all image URLs on a favourites page
    """

    driver.get('https://giphy.com/favorites')
    sleep(4)
    driver.save_screenshot('favorites_screenshot.png')
    print('Downloading all images')
    gifs = driver.find_elements(By.XPATH, '//img[@class="giphy-gif-img giphy-img-loaded"]')
    sleep(1)

    giphys_list = []
    for s in range(len(gifs)):
        try:
            # removing all text after the ? in the image src link
            postion_question_mark = gifs[s].get_attribute('src').index("?") 
            giphys_list.append(gifs[s].get_attribute('src')[:postion_question_mark])
        except ValueError:
            pass    
    return giphys_list

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)

    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))



def main(email, password, path):
    """
    Main function to start scripts
    """
    try:
        login_user(email, password)
        images = get_all_images()
        for img in images:
            # for each image, download it and store to path
            download(img, path)
    except Exception as e:
        print(e)


email = "oluwaseyioyewunmi19@gmail.com"
password = "whatsapp19"
path = "giphy-images"
email = input('Enter your user email')
password = input('Enter your password')
path = input('Enter the name of the folder to store the downloaded images to')

main(email, password, path)