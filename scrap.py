from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from utils import save_img, create_dict
import pathlib
from os import path
import os
import random
import pandas as pd

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

    driver.get('https://www.flickr.com/search/?tags=graffiti+chile&content_types=0')
    time.sleep(1)
    
except Exception as e:
    print("Error loading search results page" + str(e))

src_list = []
num = 6    
code = 0
id_num = 0
data_dict = create_dict(num)
driver.execute_script("window.scrollTo(0, 0);") #Go to top of page
SCROLL_PAUSE_TIME = 2 #How long to wait between scrolls
while True:
    previous_scrollY = driver.execute_script('return window.scrollY')
    #driver.execute_script('window.scrollBy( 0, 400 )' ) #Alternative scroll, a bit slower but reliable
    html = driver.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN) #Faster scroll, inelegant but works (Could translate to value scroll like above)
    time.sleep(SCROLL_PAUSE_TIME) #Give images a bit of time to load by waiting

    # Calculate new scroll height and compare with last scroll height
    if previous_scrollY == driver.execute_script('return window.scrollY'):
        try:    
            elems = driver.find_elements(By.XPATH, "//div[@class='photo-list-photo-container']/img")
            for elem in elems:
                link = elem.get_attribute('src')
                new_link = link[0:len(link)-6] + "_z.jpg"
                if new_link not in src_list:
                    src_list.append(new_link)
            print(len(elems))
        except Exception as e:  
            print(f"Exception: {str(e)}")
            
        try:
            button = driver.find_element(By.XPATH, "//div[@class='infinite-scroll-load-more']/button")
            button.click()
        except Exception as e:
            print(f"No loading button: {str(e)}")
            driver.quit()
            break

print(len(src_list))    
for new_link in src_list:
    print(new_link)
    img_name = ""
    try:
        img_name = f"{str(folder_path)}img_{id_num}.jpg"
        code = save_img(new_link, img_name)
        
    except Exception as e: 
        print(f"Exception in saving image {id_num}: {str(e)}")
        
    if code >= 400:
        time.sleep(random.uniform(0.1, 1))
        continue
    data_dict['link_to_img'].append(new_link)
    data_dict["img_name"].append(img_name)
    id_num+=1
    time.sleep(random.uniform(0.1, 1))
    
time.sleep(5)

data_pd_df = pd.DataFrame.from_dict(data_dict)
data_pd_df.to_csv(str(path.join(newpath, 'links_and_file_names.csv')), index = False)