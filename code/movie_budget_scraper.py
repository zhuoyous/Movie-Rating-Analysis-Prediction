import json

import requests
import pandas as pd
from bs4 import BeautifulSoup
def get_soups():
    url = "https://www.the-numbers.com/movie/budgets/all"
    soups = []
    for k in range(100,5000,100):
        url_k = url+'/'+str(k)
        r = requests.get(url)
        soup = BeautifulSoup(r.text.replace("\xc2","").replace("\xa0","").replace("\xe2","").replace("\x80","").replace("\x99",""), 'html.parser')
        soups.append(soup)
    return soups

def get_movie_metadat():
    #
    movie_bugget_infos = []
    prefix = "http://www.the-numbers.com"
    soups = get_soups()
    for soup in soups:
        print(soup.encode("utf-8"))
        rows_in_big_table = soup.find_all('tr') # set
        for i, onerow in enumerate(rows_in_big_table):
            if i % 2 == 0:
                continue
            print(onerow.encode("utf-8"))
            items = onerow.find_all('a')
            release_date = items[0].string
            _partial_url = items[0].attrs['href']
            print(_partial_url)
            movie_link = prefix + _partial_url
            movie_name = items[1].string
            print(movie_name)

            budgets = onerow.find_all('td')
            production_budget = budgets[-3].string.replace("\xc2","").replace("\xa0","")
            domestic_gross = budgets[-2].string.replace("\xc2","").replace("\xa0","")
            worldwide_gross = budgets[-1].string.replace("\xc2","").replace("\xa0","")
            print(release_date,production_budget,domestic_gross,worldwide_gross)
            movie_item = {"movie_name":movie_name,"release_date":release_date,"production_budget":production_budget,
                          "domestic_gross":domestic_gross,"worldwide_gross":worldwide_gross,"movie_link":movie_link}
            movie_bugget_infos.append(movie_item)
    movie_bugget_json = json.dumps(movie_bugget_infos,ensure_ascii=False)
    with open("../data/movie_budget.json", "w") as f:
        f.write(movie_bugget_json)




if __name__ == '__main__':
    get_movie_metadat()
