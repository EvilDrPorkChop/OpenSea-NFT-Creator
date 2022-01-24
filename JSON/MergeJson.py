import json
import os
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(
    "Metadata") if isfile(join("Metadata/", f))]
files = [os.listdir("Metadata/")]

for i in onlyfiles:
    print(i)


def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open("Metadata/" + f1, 'r') as infile:
            result.append(json.load(infile))

    with open('OutputData/metadata.json', 'w') as output_file:
        json.dump(result, output_file)


merge_JsonFiles(onlyfiles)
