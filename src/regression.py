from pprint import pprint
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import itertools

# Import the data
nyc_registry = pd.read_csv('../dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
coren = pd.read_csv('../dogdata/coren-edit.csv')
nyc_census = pd.read_csv('../censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('../dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('../dogdata/Dog_Registrations_Adelaide_2016-edit.csv')
wiki = pd.read_csv('../dogdata/wiki-edit.csv')
turcsan = pd.read_csv('../dogdata/turcsan.csv')
