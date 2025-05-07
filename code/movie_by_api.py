import requests
import json
url = "https://api.wmdb.tv/api/v1/top"
querystring = {"type":"Imdb","skip":0,"limit":250,"lang":"En"}
response = requests.request("GET", url, params=querystring)
data = response.text.encode("utf-8")
with open("../data/movie_api_top_250.json","wb")as f:
    f.write(data)
print(data)
