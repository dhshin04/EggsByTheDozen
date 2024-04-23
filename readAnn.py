import json, csv

f = open("_annotations.createml.json", 'r')

data = json.load(f)

for item in data: 
    fileName = item["image"]
    with open('%s.txt' % fileName, 'w') as txt_file:
        for ann in item["annotations"]:
            coords = ann["coordinates"]
            txt_file.write(str(coords["x"]) + " " + str(coords["y"]) + " " + str(coords["width"]) + " " + str(coords["height"]) + "\n")

        