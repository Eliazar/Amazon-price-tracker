from requests import get as requestGet
from bs4 import BeautifulSoup

BASE_URL = "https://appbrewery.github.io/instant_pot/"

response = requestGet(BASE_URL)
response.raise_for_status()

page = BeautifulSoup(response.text, "html.parser")
rawPrice = page.find("span", class_="aok-offscreen").string
print(rawPrice.split("$")[1])

