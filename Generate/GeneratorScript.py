import os
import pathlib
import random
from PIL import Image
import numpy as np
import csv
import sample_metadata as sample_metadata
import json


def main(id):

    # These are our dicts of the files in our Assets folder. Each file in those Assets subfolders should be renamed to a number eg. 1.png 2.png 3.png etc
    # Then in the dictionary create a list of the items + their attribute names. This is then added to the image metadata for uploading.

    backgroundDictionary = {
        1: 'Blue',
        2: 'Bright Red'
    }

    bodyDictionary = {
        1: 'Yellow Banana'
    }

    bodyTwoDictionary = {
    }

    eyesDictionary = {
        1: 'Glasses',
        2: 'Shades'
    }

    mouthDictionary = {
        1: 'Gold Tooth',
        2: 'Mouth'
    }

    # In this dict, 0 is empty, this can be used to create NFTs that don't have a particular attribute.
    # Just make sure you wrap an if statement around the image in the image copy and paste further down this script.
    accessoriesDictionary = {
        0: '',
        1: 'Gold Crown',
        2: 'Sword',
        3: 'Cowboy Hat'
    }

    ASSETFOLDER = "Assets/"
    OutputFolder = "OutputData/"
    OriginalFolder = "OutputData/Images/Original/"
    ResizedFolder = "OutputData/Images/Resized/"
    # This will be used for your file name when being saved & the name of the NFT during upload.
    ImageFileName = "Banana"
    # This IDCSV keeps track of the combination of asset strings, it is then checked during generation to prevent any NFT's being created which are duplicate.
    IDCSV = "Generate/GenerationIDs.csv"
    tokenid = id
    previousToken = id-1
    strTokenId = str(tokenid)
    print("Token Id"+strTokenId)
    strPreviousToken = str(previousToken)

    # This creates a JSON file object for the image which is used a lot during upload.
    def generate_meta_data():
        metadata = sample_metadata.metadata_template
        metadata_file_name = (
            "Metadata/" + ImageFileName + strTokenId + ".json")
        metadata[strPreviousToken]["name"] = ImageFileName + "#" + strTokenId
        metadata[strPreviousToken
                 ]["description"] = "A handsome Banana NFT"
        metadata[strPreviousToken]["file"] = ImageFileName + \
            strTokenId + ".png"
        metadata[strPreviousToken]["attributes"] = []
        metadata[strPreviousToken]["attributes"].append(
            {
                'Background': backgroundDictionary[background],
                'Body': bodyDictionary[body],
                'Eyes': eyesDictionary[eyes],
                'Mouth': mouthDictionary[mouth],
                'Accessory': accessoriesDictionary[accessory]
            })
        keys = list(metadata.keys())
        for key in keys:
            new_key = key.replace(strPreviousToken, strTokenId)
            if new_key != key:
                metadata[new_key] = metadata[key]
                del metadata[key]
        with open(metadata_file_name, "w") as file:
            json.dump(metadata, file)

    # This section lists out the options in our dicts then we use random.choices to weight the rarity of a particular NFT attribute.
    # Make sure the number of items matches the number specified in the dictionaries above.
    backgroundList = [1, 2]

    bodyList = [1]

    eyesList = [1, 2]

    mouthList = [1, 2]

    accessoryList = [0, 1, 2, 3]

    #bodyTwoList = []

    # Probabilities - Lower number = lower usage
    # Ensure there is a probability for each asset in each dict.
    backgroundProbabilities = [1, 1]

    bodyProbabilities = [1]

    eyesProbabilities = [1, 1]

    mouthProbabilities = [1, 1]

    accessoryProbabilities = [
        1, 1, 1, 1]

    background = random.choices(backgroundList, backgroundProbabilities)
    background2 = random.choices(backgroundList, backgroundProbabilities)
    body = random.choices(bodyList, bodyProbabilities)
    eyes = random.choices(eyesList, eyesProbabilities)
    mouth = random.choices(mouthList, mouthProbabilities)
    accessory = random.choices(accessoryList, accessoryProbabilities)
    #bodyTwo = random.choices(bodyTwoList, bodyProbabilities)

    background = background[0]
    background2 = background2[0]
    body = body[0]
    eyes = eyes[0]
    mouth = mouth[0]
    accessory = accessory[0]
    #bodyTwo = bodyTwo[0]

    # Add your attributes to this list to generate the unique ID.
    attirubutesList = [background, body, eyes, mouth, accessory]
    listString = ''.join(str(e) for e in attirubutesList)
    with open(IDCSV, "r") as f:
        reader = csv.reader(f, skipinitialspace=False,
                            delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            for field in row:
                if field == listString:
                    print(listString + "has already been generated")
                    main(tokenid)
                    return
    f.close()

    with open(IDCSV, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        writer.writerow([listString])
        csvfile.flush()
        csvfile.close()

    generate_meta_data()

    # Open Required pngs (Background, Body, Eyes etc) in respective folders
    baseBG = Image.open(ASSETFOLDER + "Background/" +
                        str(background) + ".png")
    imgBody = Image.open(ASSETFOLDER + "Body/" + str(body) + ".png")
    imgEyes = Image.open(ASSETFOLDER + "Eyes/" + str(eyes) + ".png")
    imgMouth = Image.open(ASSETFOLDER + "Mouth/" + str(mouth) + ".png")
    if accessory > 0:
        imgAccessories = Image.open(
            ASSETFOLDER + "Accessories/" + str(accessory) + ".png")

    # Paste/Merge Required PNGs, as layers on base. Paste in order of how you want the layers. Last paste will be top layer.
    baseBG.paste(imgBody, (0, 0), imgBody)
    baseBG.paste(imgEyes, (0, 0), imgEyes)
    baseBG.paste(imgMouth, (0, 0), imgMouth)
    # This check allows you to ensure that there is an accessory present. Use this for rarity.
    if accessory > 0:
        baseBG.paste(imgAccessories, (0, 0), imgAccessories)

    # This saves a single PNG. Don't use when creating GIFs.
    resized_img = baseBG.save(OriginalFolder + ImageFileName + "_" +
                              str(tokenid) + '.png', 'png', quality=95)

    # Open assets for a second frame - use this for GIFs only. Duplicate for more frames.
    # frameTwoBG = Image.open(ASSETFOLDER + "Background/" +
    #                       str(background2) + ".png")
    # frameTwoImgBody = Image.open(
    #    ASSETFOLDER + "BodyTwo/" + str(bodyTwo) + ".png")
    #frameTwoImgEyes = (ASSETFOLDER + "Eyes/" + str(eyes) + ".png")
    #frameTwoImgMouth = (ASSETFOLDER + "Mouth/" + str(mouth) + ".png")

    # Create Gif frame two. Duplicate for more frames.
    #frameTwoBG.paste(frameTwoImgBody, (0, 0), frameTwoImgBody)
    #frameTwoBG.paste(frameTwoImgEyes, (0, 0), frameTwoImgEyes)
    #frameTwoBG.paste(frameTwoImgMouth, (0, 0), frameTwoImgMouth)
    # You could even reuse elements if you wanted them to be the same between frames as below.
    # if accessory > 0:
    #frameTwoBG.paste(imgAccessories, (0, 0), imgAccessories)

    # This creates a GIF of your two (or more) images
    # resized_img = baseBG.save(OriginalFolder + ImageFileName + "_" + str(tokenid) + '.gif',
    # save_all=True, append_images=[frameTwoBG], duration=800, loop=0)

    # Resize to OpenSea recommended size. Change file extension from .png to .gif for gif resizing.
    resized_img = baseBG.resize((300, 300), resample=Image.NEAREST)
    resized_img.save(ResizedFolder + ImageFileName +
                     '_' + str(tokenid) + '.png', "PNG")
