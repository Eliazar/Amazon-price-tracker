from bs4 import BeautifulSoup
from dotenv import load_dotenv
import smtplib
import os
import requests

load_dotenv()

BASE_URL = "https://www.amazon.com/Introducing-Amazon-Soundbar-speaker-Virtual/dp/B0C4BZ28PG/ref=sr_1_1?crid=2I4NHEY2EHTBM&dib=eyJ2IjoiMSJ9.CZDdZb5X69w6upI_PhEh7-v-AHSwdlVXl0aG6k8gmzpmhU7uPr-QwQFQ40W3NkhpkVMbBUvc6sXoeONyk3zmTo_moiYEsQQMyMmBrt7vAkwHi0_G_tuPSTPGIKRCj8GXOvB13YJbIC5xY9LIylsHiuFNiYijkr9RJRkG7Ipd_oV92mlF-9DO_sTJw5hRRB5xMn8R54niju60riT95sYAjT0vS1p7dZ8uOFQ_lg-q9rs.eIwI3IuH4o9vZdM8TE1aSQYprLn4t_J3UTvNS5R139Q&dib_tag=se&keywords=fire+sound+bar&qid=1724885471&sprefix=fire+sound+%2Caps%2C124&sr=8-1"
HTTP_HEADERS = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip, deflate, br, zstd",
        "Accept-Language":"en-US,en;q=0.9,es-HN;q=0.8,es-ES;q=0.7,es;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
    }

EMAIL = os.getenv("email")
MAIL_SECRET = os.getenv("secret")
TARGET_PRICE = 100
HOST = os.getenv("host")
PORT = os.getenv("port")


response = requests.get(BASE_URL, headers=HTTP_HEADERS)
response.raise_for_status()

page = BeautifulSoup(response.text, "html.parser")
print(page.prettify())
rawPrice = page.find("span", class_="aok-offscreen").string

#We get the 99.99 part of the string to convert it to float
price = float(rawPrice.split("$")[1])

if price < TARGET_PRICE:
    with smtplib.SMTP(host = HOST, port = PORT) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=MAIL_SECRET)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject:Price alert!!\n\nThe product has lower price than the target")

