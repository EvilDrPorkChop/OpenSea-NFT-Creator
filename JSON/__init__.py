import json
import os


class JSON:

    def __init__(self, filename):
        self.filename = filename

    def readFromFile(self):
        return json.load(open(file=self.filename))


if __name__ == '__main__':
    file = JSON("OutputData/metadata.json")

    file = file.readFromFile()
    for data in file:
        for key in data:
            name = data[key]['name']
            description = data[key]['description']
            file = data[key]['name'] + ".png"
            metadata = data[key]['attributes']
            print(name, description, file, metadata)
