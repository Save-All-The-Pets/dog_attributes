from pymongo import MongoClient
import requests
import time
from pandas.io.html import read_html
from pprint import pprint
import sys
from collections import defaultdict

d = defaultdict(str)

client = MongoClient()
# Access/Initiate Database
db = client['test_db']
# Access/Initiate Table
coll = db['wiki']

counter = 0

#Capturing data for male dogs 
categories= ['Origin', 'Height', 'Weight', 'Color', 'Coat', 'AKC', 'FCI', 'ANKC', 'CKC', 'KC (UK)', 'NZKC', 'UKC']

with open('dogdata/urls.txt') as f:
    lst = f.read().splitlines() 

lst = lst[45:50]

for url in lst:
    print(url)
    counter += 1
    try:
        infobox = read_html(url, index_col=0, attrs={"class":"infobox biota"})
        dog_breed = url.replace('https://en.wikipedia.org/wiki/','').replace('_(dog)', '').replace('_',' ')
        pprint(dog_breed)
        d['Breed'] = dog_breed
        success = True
    except:
        print("Error: " , sys.exc_info()[0])
        success = False
        continue
    if success:
        for cat in categories:
            try:
                pprint(cat)
                if (cat == 'Color'):
                    pprint(infobox[0].xs('Color').values[0][0])
                    d[cat] = infobox[0].xs(cat).values[0][0]
                elif (cat == 'Weight'):
                    pprint(infobox[0].xs('Weight').values[0][1])
                    d[cat] = infobox[0].xs(cat).values[0][1]
                elif (cat == 'Height'):
                    pprint(infobox[0].xs('Height').values[0][1])
                    d[cat] = infobox[0].xs(cat).values[0][1]
                else:
                    if type(infobox[0].xs(cat).values[0]) == str:
                        pprint(infobox[0].xs(cat).values[0])
                        d[cat] = infobox[0].xs(cat).values[0]
                    else:
                        pprint(infobox[0].xs(cat).values[0][0])
                        d[cat] = infobox[0].xs(cat).values[0][0]
                d['URL'] = url  #currently repeats
            except:
                print("Error: " , sys.exc_info()[0])
                continue
        result=db.coll.insert_one(d)
        pprint('Created new object id {0}'.format(result.inserted_id))

        if (counter %5 == 0):
            time.sleep(6)
f.close()

cursor = db.find({})
for document in cursor: 
    pprint(document)

# Litter size, life span isn't working because they're two words