from bs4 import BeautifulSoup as bs
import requests
import json

# Converting URL to Image
import urllib
import cv2
import numpy as np

# Saving Image File
import os

class LolBuildScraper:
    def __init__(self):
        # Reading champion names and keys to fetch builds from web page.
        self.champions = open("champions.json")
        self.champions_data = json.load(self.champions)

        # Contains the base URL address
        self.pre_build_url = "https://www.probuilds.net/champions/details/"

        # Temporary variables to store temporary data
        self.is_champion_exist = False
        self.selected_champion_key = 0
        self.selected_champion_name = ""

    """
    @param input Champion name is entered, type is String
    """
    def champion_filter(self, input):

        # Is the champion entered by the user available in the list?
        for champion in self.champions_data["champions"]:
            if champion["name"].lower() == input.lower():
                self.is_champion_exist = True
                self.selected_champion_name, self.selected_champion_key = champion["name"], champion["key"]
                break
            else:
                self.is_champion_exist = False

        if self.is_champion_exist:
            return self.selected_champion_name, self.selected_champion_key
        else:
            return False

    """
    @param champ_key Contains champion key value which necessary to fetch build about this champion
    """
    def fetch_build(self, champ_key):
        # Web Page URL section and downloads all data and parse them.
        url = self.pre_build_url + champ_key

        request = requests.get(url, cookies={"lang": "tr_TR"})

        soup = bs(request.text, "lxml")

        # Filtering classes which equals to bigData.
        items = soup.find_all(class_ = "bigData")

        # Stores item names and images of items, respectively
        item_names_arr = []
        item_images_arr = []

        # Parsing data
        for item_containers in items:
            item_names = item_containers.find_all(class_ = "item-name")
            for name in item_names:
                item_names_arr.append(name.text)

            item_imgs = item_containers.find_all("img")
            for img in item_imgs:
                item_images_arr.append(img.get("src"))

        zip_arr = zip(item_names_arr, item_images_arr)
        dictionary = dict(zip_arr)

        return dictionary


    """
    @param arr Array variable. It contains item names and item image URLs inside.
    """
    def url_to_img(self, arr):
        # Read Background Image
        background_image = cv2.imread("bg_image_empty.png")

        """
        List of Popular Items Overlayed on the Background Image
        @param i Alignment variable. Determines start position of each item on the screen.
        """
        i = 14
        for item in arr[0:6]:
            url = item[1]
            # URL to Image Process
            url_response = urllib.request.urlopen(url)
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
            img = cv2.resize(img, (50, 50), interpolation=cv2.INTER_NEAREST)

            # Process of Overlaying Images
            x_offset, y_offset = i, 40
            background_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img

            i += 64

        """
        List of Popular Summoners Spells Overlayed on the Background Image
        @param i Alignment variable. Determines start position of each item on the screen.
        """
        i = 14
        for item in arr[7:9]:
            url = item[1]
            # URL to Image Process
            url_response = urllib.request.urlopen(url)
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
            img = cv2.resize(img, (50, 50), interpolation=cv2.INTER_NEAREST)

            # Process of Overlaying Images
            x_offset, y_offset = i, 130
            background_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img

            i += 64

        return background_image
        #cv2.imshow('Lol Build', background_image)
        #cv2.waitKey()


    def getBuild(self, save_as_image = False, output_file_name = "build", output_file_extension = "jpg"):
        selection = self.champion_filter("jinx")
        if selection:
            name, key = selection[0], selection[1]
            data_dict = self.fetch_build(key)
            data = np.array(list(data_dict.items()))

            image = self.url_to_img(data)

            if save_as_image:
                file_name = output_file_name + "." + output_file_extension
                cv2.imwrite(file_name, image)

            return image

        else:
            print("Champion Could Not Found!")
