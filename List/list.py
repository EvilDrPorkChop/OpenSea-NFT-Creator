from selenium.webdriver.common.action_chains import ActionChains
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decouple import config
from webdriver_manager.chrome import ChromeDriverManager

import time

EXTENSION_PATH = config("EXTENSION_PATH")

RECOVERY_CODE = config("RECOVERY_CODE")

PASSWORD = config("PASSWORD")

CHROME_DRIVER_PATH = ChromeDriverManager().install()


def setup_metamask_wallet(d):
    d.switch_to.window(d.window_handles[0])  # focus on metamask tab
    time.sleep(5)
    d.find_element(By.XPATH, '//button[text()="Get Started"]').click()

    time.sleep(1)
    d.find_element_by_xpath('//button[text()="Import wallet"]').click()
    time.sleep(1)

    d.find_element_by_xpath('//button[text()="No Thanks"]').click()
    time.sleep(1)

    inputs = d.find_elements_by_xpath("//input")
    inputs[0].send_keys(RECOVERY_CODE)
    time.sleep(1)
    inputs[1].send_keys(PASSWORD)
    inputs[2].send_keys(PASSWORD)
    time.sleep(2)

    d.find_element_by_css_selector(".first-time-flow__terms").click()
    d.find_element_by_xpath('//button[text()="Import"]').click()


def move_to_opensea(d):
    d.execute_script(
        '''window.open("https://opensea.io/collection/guy-with-a-smirk/assets/create","_blank")''')
    d.switch_to.window(d.window_handles[2])
    time.sleep(5)


def signin_to_opensea(d):
    d.find_element_by_xpath('//span[text()="MetaMask"]').click()
    time.sleep(4)
    d.switch_to.window(d.window_handles[2])
    d.find_element_by_xpath('//span[text()="MetaMask"]').click()
    time.sleep(4)
    d.switch_to.window(d.window_handles[-1])
    d.find_element_by_xpath('//button[text()="Next"]').click()
    time.sleep(4)
    d.find_element_by_xpath('//button[text()="Connect"]').click()
    d.switch_to.window(d.window_handles[2])


def listNFT(driver, df):
    listedMessage = 'Listed'
    for index, row in df.iterrows():
        status = pd.isnull(df['Status'].iloc[index])
        print(status)
        if status is True:
            price = (row.Price)
            driver.get(row.URL + '/sell')
            driver.switch_to.window(driver.window_handles[2])
            time.sleep(1)
            actions = ActionChains(driver)
            actions.send_keys(str(price))
            actions.perform()
            time.sleep(1)
            driver.find_element_by_xpath(
                '//button[text()="Complete listing"]').click()
            time.sleep(3)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="Sign"]')))
            except:
                print("A listing failed, you'll need to restart")
            driver.find_element_by_xpath(
                '//button[text()="Sign"]').click()
            time.sleep(3)
            driver.switch_to.window(driver.window_handles[-1])
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[text()="Sign"]')))
            except:
                print("A listing failed, you'll need to restart")
            driver.find_element_by_xpath('//button[text()="Sign"]').click()
            driver.switch_to.window(driver.window_handles[2])
            time.sleep(10)
            df.loc[index, 'Status'] = listedMessage
            df.to_csv(
                'OutputData/AssetLinks.csv', index=False)
    print("Completed")


df = pd.read_csv('OutputData/AssetLinks.csv', header=0)
opt = webdriver.ChromeOptions()
opt.add_extension(EXTENSION_PATH)
driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
setup_metamask_wallet(driver)
time.sleep(4)
move_to_opensea(driver)
signin_to_opensea(driver)
print("Complete")
listNFT(driver, df)
