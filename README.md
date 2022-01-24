# OpenSea PNG/GIF NFT Creator

## Description
A collection of python scripts which help you programatically create PNGs or GIFs and their Metadata in bulk with custom rarity rates, upload them to OpenSea & list them for sale. <br>

In /Generate/ is the generator script for programmatically creating images.

In /Upload/ there is an uploader script that logs into your OpenSea account via Selenium and metamask chrome plugin to bulk upload NFT to your collection. This part of the collection was customised from https://github.com/lakshyabatman/Bulk-uploader-NFT <br>

Inside /List/ there are a set of scripts to help you grab all your collection links and metadata information so that you can then set a price in Eth within the AssetLinks.csv and list them for sale. This was quite a tricky issue to solve as there is no bulk sell feature in OpenSea but this does automate the listing process.

Whilst this is an easy, hands-off way of uploading/listing your NFTs it takes time and isn't as efficient as having API access. I might update some of the functionality to use OpenSea's API in the future but for now you may want to run the upload process over night when you don't need your machine.

I've created a few example assets/images for the purpose of demoing this project. Feel free to do what you like with them.

You can check out the OpenSea NFT collection I made with this project here: https://opensea.io/collection/ether-swimmers/


### <b> If this proves useful to you or you get NFT rich consider buying me a coffee: </b>
<a href="https://www.buymeacoffee.com/tomhar" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

# Before you get started

## Accounts
- Get a metamask wallet and the Chrome extension.
- Sign up to OpenSea using a metamask wallet.

## Install Requirements

- `pip install -r requirements.txt`
- Make sure you have chrome driver installed.
- Create `.env` from `.example.env` with required keys.

## Create your PNG assets

- Create your assets and put them in folders within the /Assets/ folders. 
- Recommended image size is 300x300 but there is code to resize images automatically.
- Rename your assets to numbers such as 1.png, 2.png, 3.png etc and put them in the right folders. This makes it easier to work with a dictionary to generate metadata.

# Generating your NFTs

## Configure the Generator Script
- Follow the comments in the script.
- Setup your dictionarys of asset information for NFT metadata.
- Configure the image output for PNG/GIF.

## Start generating
- Open Execute.py and change the NumberOfNFTS.
- Run the script.
- The generator script will put strings of numbers into a GenerationIDs csv this is used to stop duplicate NFTs. If you need to rerun the generator from scratch, make sure to clear the IDs so that you aren't limited.
- There will be a metadata JSON file for each image. These will need to be joined by running the MergeJson.py file in the /JSON/ folder. (This could probably be fixed to do automatically at the point of generation).
- All your images should now be in OutputData/Images.

# Uploading to OpenSea

## Using UploadNFTs.py

### Setup your .env file

- EXTENSION_PATH: In our program, we're running a selenium based browser (chrome driver here) and usually in automated environment we don't have access to extensions, so get the access.
   - Navigate to chrome://extensions/
Click ‘Pack extension’ and enter the local path to the Metamask extension. This will generate a .crx file. Also, make a note of Extension ID.
   - Now the path to this '.crx' file is the value of this field.
- RECOVERY_CODE: Recovery code of your wallet cause we need to login into your metamask.
- PASSWORD: Metamask's password.
- CHROME_DRIVER_PATH: To run chromium, you need to download the chrome driver and it's path will be the value. (https://chromedriver.chromium.org/downloads)

### Note on metamask automation:
- You have to click the "sign" button during user login on opensea for the first time.
- Sometimes metamask wants additional "sign" auth on actions which when unattended can stop the scripts.
- If it fails at any point just rerun, the code is designed to keep track of what has already been uploaded/listed and skip that.
- You may find that when OpenSea's servers slow down (which happens a lot) this can affect Selenium's timings and cause errors as it tries to click things that don't exist. I've accounted for a fair bit of this behaviour but it doesn't account for every situation.

### Setup your OpenSea Collection
- You will need to input your OpenSea collection URL on line 98 & 134 of UploadNFTs.py. Create your OpenSea collection in your account and grab the link.

### Run UploadNFTs.py


# Listing for sale on OpenSea
This is long winded but worth it.
## Run the scripts in the List folder in this order:

### getUrls.py
- Change the collection URL on line 74
- This gets all (most) the URLs of the NFTs from the collection 
- This takes a while as it has to scroll through the page to overcome the infinite loader. The more images you have, the longer it'll take.
- <b>Important!</b> - After you've run this do a Remove Duplicates operation in the CSV to get rid of any URLs which are duplicated.

### getProperties.py
- This gets all the Metadata attributes & their % rarity for the NFT URLs and throws them into AssetLinks.csv.

## Important - Price your NFTs
-  Inside AssetLinks.csv add prices to your NFTs in Ethereum before runing

### Run list.py
- This should just run

Phew, you are done and now have a collection of shiny NFTs on OpenSea! Congrats