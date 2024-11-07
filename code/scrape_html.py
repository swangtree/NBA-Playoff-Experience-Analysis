import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.basketball-reference.com/playoffs/2023-nba-eastern-conference-first-round-heat-vs-bucks.html"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

with open("test.txt", "w+", encoding="utf-8") as f:
    f.write(soup.prettify())