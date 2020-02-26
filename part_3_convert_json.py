import cc_dat_utils
import json
from cc_classes import *

# Part 3
# Load your custom JSON file
# Convert JSON data to CCLevelPack
# Save converted data to DAT file

def make_CCLevelPack_data_from_json(jsonData):
    newLevelPack = CCLevelPack()
    levels = jsonData["levels"]
    for level in levels:
        newLevel = CCLevel()
        levelNum = level["levelNumber"]
        chipNum = level["chipNumber"]
        levelTime = level["time"]
        optFields = []

        for field in level["optionalFields"]:
            newCCField = make_CCField_from_data(field)
            optFields.append(newCCField)

        newLevel.level_number = levelNum
        newLevel.num_chips = chipNum
        newLevel.time = levelTime
        newLevel.optional_fields = optFields
        newLevel.upper_layer = level["upperLayer"]

        newLevelPack.add_level(newLevel)

    return newLevelPack

# Fuctions like a switch-case
def make_CCField_from_data(fieldData):
    newField = ""
    if fieldData["fieldType"] == "levelTitle":
        newField = CCMapTitleField(fieldData["value"])
    elif fieldData["fieldType"] == "encodedPassword":
        newField = CCEncodedPasswordField(fieldData["value"])
    elif fieldData["fieldType"] == "hintText":
        newField = CCMapHintField(fieldData["value"])
    elif fieldData["fieldType"] == "movingObjectsPos":
        monsters = []
        for monster in fieldData["value"]:
            monsters.append(CCCoordinate(monster["x"], monster["y"]))

        newField = CCMonsterMovementField(monsters)

    return newField

# Global
input_file = "data/level_data.json"

with open(input_file,"r") as reader:
    levelData_json = json.load(reader)

levelPack = make_CCLevelPack_data_from_json(levelData_json)


datFile_name = "data/level_data.dat"
cc_dat_utils.write_cc_level_pack_to_dat(levelPack, datFile_name)