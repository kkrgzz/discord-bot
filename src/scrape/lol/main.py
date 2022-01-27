from bs4 import BeautifulSoup as bs
import requests
import json


user_input = "JiNX"

# Reading champion names and keys to fetch builds from web page.
champions = open("champions.json")
champions_data = json.load(champions)

# Web Page URL section and downloads all data and parse them.
main_url = "https://www.probuilds.net/champions/details/222"
request = requests.get(main_url)
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


for champion in champions_data["champions"]:
    if champion["name"].lower() == user_input.lower():
        print(champion["name"], " - ", champion["key"])
