import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
#from CSV import CSV
#from JSON import JSON

EXTENSION_PATH = config("EXTENSION_PATH")
CHROME_DRIVER_PATH = ChromeDriverManager().install()

# This will need customising based on your attributes and their order.
dict = {
    'Background': 1,
    'Body': 2,
    'Eyes': 3,
    'Mouth': 4,
    'Accessory': 5
}


def getAttributes(driver):
    df = pd.read_csv('OutputData/AssetLinks.csv', header=0)
    for index, row in df.iterrows():
        driver.get(row.URL)
        attributes = driver.find_elements_by_class_name('Property--type')
        value = driver.find_elements_by_class_name('Property--value')
        rarity = driver.find_elements_by_class_name('Property--rarity')
        # i is the index for where to start writing the attributes, this should always be 1.
        i = 1
        for a in value:
            toWrite = (a.get_attribute('innerHTML'))
            df.iloc[index, i] = toWrite
            i = i+1
            df.to_csv(
                'OutputData/AssetLinks.csv', index=False)
        # j is the index for where to start writing the rarity. This should be changed based on the number of attributes your NFT has.
        j = 6
        for a in rarity:
            toWrite = (a.get_attribute('innerHTML'))
            df.iloc[index, j] = toWrite
            j = j+1
            df.to_csv(
                'OutputData/AssetLinks.csv', index=False)


opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
# opt.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
getAttributes(driver)
