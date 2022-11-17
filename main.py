from PIL import Image
import requests
import time
import os
import json

def get_data(id_range, img_dir, json_dir):
    size = (256, 256)
    for id in id_range :
        drifter_url = f"https://omniscient.fringedrifters.com/main/images/{id}.jpeg"
        octo_1 = requests.get(drifter_url, stream=True).raw
        im = Image.open(octo_1).convert('RGBA')
        im.thumbnail(size)
        im.save(f'{img_dir}/{id}.png')
        time.sleep(1)

        drifter_json_url = f"https://omniscient.fringedrifters.com/main/metadata/{id}.json"
        drifter_json = requests.get(drifter_json_url).text
        with open(f'{json_dir}/{id}.json', "w") as f:
            f.write(drifter_json)
        time.sleep(2)

def get_by_trait(trait_name, trait_value, directory):
    matched_list = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath) as obj:
                drifter = json.load(obj)
                attributes = drifter.get('attributes')
                for attribute in attributes:
                    if attribute.get('trait_type') == trait_name and attribute.get('value') == trait_value:
                        matched_list.append([drifter.get("name"), trait_name, trait_value])
    return matched_list

def write_old_specials(in_directory, out_file):
    with open(out_file, "w") as f:
            f.write("")

    legendaries = get_by_trait("Looks Rare", "Legendary", in_directory)
    for drifter in legendaries:
        id = drifter[0][9:]
        line = f'{id},"{drifter[2]}"\n'
        with open(out_file, "a") as f:
            f.write(line)

    blues = get_by_trait("Location", "The Blue", in_directory)
    for drifter in blues:
        id = drifter[0][9:]
        line = f'{id},"{drifter[2]}"\n'
        with open(out_file, "a") as f:
            f.write(line)

#get_data(range(1498,1503),"img_void","json_void")
#get_data(range(1510,1520),"img","json")
#write_old_specials("json_void", "rare_void.csv")

forsale_ids = [1645]
get_data(forsale_ids,"img_forsale","json_forsale")

mine_ids = [1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973]
get_data(forsale_ids,"img_mine","json_mine")