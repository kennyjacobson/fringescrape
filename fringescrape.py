from PIL import Image
import requests
import time
import os
import json


class Fringescrape:
    """A class to facilitate scraping the fringe server, both the images and the metadata, and writing them to a csv file."""
    def __init__(self, location = "void") -> None:
        self.location = location
        self.fringe_project_img_dir = "https://omniscient.fringedrifters.com/main/images/"
        self.fringe_project_metadata_dir = "https://omniscient.fringedrifters.com/main/metadata/"
        self.json_dir = f"json_{location}"
        self.img_dir = f"img_{location}"
        self.mint_start, self.mint_end = self._get_location_params()
        self._check_dir()

    def _get_location_params(self):
        if self.location == 'scablands':
            return 1, 1509
        if self.location == 'void':
            return 1510, 3507
        if self.location == 'haze':
            return 3508, 6000
        if self.location == 'void_back':
            return 3486, 3508

    def _check_dir(self):
        if not os.path.exists(self.json_dir):
            print("no json dir. making it.")
            os.mkdir(self.json_dir)
        if not os.path.exists(self.img_dir):
            print("no img dir. making it.")
            os.mkdir(self.img_dir)
        
    def get_last_mint_number(self):
        drifter_numbers = sorted([int(filename.replace('.json', '')) for filename in os.listdir(self.json_dir)], reverse=True)
        if not drifter_numbers:
            return self.mint_start - 1
        else:
            return drifter_numbers[0]

    
    def scrape(self, process_img = True, process_json = True):
        """This is usually step 1, by default it gathers both the images and json metadata and saves it locally in two separate directories. This if for a give Fringe 'location'."""
        size = (256, 256)
        id_range = range(self.get_last_mint_number(), self.mint_end) 
        for id in id_range :
            try:
                if process_img:
                    drifter_url = f"{self.fringe_project_img_dir}{id}.jpeg"
                    octo_1 = requests.get(drifter_url, stream=True).raw
                    im = Image.open(octo_1).convert('RGBA')
                    im.thumbnail(size)
                    im.save(f'{self.img_dir}/{id}.png')
                    time.sleep(1)
            except Exception as exception:
                if type(exception).__name__ == 'UnidentifiedImageError':
                    print(f"{id} does not yet have an image. Done for now.")
                    break
                else:
                    raise Exception(type(exception).__name__)
                    
            if process_json:
                drifter_json_url = f"{self.fringe_project_metadata_dir}{id}.json"
                drifter_json = requests.get(drifter_json_url).text
                if "Soon you will arrive in the Fringe" in drifter_json:
                    print(f"{id} does not yet have real metadata. Done for now.")
                    break
                with open(f'{self.json_dir}/{id}.json', "w") as f:
                    f.write(drifter_json)
                time.sleep(2)

    def _get_traits(self):
        traits = []
        for filename in os.listdir(self.json_dir):
            filepath = os.path.join(self.json_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath) as obj:
                    drifter = json.load(obj)
                    attributes = drifter.get('attributes')
                    if attributes:
                        for attribute in attributes:
                            traits.append(attribute.get('trait_type'))
        traits.append("Death")
        return sorted([*set(traits)])

    def _get_all_attributes(self, traits):
        csv = []
        header = "id"
        for trait in traits:
            header = header + ',"' + trait  + '"'
        csv.append(header + '\n')
        for filename in os.listdir(self.json_dir):
            filepath = os.path.join(self.json_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath) as obj:
                    row = ""
                    drifter = json.load(obj)
                    name = drifter.get('name')
                    id = name[9:]
                    #print(id)
                    row = id
                    attributes = drifter.get('attributes')
                    #print(attributes)
                    
                    for trait in traits:
                        #print(trait)
                        found = False
                        for attribute in attributes:
                            
                            if attribute.get('trait_type') == trait:
                                #print(attribute.get('value'))
                                row = row + ',"' + attribute.get('value') + '"'
                                found = True
                        if not found:
                            row = row + ',"' + 'None' + '"'

                    csv.append(row + "\n")
        return csv

    
    def write_csv(self, cvs_path):
        """This is usually step 2 after the scrape. I takes all the drifters for a given Fringe 'location' and write their id and attributes to a csv file."""
        traits = self._get_traits()
        csv = self._get_all_attributes(traits)
        with open(cvs_path, "w") as f:
            f.write("")
        with open(cvs_path,'a') as f:
            for line in csv:
                f.write(line)

    def write_combine_void(self, new_file, files):
        combined_contents = ''
        is_first = True
        for file in files:
            with open(file) as f:
                contents = f.read()
                if is_first:
                    is_first = False
                else:
                    #remove the first line
                    contents = contents[contents.find("\n")+1:]
                    pass
                combined_contents +=  contents
        with open(new_file, "w") as f:
            f.write("")
        with open(new_file,'a') as f:
            f.write(combined_contents)

