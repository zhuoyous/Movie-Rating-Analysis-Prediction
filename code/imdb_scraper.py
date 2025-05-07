import json
from urllib import parse
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def prepare_imdb_title_search_urls():
    with open("../data/movie_budget.json", "r") as f:
        movies = json.load(f)

    urls = []
    for m in movies:
        title = m['movie_name']
        # >=2018
        release_date = m['release_date']
        year = release_date.split(' ')[-1]
        if int(year) >= 2018:
            title_for_url = parse.quote(title)
            imdb_search_link = "http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt".format(title_for_url)
            urls.append(imdb_search_link)
    return urls


def get_imdb_url():
    urls = prepare_imdb_title_search_urls()
    print("total movies after 2018:{}".format(len(urls)))
    movie_url_infos = []
    for url in urls:
        soup = get_soup(url)
        first_movie_href = soup.find("tr").find("td").find("a").attrs['href']
        first_movie_name = soup.find("tr").find_all("td")[1].find("a").string
        full_imdb_url = "http://www.imdb.com" + first_movie_href
        movie_item = {"movie_name": first_movie_name, "full_imdb_url": full_imdb_url}
        print(full_imdb_url,movie_item)
        movie_url_infos.append(movie_item)
    movie_url_json = json.dumps(movie_url_infos, ensure_ascii=False)
    with open("../data/movie_url.json", "w") as f:
        f.write(movie_url_json)


if __name__ == '__main__':
    get_imdb_url()
