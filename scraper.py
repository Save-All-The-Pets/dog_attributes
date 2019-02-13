from pymongo import MongoClient
import requests
import time
from pandas.io.html import read_html
from pprint import pprint
import sys
from collections import defaultdict


client = MongoClient('localhost', 27017)
# Access/Initiate Database
db = client['dogs']
# Access/Initiate Table
data = db['data']

counter = 0

#Capturing data for male dogs 
categories= ['Origin', 'Height', 'Weight', 'Color', 'Coat', 'AKC', 'FCI', 'ANKC', 'CKC', 'KC (UK)', 'NZKC', 'UKC']

with open('dogdata/urls.txt') as f:
    lst = f.read().splitlines() 

for url in lst:
    d = defaultdict(str)
    print(url)
    counter += 1
    try:
        infobox = read_html(url, index_col=0, attrs={"class":"infobox biota"})
        dog_breed = url.replace('https://en.wikipedia.org/wiki/','').replace('_(dog)', '').replace('_',' ')
        d['Breed'] = dog_breed
        success = True
    except:
        print("Error: " , sys.exc_info()[0])
        success = False
        continue
    if success:
        for cat in categories:
            try:
                if (cat == 'Color'):
                    d[cat] = infobox[0].xs(cat).values[0][0]
                elif (cat == 'Weight'): # unnecessary due to additional dataset on height and weight
                    if infobox[0].xs(cat).values[0][0] == 'Male':
                        d[cat] = infobox[0].xs(cat).values[0][1]
                    else:
                        d[cat] = infobox[0].xs(cat).values[0][0]                        
                elif (cat == 'Height'): # unnecessary due to additional dataset on height and weight
                    if infobox[0].xs(cat).values[0][0] == 'Male':
                        d[cat] = infobox[0].xs(cat).values[0][1]
                    else:
                        d[cat] = infobox[0].xs(cat).values[0][0]  
                else:
                    if type(infobox[0].xs(cat).values[0]) == str:
                        d[cat] = infobox[0].xs(cat).values[0]
                    else:
                        d[cat] = infobox[0].xs(cat).values[0][0]
                d['URL'] = url  #currently repeats
            except:
                print("Error: " , sys.exc_info()[0])
                continue
        result=db.data.insert_one(d)
        pprint('Created new object id {0}'.format(result.inserted_id))

        if (counter %5 == 0):
            time.sleep(4)
f.close()

cursor = data.find()
for document in cursor: 
    pprint(document)

# Litter size, life span isn't working because they're two words