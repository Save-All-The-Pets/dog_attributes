import time
from pprint import pprint
import sys
import pandas as pd
from fuzzywuzzy import fuzz
import re



nyc_registry = pd.read_csv('dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
iq = pd.read_csv('dogdata/dog_intelligence-edit.csv')
nyc_census = pd.read_csv('censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('dogdata/Dog_Registrations_Adelaide_2016-edit.csv')

# Make the census columns understandable
val = 'EST_'
err = 'MOE_'
age_under_5 = 'VC16'
age_5_17 = 'VC17'; age_18_24 = 'VC18'
age_25_34 = 'VC19'; age_35_44 = 'VC20'
age_45_54 = 'VC21'; age_55_64 = 'VC22'
age_65_74 = 'VC23'; age_75_over = 'VC24'

# Sometimes centimeters are first and sometimes inches are first
# wiki['Height'] = wiki['Height'].apply(lambda x: re.search(r'\d+', x).group())

pprint(nyc_registry.head())
pprint(nyc_census.head())
pprint(iq.head())
pprint(edmonton_registry.head())
pprint(adelaide_registry.head())
pprint(wiki.head())


# fuzz.ratio(