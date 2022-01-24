import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
#from CSV import CSV
from JSON import JSON
from Upload import NFT

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
    time.sleep(1)

    d.find_element_by_css_selector(".first-time-flow__terms").click()
    d.find_element_by_xpath('//button[text()="Import"]').click()


def move_to_opensea(d):
    d.execute_script(
        '''window.open("https://opensea.io/collection/guy-with-a-smirk/assets/create","_blank")''')
    d.switch_to.window(d.window_handles[2])
    time.sleep(6)


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


def fillMetadata(d, metadataMap: dict):
    d.find_element_by_xpath(
        '//div[@class="AssetFormTraitSection--side"]/button').click()
    for item in metadataMap:
        for key in item:
            input1 = d.find_element_by_xpath(
                '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
            input2 = d.find_element_by_xpath(
                '//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')

            input1.send_keys(str(key))
            input2.send_keys(str(item[key]))
            d.find_element_by_xpath('//button[text()="Add more"]').click()

    time.sleep(1)
    d.find_element_by_xpath('//button[text()="Save"]').click()


def upload(d, nft: NFT):
    d.switch_to.window(driver.window_handles[-1])
    time.sleep(3)
    d.find_element_by_id("media").send_keys(nft.file)
    d.find_element_by_id("name").send_keys(nft.name)
    d.find_element_by_id("description").send_keys(nft.description)

    time.sleep(3)

    fillMetadata(d, nft.metadata)

    time.sleep(2)
    d.find_element_by_xpath('//button[text()="Create"]').click()
    time.sleep(4)
    d.execute_script(
        '''location.href="https://opensea.io/collection/ether-swimmers/assets/create"''')


def checkForAlreadyUploaded(filename):
    with open('/OutputData/uploaded.csv', "r") as f:
        reader = csv.reader(f, skipinitialspace=False,
                            delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            for field in row:
                # print("Field" + field)
                if field == filename:
                    print("is in file")
                    return False
        f.close()
        return True


def addFileToComplete(filename):
    with open('OutputData/uploaded.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow([filename])
        csvfile.flush()
        csvfile.close()


if __name__ == '__main__':
    # setup metamask
    opt = webdriver.ChromeOptions()
    opt.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(
        executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
    setup_metamask_wallet(driver)
    time.sleep(2)
    move_to_opensea(driver)
    signin_to_opensea(driver)
    driver.execute_script(
        '''window.open("https://opensea.io/collection/ether-swimmers/assets/create","_blank")''')
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(7)  # todo- need to manually click on sign button for now
    file = JSON("OutputData/metadata.json").readFromFile()
    for data in file:
        for key in data:
            if (checkForAlreadyUploaded(data[key]['file'])):
                name = data[key]['name']
                description = data[key]['description']
                filename = data[key]['file']
                metadata = data[key]['attributes']
                upload(driver, NFT(name, description, metadata,
                                   os.getcwd() + "/data/" + filename))
                addFileToComplete(filename)

    print("DONE!!")
