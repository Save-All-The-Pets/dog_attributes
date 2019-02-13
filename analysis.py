import time
from pprint import pprint
import pandas as pd
import sys
from fuzzywuzzy import fuzz
import re

nyc_registry = pd.read_csv('dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
coren = pd.read_csv('dogdata/dog_intelligence-edit.csv')
nyc_census = pd.read_csv('censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('dogdata/Dog_Registrations_Adelaide_2016-edit.csv')
wiki = pd.read_csv('dogdata/wiki-edit.csv')
iq = turcsan = pd.read_csv('dogdata/turcsan.csv')

#iq = coren.set_index('Breed').join(turcsan.set_index('Breed'), how='inner')


# Canine intelligence by AKC Groupings
wiki_pared = wiki[['Breed', 'AKC']]
akc_groups_iq = wiki_pared.set_index('Breed').join(iq.set_index('Breed'), how='left')
akc = akc_groups_iq.groupby('AKC').mean()
pprint(akc)
akc_count = akc_groups_iq.groupby('AKC').count()
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
nyc_registry['Borough'] = nyc_registry['Borough'].map(lambda x: '' if x not in {'Brooklyn', 'Bronx', 'Staten Island', 'Manhattan', 'Queens'} else x)

nyc_iq = nyc_registry.set_index('BreedName').join(iq.set_index('Breed'), how='left')

#Redo this section, which is inefficient
# queens = nyc_iq[nyc_iq['Borough'] == 'Queens']
# manhattan = nyc_iq[nyc_iq['Borough'] == 'Manhattan']
# brooklyn = nyc_iq[nyc_iq['Borough'] == 'Brooklyn']
# bronx = nyc_iq[nyc_iq['Borough'] == 'Bronx']
# staten = nyc_iq[nyc_iq['Borough'] == 'Staten Island']

# print('Queens: ' + str(queens['obey'].mean()))
# print('Manhattan: ' + str(manhattan['obey'].mean()))
# print('Brooklyn: ' + str(brooklyn['obey'].mean()))
# print('Bronx: ' + str(bronx['obey'].mean()))
# print('Staten Island: ' + str(staten['obey'].mean()))
# print('NYC Overall: ' + str(nyc_iq['obey'].mean()))

# print('Queens Standard Deviation: ' + str(queens['obey'].std()))
# print('Manhattan Standard Deviation: ' + str(manhattan['obey'].std()))
# print('Brooklyn Standard Deviation: ' + str(brooklyn['obey'].std()))
# print('Bronx Standard Deviation: ' + str(bronx['obey'].std()))
# print('Staten Island Standard Deviation: ' + str(staten['obey'].std()))
# print('NYC Overall Standard Deviation: ' + str(nyc_iq['obey'].std()))

nyc_iq_t = nyc_registry.set_index('BreedName').join(turcsan.set_index('Breed'), how='left')
nyc_iq_t_g = nyc_iq_t.groupby('Borough').mean()
pprint(nyc_iq_t_g)

# Adelaide
adelaide_iq = adelaide_registry.set_index('AnimalBreed').join(iq.set_index('Breed'), how='left')
print('Adelaide: ' + str(adelaide_iq['obey'].mean()))
print('Adelaide Standard Deviation: ' + str(adelaide_iq['obey'].std()))

# Edmonton
edmonton_iq = edmonton_registry.set_index('BREED').join(iq.set_index('Breed'), how='left')
print('Edmonton: ' + str(edmonton_iq['obey'].mean()))
print('Edmonton Standard Deviation: ' + str(edmonton_iq['obey'].std()))

# Which ancestral homeland has the smartest/most obedient dogs?
ancestral = wiki[['Breed', 'Origin']]

# Only looking at the UK and Ireland
ancestral_uk_ire = ancestral.copy()
ancestral_uk_ire.dropna()
ancestral_uk_ire = ancestral_uk_ire.loc[ancestral_uk_ire['Origin'].isin(['England', 'Scotland', 'Wales', 'Ireland'])]
ancestral_uk_ire_iq = ancestral_uk_ire.set_index('Breed').join(iq.set_index('Breed'), how='inner')
ancestral_uk_ire_iq_group = ancestral_uk_ire_iq.groupby('Origin').mean()
print('UK and Ireland only')
pprint(ancestral_uk_ire_iq_group)
ancestral_uk_ire_std = ancestral_uk_ire_iq.groupby('Origin').std()
pprint(ancestral_uk_ire_std)
ancestral_uk_ire_count = ancestral_uk_ire_iq.groupby('Origin').count()
pprint(ancestral_uk_ire_count)

# Combining Scotland, Wales, and England as United Kingdom
ancestral2 = ancestral.copy()
ancestral2['Origin'] = ancestral['Origin'].map(lambda x: 'United Kingdom' if x in {'England', 'Wales', 'Scotland'} else x)
ancestral_iq = ancestral2.set_index('Breed').join(iq.set_index('Breed'), how='inner')

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

ancestral_iq.dropna(inplace=True)
ancestral_iq2 = splitDataFrameList(ancestral_iq,'Origin', '/')

ancestral_iq_group = ancestral_iq2.groupby('Origin').mean()
pprint(ancestral_iq_group)
ancestral_count = ancestral_iq2.groupby('Origin').count()
pprint(ancestral_count)


wiki_breeds = set(wiki['Breed'].tolist())
coren_breeds = set(iq['Breed'].tolist())

print('Intersection')
print(wiki_breeds & coren_breeds)
print('Difference')
print(wiki_breeds - coren_breeds)
print(coren_breeds - wiki_breeds)

# pprint(manhattan.count())
# pprint(staten.count())

# pprint(nyc_registry.head())
# pprint(nyc_census.head())
# pprint(iq.head())
# pprint(edmonton_registry.head())
# pprint(adelaide_registry.head())
# pprint(wiki.head())
# nyc_registry.describe()

# Use fuzzing after exact match
# fuzz.ratio(