from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import save_img
import pathlib
from os import path
import os
import random

newpath = f"{str(pathlib.Path().absolute())}\\"
folder_path = path.join(newpath, 'images\\')
if str(folder_path) == "C:\images\\":
    print("sorry i'm a stupid computer")
    quit()
if not path.exists(folder_path):
    os.makedirs(folder_path)
try:
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(options = options)

    driver.get('https://www.flickr.com/search/?tags=graffiti+chile')
    time.sleep(1)
except Exception as e:
    print("Error loading search results page" + str(e))
try:
    code = 0
    id_num = 0
    elems = driver.find_elements(By.XPATH, "//div[@class='photo-list-photo-container']/img")
    print(len(elems))
    for elem in elems:
        link = elem.get_attribute('src')
        new_link = link[0:len(link)-6] + "_z.jpg"
        print(link)
        print(new_link)
        print(type(link))
        try:
            img_name = f"{str(folder_path)}img_{id_num}.jpg"
            code = save_img(new_link, img_name)
        except Exception as e:
            print(f"Exception in saving image {id_num}: {str(e)}")
        if code >= 400:
            time.sleep(random.uniform(0.1, 1))
            continue
        id_num+=1
        time.sleep(random.uniform(0.1, 1))
        
    # for elem in elems:
    #     elem.click()
    #     time.sleep(1)
    time.sleep(5)
except Exception as e:
    print(f"Exception: {str(e)}")