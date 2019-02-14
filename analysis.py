import time
from pprint import pprint
import pandas as pd
import sys
from fuzzywuzzy import process
import re

nyc_registry = pd.read_csv('dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
coren = pd.read_csv('dogdata/coren-edit.csv')
nyc_census = pd.read_csv('censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('dogdata/Dog_Registrations_Adelaide_2016-edit.csv')
wiki = pd.read_csv('dogdata/wiki-edit.csv')
attrib = turcsan = pd.read_csv('dogdata/turcsan.csv')

#coren = coren[['Breed', 'obey']]
#attrib = coren.set_index('Breed').join(turcsan.set_index('Breed'), how='outer')

lst = ['Calm', 'Trainable', 'Sociable', 'Bold']

# Canine attributes by AKC Groupings
wiki_akc = wiki[['Breed', 'AKC']]
akc_groups_attrib = wiki_akc.set_index('Breed').join(attrib.set_index('Breed'), how='left')
print('\nAKC Mean')
akc = akc_groups_attrib.groupby('AKC').mean().round(decimals=2)
pprint(akc)
print('\nAKC Standard Deviation')
akc_std = akc_groups_attrib.groupby('AKC').std().round(decimals=2)
pprint(akc_std)
akc_count = akc_groups_attrib.groupby('AKC').count()
pprint(akc_count)

# Make the census columns understandable
val = 'EST_'
err = 'MOE_'
age_under_5 = 'VC16'
age_5_17 = 'VC17'; age_18_24 = 'VC18'
age_25_34 = 'VC19'; age_35_44 = 'VC20'
age_45_54 = 'VC21'; age_55_64 = 'VC22'
age_65_74 = 'VC23'; age_75_over = 'VC24'

# Strip out dirty values
nyc_registry['Borough'] = nyc_registry['Borough'].map(lambda x: None if x not in {'Brooklyn', 'Bronx', 'Staten Island', 'Manhattan', 'Queens'} else x)
nyc_registry.dropna(inplace=True)

nyc_attrib = nyc_registry.set_index('BreedName').join(attrib.set_index('Breed'), how='left')
nyc_attrib_t = nyc_registry.set_index('BreedName').join(turcsan.set_index('Breed'), how='left')
nyc_attrib_t = nyc_attrib_t[['Borough','Calm', 'Trainable', 'Sociable', 'Bold']]
nyc_attrib_t_g = nyc_attrib_t.groupby('Borough')
pprint(nyc_attrib_t_g.mean().round(decimals=2))
pprint(nyc_attrib_t_g.std().round(decimals=2))
pprint(nyc_attrib_t_g.count())


# Adelaide
adelaide_attrib = adelaide_registry.set_index('AnimalBreed').join(attrib.set_index('Breed'), how='left')

print('\nAdelaide Mean')
print(adelaide_attrib[lst].mean().round(decimals=2))
print('\nAdelaide Standard Deviation')
print(adelaide_attrib[lst].std().round(decimals=2))

# Edmonton
print('\nEdmonton Mean')
edmonton_attrib = edmonton_registry.set_index('BREED').join(attrib.set_index('Breed'), how='left')
print(edmonton_attrib[lst].mean().round(decimals=2))
print('\nEdmonton Standard Deviation')
print(edmonton_attrib[lst].std().round(decimals=2))

ancestral = wiki[['Breed', 'Origin']]

# Looking at the UK and Ireland
ancestral_uk_ire = ancestral.copy()
ancestral_uk_ire.dropna()
ancestral_uk_ire = ancestral_uk_ire[ancestral_uk_ire['Origin'].isin(['England', 'Scotland', 'Wales', 'Ireland'])]
ancestral_uk_ire = ancestral_uk_ire.set_index('Breed').join(attrib.set_index('Breed'), how='inner')
ancestral_uk_ire_grp = ancestral_uk_ire.groupby('Origin')
print('\nUK and Ireland Mean')
print(ancestral_uk_ire_grp.mean().round(decimals=2))
print('\nUK and Ireland Standard Deviation')
print(ancestral_uk_ire_grp.std().round(decimals=2))
print('\nUK and Ireland Count')
print(ancestral_uk_ire_grp.count())

# Combining Scotland, Wales, and England as United Kingdom
ancestral['Origin'] = ancestral['Origin'].map(lambda x: 'United Kingdom' if x in {'England', 'Wales', 'Scotland'} else x)
ancestral_attrib = ancestral.set_index('Breed').join(attrib.set_index('Breed'), how='inner')

# Take cells with multiple countries and split them into separate countries
def splitDataFrameList(df,target_column,separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    Thanks to James Allen, https://gist.github.com/jlln/338b4b0b55bd6984f883
    '''
    def splitListToRows(row,row_accumulator,target_column,separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
    new_df = pd.DataFrame(new_rows)
    return new_df

ancestral_attrib.dropna(inplace=True)
ancestral_attrib2 = splitDataFrameList(ancestral_attrib,'Origin', '/')
ancestral_attrib2['Origin'] = ancestral_attrib2['Origin'].map(lambda x: 'China' if x == 'Tibet (China)' else x)

ancestral_attrib_grp = ancestral_attrib2.groupby('Origin')

ancestral_attrib_count = ancestral_attrib_grp.count()
ancestral_attrib_mean =  ancestral_attrib_grp.mean().round(decimals=2)

# Only display values where there is more than one dog
ancestral_attrib_mean_filtered = ancestral_attrib_mean[ancestral_attrib_count['Bold'] > 1]

print('\nAncestral Origin Mean, n>1')
pprint(ancestral_attrib_mean_filtered)
print('\nAncestral Origin Standard Deviation')
pprint(ancestral_attrib_grp.std().round(decimals=2).dropna())
print('\nAncestral Origin Count')
pprint(ancestral_attrib_count)

wiki_breeds = set(wiki['Breed'].tolist())
coren_breeds = set(coren['Breed'].tolist())
turcsan_breeds = set(turcsan['Breed'].tolist())

print('\nIntersection')
print(wiki_breeds & turcsan_breeds)
print('\nDifference, Wiki - Turcsan')
print(wiki_breeds - turcsan_breeds)
print('\nDifference, Turcsan - Wiki')
print(turcsan_breeds - wiki_breeds)

comparison = wiki[['Breed']]
comparison['Turcsan'] = comparison['Breed'].apply(lambda x: process.extractOne(x, list(turcsan_breeds)) if x not in turcsan_breeds else '')
comparison['Coren'] = comparison['Breed'].apply(lambda x: process.extractOne(x, list(coren_breeds)) if x not in coren_breeds else '')
#comparison.to_csv('dogdata/comparisons.csv')
