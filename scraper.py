from pymongo import MongoClient
import requests
import time
from pandas.io.html import read_html
from pprint import pprint
import sys

client = MongoClient()
# Access/Initiate Database
db = client['dog_db']
# Access/Initiate Table
collection = db['pages']

counter = 0
#Capturing data for male dogs 
categories= ['Origin', 'Height', 'Weight', 'Color', 'Coat', 'AKC', 'FCI', 'ANKC', 'CKC', 'KC (UK)', 'NZKC', 'UKC']

with open('dogdata/urls.txt') as f:
    lst = f.read().splitlines() 

lst = lst[30:35]

for url in lst:
    print(url)
    counter += 1
    try:
        infobox = read_html(url, index_col=0, attrs={"class":"infobox biota"})
        dog_breed = url.replace('https://en.wikipedia.org/wiki/','').replace('_(dog)', '').replace('_',' ')
        pprint(dog_breed)
    except:
        print("Error: " , sys.exc_info()[0])
        continue
    for cat in categories:
        try:
            pprint(cat)
            if (cat == 'Color'):
                pprint(infobox[0].xs('Color').values[0][0])
            elif (cat == 'Weight'):
                pprint(infobox[0].xs('Weight').values[0][1])
            elif (cat == 'Height'):
                pprint(infobox[0].xs('Height').values[0][1])
            # elif (cat == 'Life span'):
            #     pprint(infobox[0].xs('Life span').values[0])
            else:
                if type(infobox[0].xs(cat).values[0]) == str:
                    pprint(infobox[0].xs(cat).values[0])
                else:
                    pprint(infobox[0].xs(cat).values[0][0])
        except:
            print("Error: " , sys.exc_info()[0])
            continue

    if (counter %5 == 0):
        time.sleep(6)
f.close()

# Litter size, life span isn't working because they're two words

# TO DO: Export names with the URLs, import them here