import requests 
import unicodedata
from bs4 import BeautifulSoup
import clip_length as cl
from pathlib import Path
#from IPython.core.debugger import set_trace



class MovieInfo:
    def __init__(self, moviekey):
        #set_trace()
        self.vidpath = Path("/home/seonils/data_storage/story/video_clips/").resolve()
        self.moviekey = moviekey
        self.req = requests.get("https://www.imdb.com/title/{moviekey}/".format(moviekey=self.moviekey))
        self.html = self.req.text
        self.soup = BeautifulSoup(self.html, "html.parser")
        
        self.title = self.soup.select(
        "#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > h1",) 
        self.year = self.soup.select("#titleYear > a",) if not self.moviekey=="tt0244353" else \
                    self.soup.select( "#title-episode-widget > div > div") # tt0244353 exception
        self.genre_list = self.soup.select("#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > div.subtext > a",)
        self.running_time = self.soup.select("#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > div > time",)
        
    def refine(self, entity):
        if entity == "genre_list":
            for i, genre in enumerate(self.genre_list): #instance == genre_list
                try: self.genre_list[i] = self.genre_list[i].contents[0].contents[0] 
                except: 
                    if len(self.genre_list)>1: 
                        self.genre_list = self.genre_list[:-1]
            return self.genre_list
        elif entity == "running_time": #instance == runningtime
            self.running_time = int(self.running_time[0].attrs['datetime'][2:-1])
            return self.running_time
        elif entity == "title": # title, year
            self.title = self.title[0].contents[0] #instance == year or title
            return unicodedata.normalize("NFKD", self.title)
        else: #entity == year
            if self.moviekey != "tt0244353": res = self.year[0].contents[0]
            else: res = self.year[3].contents[1].contents[0] # tt0244353 exception
            self.year = res
            return self.year
        
    def key_title_yr_genre_runtime(self):
        result_dict = {}
        result_dict["key"] = self.moviekey
        
        
        for entity in ["title", "year", "genre_list", "running_time"]:
            result_dict[entity] = self.refine(entity)
        
        clips_list = list(self.vidpath.glob("{moviekey}/*mp4".format(moviekey = self.moviekey))) #generator has no __length__() method
        #if self.moviekey == "tt0074285": 
        #    set_trace()
        result_dict["num_clips"] = len(clips_list)
        result_dict["clip_duration"] = [cl.duration(str(clip_path)) for clip_path in clips_list]
        return result_dict 
    
    # {"key": self.moviekey, "title": ____, "year":____, "genre_list": [__, __, __, __, ..], "runningtime": ___(int in min), num_clips: ___, clip_duration: [___, ___, ___, ... (in secs)] }


#SSL error?
#tt1182345