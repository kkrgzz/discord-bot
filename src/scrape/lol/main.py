from bs4 import BeautifulSoup as bs
import requests
import json


main_url = "https://www.probuilds.net/champions/details/222"

request = requests.get(main_url)

soup = bs(request.text, "lxml")
items = soup.find_all(class_ = "bigData")

all_items_arr = []

item_names_arr = []
item_images_arr = []

for item_containers in items:

    item_names = item_containers.find_all(class_ = "item-name")
    for name in item_names:
        item_names_arr.append(name.text)

    item_imgs = item_containers.find_all("img")
    for img in item_imgs:
        item_images_arr.append(img.get("src"))

    all_items_arr.append(item_containers)
