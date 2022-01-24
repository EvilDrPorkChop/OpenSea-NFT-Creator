import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.common.exceptions import StaleElementReferenceException
#from CSV import CSV
#from JSON import JSON

EXTENSION_PATH = config("EXTENSION_PATH")
CHROME_DRIVER_PATH = ChromeDriverManager().install()
links = []
assetsString = "/assets/"


def addLinkToFile(href):
    if assetsString in str(href):
        with open('OutputData/AssetLinks.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow([str(href)])
            csvfile.flush()
            csvfile.close()


def getLinks(driver):
    elements = driver.find_elements_by_tag_name('a')
    if elements is not None:
        for elem in elements:
            try:
                href = elem.get_attribute("href")
                links.append(href)
                addLinkToFile(href)
            except StaleElementReferenceException as e:
                pass


def scrollToBottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_height = 800
    new_height = driver.execute_script(
        "return document.body.scrollHeight")
    current_height_str = "'" + str(new_height) + "'"
    print(current_height_str)

    while True:
        while current_height < new_height:
            driver.execute_script(
                "window.scrollTo(0, arguments[0]);", current_height)
            time.sleep(2)
            getLinks(driver)
            current_height = current_height + 300
            print(current_height)
            print(new_height)
            if current_height == new_height:
                break
        new_height = driver.execute_script(
            "return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = driver.execute_script(
            "return document.body.scrollHeight")


opt = webdriver.ChromeOptions()
opt.add_argument("--start-maximized")
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
driver.get("https://opensea.io/collection/ether-swimmers")
time.sleep(5)
scrollToBottom(driver)
time.sleep(5)
