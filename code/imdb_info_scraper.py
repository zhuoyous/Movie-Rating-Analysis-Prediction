# imdb info
import json
import sys
import traceback

from utils import get_soup
from lxml import etree
import requests
def prepare_movie_urls():
    with open("../data/movie_url.json", "r") as f:
        movies = json.load(f)
    urls = [m['full_imdb_url'] for m in movies]
    return urls

def parse_item_info():
    urls = prepare_movie_urls()
    movie_infos=[]
    for url in urls:
        try:
            item = {}
            r = requests.get(url)
            content = r.content
            selector = etree.HTML(content)
            try:
                movie_title = selector.xpath('//h1/text()')[0]
            except:
                print(traceback.format_exc())
                movie_title = ""
            item["movie_title"] = movie_title
            print(url)
            #//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/ul/li[1]/span
            title_year = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/ul/li[1]/span/text()')[0]
            item["title_year"] = title_year
            genres = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div//text()')[0]
            item["genres"] = genres
            # //*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[2]/span
            # //*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[2]/div/ul/li[1]/a/text()
            try:
                country = selector.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[2]//text()')[1]
            except:
                country = ""
            item["country"] = country
            #//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[10]/div[2]/ul/li[2]/div/ul/li[1]/a/text()
            try:
                language = selector.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[4]//text()')[1]
            except:
                language = ""
            item['language'] = language
            time = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/ul/li[3]/text()')
            item['time'] = time
            try:
                plot_keywords = selector.xpath('//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[7]/div[2]/div[2]/a/span/text()')[0]
            except:
                plot_keywords = ""
            item['plot_keywords'] = plot_keywords
            imdb_score = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]/text()')[0]
            item['imdb_score'] = imdb_score
            num_user_for_reviews = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a/span/span[1]/text()')[0]
            item['num_user_for_reviews'] = num_user_for_reviews
            num_critic_for_reviews = selector.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[2]/a/span/span[1]/text()')[0]
            item['num_critic_for_reviews'] = num_critic_for_reviews
            #//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[12]/div[2]/ul/li[4]/span
            #//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[14]/div[2]/ul/li[4]/div/ul/li/span/text()
            #//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[14]/div[2]/ul/li[4]/div/ul/li/span
            try:
                aspect_ratio = selector.xpath('//span[contains(text(), " : 1")]/text()')[0]
            except:
                aspect_ratio = ""
            item['aspect_ratio'] = aspect_ratio
            item['url']=url
            print(item)
            movie_infos.append(item)
        except:
            print(traceback.format_exc())
    movie_info_json = json.dumps(movie_infos, ensure_ascii=False)
    with open("../data/movie_info.json", "w") as f:
        f.write(movie_info_json)






if __name__ == '__main__':
    parse_item_info()
