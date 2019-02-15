from pymongo import MongoClient
import pandas as pd

# Convert mongo to a DataFrame
client = MongoClient('localhost', 27017)
# Access/Initiate Database
db = client['dogs']
# Access/Initiate Table
data = db['data']
#convert entire collection to Pandas dataframe
wiki = pd.DataFrame(list(data.find()))

wiki.to_csv('dogdata/wiki.csv')