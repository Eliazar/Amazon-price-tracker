from requests import get as requestGet
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

BASE_URL = "https://appbrewery.github.io/instant_pot/"
EMAIL = os.getenv("email")
MAIL_SECRET = os.getenv("secret")
TARGET_PRICE = 100
HOST = os.getenv("host")
PORT = os.getenv("port")


response = requestGet(BASE_URL)
response.raise_for_status()

page = BeautifulSoup(response.text, "html.parser")
rawPrice = page.find("span", class_="aok-offscreen").string

#We get the 99.99 part of the string to convert it to float
price = float(rawPrice.split("$")[1])

if price < TARGET_PRICE:
    with smtplib.SMTP(host = HOST, port = PORT) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=MAIL_SECRET)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject:Price alert!!\n\nThe product has lower price than the target")