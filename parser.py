import requests 
#from pathlib import Path
import unicodedata
from bs4 import BeautifulSoup


#pwd = Path("/home/seonils/data_storage/story/")
#datadir_json = pwd / "json" 
#header = req.headers
#status = req.status_code
#is_ok = req.ok


def refine(entity, instance):
    if entity == "genre_list":
        for i, genre in enumerate(instance): #instance == genre_list
            try: instance[i] = instance.contents[0].contents[0] 
            except: instance = instance_list[:-1]
        return instance
    elif entity == "runningtime": #instance == runningtime
        instance = int(instance[0].attrs['datetime'][2:-1])
        return instance
    else: # title, year
        res = instance[0].contents[0] #instance == year or title
        return res if entity=="year" else unicodedata.normalize("NFKD", res) 

    
    
def title_yr_genre_runtime(self):
    req = requests.get("https://www.imdb.com/title/{moviekey}/".format(moviekey=moviekey))
    html = req.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select(
        "#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > h1",) # CSSselector
    year = soup.select("#titleYear > a",)
    genre_list = soup.select("#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > div.subtext > a",)
    runningtime = soup.select("#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > div > time",)

    result_dict = {}

    for entity in ["title", "year", "genre_list", "runningtime"]:
        result_dict[entity] = refine(entity, eval(entity))

    return result_dict # {"title": ____, "year":____, "genre_list": [__, __, __, __, ..], "runningtime": ___(int in min)}


