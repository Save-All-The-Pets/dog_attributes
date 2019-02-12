from pymongo import MongoClient
import time
from pprint import pprint
import sys
import pandas as pd

nyc_registry = pd.read_csv('NYC_Dog_Licensing_Dataset.csv')
iq = pd.read_csv('dog_intelligence.csv')
nyc_census = pd.read_csv('ACS_17_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('Edmonton_Pet_Licenses_by_Neighbourhood.csv')
adelaide_registry = pd.read_csv('Dog_Registrations_Adelaide_2016.csv')