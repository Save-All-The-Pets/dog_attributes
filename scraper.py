from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time
from pandas.io.html import read_html

client = MongoClient()
# Access/Initiate Database
db = client['dog_db']
# Access/Initiate Table
collection = db['pages']

counter = 0


with open('dogdata/urls2.txt') as f:
    lst = f.read().splitlines() 

for url in lst:
    print(url)
    counter += 1
    try:
        infobox = read_html(url, index_col=0, attrs={"class":"infobox biota"})
    except:
        print "Some error"
    print(infobox)
    if (counter %5 == 0):
        time.sleep(6)
f.close()


    # soup = BeautifulSoup(page, 'html.parser')
    # db.insert_one(requests.get({'url': url))