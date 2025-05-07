import os
import re
import pandas as pd
import json
import csv


base_dir = "../data"
def parse_view_user_number(view_user_number):
    # eg: "8.5K" --> "85000"
    print(view_user_number)
    if not view_user_number:
        return 0
    size = len(view_user_number)

    if view_user_number[-1] == 'K':
        return int(float(view_user_number[ : size - 1]) * 1000)
    elif view_user_number.isdigit():
        return int(view_user_number)
    else:
        return 0

def parse_price(price):
    # eg: u'$237,000,000' --> 237000000
    if not price:
        return 0
    else:
        price = int(re.sub('[^0-9,]', "", price))
    return price


def remove_non_ascii_chars_in_string(s):
    return re.sub(r'[^\x00-\x7F]+','', s)

def load_unparsed_movie_metadata():
    with open(os.path.join(base_dir, "movie_info.json"), "r") as f:
        movies = json.load(f)
        return movies

def parse_time(time_list):
    if len(time_list)==5:
        return int(time_list[0])*60+int(time_list[3])
def parse_aspect_ratio(ratio_string):
    if not ratio_string:
        return None
    if ":" in ratio_string:
        return float(ratio_string.split(":")[0].strip())
    else:
        return float(re.search('[0-9,.]+', ratio_string).group())

def parse_one_movie_metadata(movie):
    if not movie:
        return None

    parsed_movie = {}
    parsed_movie['movie_title'] = movie['movie_title']
    parsed_movie['num_user_for_reviews'] = parse_view_user_number(movie['num_user_for_reviews'])
    # parsed_movie['num_voted_users'] = movie['num_voted_users']
    parsed_movie['plot_keywords'] = movie['plot_keywords']
    #parsed_movie['language'] = movie['language']
    #parsed_movie['country'] = movie['country']  # choose 1st country
    parsed_movie['genres'] = movie['genres']
    parsed_movie['time'] = parse_time(movie['time'])
    #parsed_movie['content_rating'] = None if movie['content_rating'] is None or len(movie['content_rating']) == 0 else movie['content_rating'][0].strip()
    #parsed_movie['budget'] = None if movie['budget'] is None or len(movie['budget']) == 0 else parse_price(movie['budget'][0].strip())
    parsed_movie['title_year'] = None if movie['title_year'] is None else int(movie['title_year'])
    #parsed_movie['movie_facebook_likes'] = parse_facebook_likes_number(movie['num_facebook_like'])
    #parsed_movie['storyline'] = movie['storyline'].strip().encode('utf-8')
    parsed_movie['imdb_score'] = float(movie['imdb_score'].strip())
    parsed_movie['aspect_ratio'] = float(movie['aspect_ratio'].split(':')[0].strip()) if len(movie['aspect_ratio'])>0 else None
    #parsed_movie['aspect_ratio'] = parse_aspect_ratio(movie['aspect_ratio'])
    # get number of human faces in movie poster
    num_critic_for_reviews = movie['num_critic_for_reviews']
    parsed_movie['num_critic_for_reviews'] = None if num_critic_for_reviews is None else num_critic_for_reviews
    parsed_movie['movie_link'] = movie['url']
    return parsed_movie

def parse_all_movies():
    movies = load_unparsed_movie_metadata()
    total_count = len(movies)
    print("{} movies".format(total_count))
    parse_movies = []
    for i, movie in enumerate(movies):
        parsed_movie = parse_one_movie_metadata(movie)
        parse_movies.append(parsed_movie)
    df = pd.DataFrame(parse_movies)
    df.to_csv("../data/movie_imb_data.csv")

parse_all_movies()

