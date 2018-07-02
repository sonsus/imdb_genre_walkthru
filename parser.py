import requests 
import json
from pathlib import Path
from bs4 import BeautifulSoup

pwd = Path("/home/seonils/data_storage/story/")
# child folder path (Path obj)
datadir_json = pwd / "json" 

req = requests.get("https://www.imdb.com/title/tt0074285/")
html = req.text

#header = req.headers
#status = req.status_code
#is_ok = req.ok

soup = BeautifulSoup(html, "html.parser")

title = soup.select(
    ".title_wrapper > h1:nth-child(1)", # CSSselector
    )
year = soup.select(
    "#titleYear > a:nth-child(1)",
    )


print("title")
print(title.text)
print(title.get("href"))
print("--------------")

print("year")
print(year.text)
print(year.get("href"))
print("------------------")

if not (datadir_json.is_dir()): datadir_json.mkdir() 

data = {}
data[title.text] = title.get("href")
data[year.text] = year.get("href")

with open(datadir_json / "test.json", "w+") as json_file:
    json.dump(data1, json_file)
    json.dump(data2, json_file)
    
