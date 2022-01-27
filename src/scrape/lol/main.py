from bs4 import BeautifulSoup as bs
import requests
import json

# Converting URL to Image
import urllib
import cvzone
import cv2
import numpy as np

# Reading champion names and keys to fetch builds from web page.
champions = open("champions.json")
champions_data = json.load(champions)

# Contains the base URL address
pre_build_url = "https://www.probuilds.net/champions/details/"

# Temporary variables to store temporary data
is_champion_exist = False
selected_champion_key = 0
selected_champion_name = ""

"""
@param input Champion name is entered, type is String
"""
def champion_filter(input):

    # Is the champion entered by the user available in the list?
    for champion in champions_data["champions"]:
        if champion["name"].lower() == input.lower():
            is_champion_exist = True
            selected_champion_name, selected_champion_key = champion["name"], champion["key"]
            break
        else:
            is_champion_exist = False

    if is_champion_exist:
        return selected_champion_name, selected_champion_key
    else:
        return False

"""
@param champ_key Contains champion key value which necessary to fetch build about this champion
"""
def fetch_build(champ_key):
    # Web Page URL section and downloads all data and parse them.
    url = pre_build_url + champ_key

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

def url_to_img(arr):
    url = arr[0][1]

    # Read Background Image
    background_image = cv2.imread("bg_image_empty.png")

    # URL to Image Process
    url_response = urllib.request.urlopen(url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    img = cv2.resize(img, (50, 50), interpolation=cv2.INTER_NEAREST)

    # background_image = cv2.putText(background_image, 'Build', (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    # Process of Overlaying Images
    x_offset, y_offset = 14, 100
    background_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img

    cv2.imshow('League of Legends', background_image)
    cv2.waitKey()




selection = champion_filter("evelynn")
if selection:
    name, key = selection[0], selection[1]
    data_dict = fetch_build(key)
    data = np.array(list(data_dict.items()))

    url_to_img(data)

else:
    print("Champion Could Not Found!")
