# IMDB crawler for movieQA genre walkthru

### requirements
experiments (visualization) are done under jupyter lab = v4.4.0

```
# for data analysis
python >= 3.x
numpy 
pandas

# for crawler

```    

### data visualization with pandas
> analysis.ipynb   

 crawling over movieQA genre is done and summarized as <code>imdb_crawled_whole.json</code> file.  
 - genre information of each movie follows imdb classification
 - movie lists from movieQA (imdb keys starting with "tt"): <code>id_ds_splits.json</code>

### crawler
> crawler_main.ipynb    

 crawler is implemented with bs4 and python requests lib.



### acknowledgement
Thx to sigran0 for many helps    

### ref source
https://beomi.github.io/gb-crawling/posts/2017-01-20-HowToMakeWebCrawler.html
http://docs.python-requests.org/en/master/user/quickstart/#make-a-request
https://github.com/sigran0/LyricScrapper/blob/master/Scrapper/MelonLyricScrapper.py
