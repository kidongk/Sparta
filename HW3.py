import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta_class


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


charts = soup.select(' #body-content > div.newest-list > div > table > tbody > tr')

for chart in charts:
    title = chart.select_one('td.info > a.title.ellipsis').text
    artist = chart.select_one('td.info > a.artist.ellipsis').text
    album = chart.select_one(' td.info > a.albumtitle.ellipsis').text
    db.music_chart.insert_one({'Title': title, 'Artist': artist, 'Album': album})



# title
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
#body-content > div.newest-list > div > table > tbody > tr:nth-child(2) > td.info > a.title.ellipsis

# artist
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

# album
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.albumtitle.ellipsis
