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
wiki = pd.read_csv('dogdata/wiki-edit.csv')

# Make the census columns understandable
val = 'EST_'
err = 'MOE_'
age_under_5 = 'VC16'
age_5_17 = 'VC17'; age_18_24 = 'VC18'
age_25_34 = 'VC19'; age_35_44 = 'VC20'
age_45_54 = 'VC21'; age_55_64 = 'VC22'
age_65_74 = 'VC23'; age_75_over = 'VC24'

nyc_iq = nyc_registry.set_index('BreedName').join(iq.set_index('Breed'), how='left')

queens = nyc_iq[nyc_iq['Borough'] == 'Queens']
manhattan = nyc_iq[nyc_iq['Borough'] == 'Manhattan']
brooklyn = nyc_iq[nyc_iq['Borough'] == 'Brooklyn']
bronx = nyc_iq[nyc_iq['Borough'] == 'Bronx']
staten = nyc_iq[nyc_iq['Borough'] == 'Staten Island']

pprint('Queens Dog IQ: ' + str(queens['obey'].mean()))
pprint('Manhattan Dog IQ: ' + str(manhattan['obey'].mean()))
pprint('Brooklyn Dog IQ: ' + str(brooklyn['obey'].mean()))
pprint('Bronx Dog IQ: ' + str(bronx['obey'].mean()))
pprint('Staten Island Dog IQ: ' + str(staten['obey'].mean()))
pprint('NYC Overall Dog IQ: ' + str(nyc_iq['obey'].mean()))

pprint('Queens Standard Deviation: ' + str(queens['obey'].std()))
pprint('Manhattan Standard Deviation: ' + str(manhattan['obey'].std()))
pprint('Brooklyn Standard Deviation: ' + str(brooklyn['obey'].std()))
pprint('Bronx Standard Deviation: ' + str(bronx['obey'].std()))
pprint('Staten Island Standard Deviation: ' + str(staten['obey'].std()))
pprint('NYC Overall Standard Deviation: ' + str(nyc_iq['obey'].std()))

# Adelaide
adelaide_iq = adelaide_registry.set_index('AnimalBreed').join(iq.set_index('Breed'), how='left')
pprint('Adelaide Dog IQ: ' + str(adelaide_iq['obey'].mean()))
pprint('Adelaide Standard Deviation: ' + str(adelaide_iq['obey'].std()))

# Edmonton
edmonton_iq = edmonton_registry.set_index('BREED').join(iq.set_index('Breed'), how='left')
pprint('Edmonton Dog IQ: ' + str(edmonton_iq['obey'].mean()))
pprint('Edmonton Standard Deviation: ' + str(edmonton_iq['obey'].std()))

# Which ancestral homeland has the smartest/most obedient dogs?

# For this analysis, we'll combine Scotland, Wales, and England as United Kingdom
ancestral = wiki[['Breed', 'Origin']]
ancestral['Origin'] = ancestral['Origin'].map(lambda x: 'United Kingdom' if x == 'England' or x == 'Wales' or x == 'Scotland' else x)
ancestral_iq = ancestral.set_index('Breed').join(iq.set_index('Breed'), how='inner')
# Take cells with multiple countries and split them into separate countries


def splitDataFrameList(df,target_column,separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
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


# pprint('Ancestral IQ: ' + str(staten['obey'].mean()))


# pprint(manhattan.count())
# pprint(staten.count())

# Sometimes centimeters are first and sometimes inches are first
# wiki['Height'] = wiki['Height'].apply(lambda x: re.search(r'\d+', x).group())

# pprint(nyc_registry.head())
# pprint(nyc_census.head())
# pprint(iq.head())
# pprint(edmonton_registry.head())
# pprint(adelaide_registry.head())
# pprint(wiki.head())
# nyc_registry.describe()

# Use fuzzing after exact match
# fuzz.ratio(