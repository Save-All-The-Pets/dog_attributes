from pprint import pprint
import pandas as pd
import numpy as np
from scipy import stats
import sys
from fuzzywuzzy import process
import matplotlib.pyplot as plt
import itertools
# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go
 
# f = open('key.pem', 'r')
# access_token = f.readline().strip('\n')
# plotly.tools.set_credentials_file(username='msuttles', api_key=access_token)
# plotly.tools.set_config_file(world_readable=False,
#                              sharing='private')

nyc_registry = pd.read_csv('dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
coren = pd.read_csv('dogdata/coren-edit.csv')
nyc_census = pd.read_csv('censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('dogdata/Dog_Registrations_Adelaide_2016-edit.csv')
wiki = pd.read_csv('dogdata/wiki-edit.csv')
turcsan = pd.read_csv('dogdata/turcsan.csv')

coren = coren[['Breed', 'Obedient']]
attrib = coren.set_index('Breed').join(turcsan.set_index('Breed'), how='outer')

lst = ['Calm', 'Trainable', 'Sociable', 'Bold', 'Obedient']

wiki_breeds = set(wiki['Breed'].tolist())
coren_breeds = set(coren['Breed'].tolist())
turcsan_breeds = set(turcsan['Breed'].tolist())

print('\nIntersection, Wiki and Turcsan')
print(wiki_breeds & turcsan_breeds)
print('\nIntersection, Wiki and Coren')
print(wiki_breeds & coren_breeds)

print('\nDifference, Wiki - Turcsan')
print(wiki_breeds - turcsan_breeds)
print('\nDifference, Turcsan - Wiki')
print(turcsan_breeds - wiki_breeds)
print('\nDifference, Wiki - Coren')
print(wiki_breeds - coren_breeds)
print('\nDifference, Coren - Wiki')
print(coren_breeds - wiki_breeds)

# comparison = wiki[['Breed']]
# comparison['Turcsan'] = comparison['Breed'].apply(lambda x: process.extractOne(x, list(turcsan_breeds)) if x not in turcsan_breeds else '')
# comparison['Coren'] = comparison['Breed'].apply(lambda x: process.extractOne(x, list(coren_breeds)) if x not in coren_breeds else '')
# comparison.to_csv('dogdata/comparisons.csv')


# Canine attributes by AKC Groupings
wiki_akc = wiki[['Breed', 'AKC']]
akc_groups_attrib = wiki_akc.set_index('Breed').join(attrib, how='left')
print('\nAKC Mean')
akc = akc_groups_attrib.groupby('AKC').mean().round(decimals=2)
pprint(akc)
print('\nAKC Standard Deviation')
akc_std = akc_groups_attrib.groupby('AKC').std().round(decimals=2)
pprint(akc_std)
akc_count = akc_groups_attrib.groupby('AKC').count()
pprint(akc_count)

fig, ax = plt.subplots()
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor') 
ax.plot(akc.index, akc['Bold'])
ax.plot(akc.index, akc['Calm'])
ax.plot(akc.index, akc['Obedient'])
ax.plot(akc.index, akc['Sociable'])
ax.plot(akc.index, akc['Trainable'])

plt.gcf().subplots_adjust(bottom=0.3, right=.75)
plt.legend(loc=(1.04,0.6))
plt.title('Scores by AKC Grouping')
ax.set_ylabel('Score')
ax.set_xlabel('AKC Grouping')
# plt.savefig('plots/akc.png')
plt.show()


# # Make the census columns understandable
# val = 'EST_'
# err = 'MOE_'
# age_under_5 = 'VC16'
# age_5_17 = 'VC17'; age_18_24 = 'VC18'
# age_25_34 = 'VC19'; age_35_44 = 'VC20'
# age_45_54 = 'VC21'; age_55_64 = 'VC22'
# age_65_74 = 'VC23'; age_75_over = 'VC24'

# Strip out dirty values
nyc_registry['Borough'] = nyc_registry['Borough'].map(lambda x: None if x not in {'Brooklyn', 'Bronx', 'Staten Island', 'Manhattan', 'Queens'} else x)
nyc_registry['BreedName'] = nyc_registry['BreedName'].map(lambda x: None if x == 'Unknown' else x)
nyc_registry.dropna(inplace=True)

nyc_attrib = nyc_registry.set_index('BreedName').join(attrib, how='left')
#nyc_attrib_t = nyc_registry.join(turcsan, how='left')
nyc_attrib = nyc_attrib[['Borough','Calm', 'Trainable', 'Sociable', 'Bold', 'Obedient']]
nyc_attrib_g = nyc_attrib.groupby('Borough')
print('\nNYC Mean:')
nyc_attrib_mean = nyc_attrib_g.mean()
pprint(nyc_attrib_mean.round(decimals=2))
print('\nNYC Standard Deviation:')
pprint(nyc_attrib_g.std().round(decimals=2))
print('\nNYC Count:')
pprint(nyc_attrib_g.count())

fig, ax = plt.subplots()
plt.xticks(rotation=45)
ax.plot(nyc_attrib_mean.index, nyc_attrib_mean['Bold'])
ax.plot(nyc_attrib_mean.index, nyc_attrib_mean['Calm'])
ax.plot(nyc_attrib_mean.index, nyc_attrib_mean['Obedient'])
ax.plot(nyc_attrib_mean.index, nyc_attrib_mean['Sociable'])
ax.plot(nyc_attrib_mean.index, nyc_attrib_mean['Trainable'])

plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor') 
plt.gcf().subplots_adjust(bottom=0.3, right=.75)
plt.legend(loc=(1.04,0.6))
plt.title('Scores by Borough in NYC')
ax.set_ylabel('Score')
ax.set_xlabel('Borough')
# plt.savefig('plots/borough.png')
plt.show()

nyc_breeds = nyc_registry[['Borough', 'BreedName']]
print('\nTop Dogs Count')
pprint(nyc_breeds['BreedName'].value_counts().nlargest(5))
nyc_breeds_grp = nyc_breeds.groupby('Borough')
# Most popular breeds by Borough
n = False # Whether or not to normalize values
print('\nTop Dogs By Borough')
print('\nManhattan')
print(nyc_breeds_grp.get_group('Manhattan')['BreedName'].value_counts(normalize=n).head(5))
print('\nQueens')
print(nyc_breeds_grp.get_group('Queens')['BreedName'].value_counts(normalize=n).head(5))
print('\nStaten Island')
print(nyc_breeds_grp.get_group('Staten Island')['BreedName'].value_counts(normalize=n).head(5))
print('\nBrooklyn')
print(nyc_breeds_grp.get_group('Brooklyn')['BreedName'].value_counts(normalize=n).head(5))
print('\nBronx')
print(nyc_breeds_grp.get_group('Bronx')['BreedName'].value_counts(normalize=n).head(5))


# NYC Overall 
plt.title('NYC Overall Attributes')
plt.ylabel('Score')
plt.xlabel('Attributes')
nyc_attrib_overall = nyc_attrib[lst]
nyc_attrib_overall = nyc_attrib.mean()
plt.bar(nyc_attrib_overall.index, nyc_attrib_overall.values)
plt.ylim([0,0.65])
plt.savefig('plots/nyc_overall.png')
plt.show()


# Perform Chi-Square analysis on NYC data
chi2_breed = ['Yorkshire Terrier', 'Shih Tzu','Chihuahua', 'Maltese', 'Labrador Retriever']
chi2_breed_com = itertools.combinations(chi2_breed, 2)

nyc_breeds_5 = nyc_registry[nyc_registry['BreedName'].isin(chi2_breed)] #top 5 breeds overall
for i in chi2_breed_com:
    print('\n',i)
    nyc_breeds_2 = nyc_registry[nyc_registry['BreedName'].isin(i)]
    contingency_table = pd.crosstab(nyc_breeds_2['BreedName'], nyc_breeds_2['Borough'])
    nyc_chi2 = stats.chi2_contingency(contingency_table)
    print('Test statistic: {}'.format(nyc_chi2[0].round(2)))
    print('P-value: {}'.format(nyc_chi2[1].round(4)))


# Adelaide
adelaide_attrib = adelaide_registry.set_index('AnimalBreed').join(attrib, how='left')
print('\nAdelaide Mean')
adelaide_attrib_mean = adelaide_attrib[lst].mean()
print(adelaide_attrib_mean.round(decimals=2))
print('\nAdelaide Standard Deviation')
print(adelaide_attrib[lst].std().round(decimals=2))

plt.title('Adelaide Overall Attributes')
plt.bar(adelaide_attrib_mean.index, adelaide_attrib_mean.values)
plt.ylim([0,0.65])
plt.savefig('plots/adelaide_overall.png')

plt.show()

# Edmonton
print('\nEdmonton Mean')
edmonton_attrib = edmonton_registry.set_index('BREED').join(attrib, how='left')
edmonton_attrib_mean = edmonton_attrib[lst].mean()
print(edmonton_attrib_mean.round(decimals=2))
print('\nEdmonton Standard Deviation')
print(edmonton_attrib[lst].std().round(decimals=2))

plt.title('Edmonton Overall Attributes')
plt.bar(edmonton_attrib_mean.index, edmonton_attrib_mean.values)
plt.ylim([0,0.65])
plt.savefig('plots/edmonton_overall.png')
plt.show()

ancestral = wiki[['Breed', 'Origin']]

# Looking at the UK and Ireland
ancestral_uk_ire = ancestral.copy()
ancestral_uk_ire.dropna(inplace=True)
ancestral_uk_ire = ancestral_uk_ire[ancestral_uk_ire['Origin'].isin(['England', 'Scotland', 'Wales', 'Ireland'])]
ancestral_uk_ire = ancestral_uk_ire.set_index('Breed').join(attrib, how='inner')
ancestral_uk_ire_grp = ancestral_uk_ire.groupby('Origin')
ancestral_uk_ire_mean = ancestral_uk_ire_grp.mean()
print('\nUK and Ireland Mean')
print(ancestral_uk_ire_grp.mean().round(decimals=2))
print('\nUK and Ireland Standard Deviation')
print(ancestral_uk_ire_grp.std().round(decimals=2))
print('\nUK and Ireland Count')
print(ancestral_uk_ire_grp.count())

fig, ax = plt.subplots()
plt.xticks(rotation=45)
ax.plot(ancestral_uk_ire_mean.index, ancestral_uk_ire_mean['Bold'])
ax.plot(ancestral_uk_ire_mean.index, ancestral_uk_ire_mean['Calm'])
ax.plot(ancestral_uk_ire_mean.index, ancestral_uk_ire_mean['Obedient'])
ax.plot(ancestral_uk_ire_mean.index, ancestral_uk_ire_mean['Sociable'])
ax.plot(ancestral_uk_ire_mean.index, ancestral_uk_ire_mean['Trainable'])

plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor') 
plt.gcf().subplots_adjust(bottom=0.3, right=.75)
plt.legend(loc=(1.04,0.6))
plt.title('Scores by UK and Irish Ancestry')
ax.set_ylabel('Score')
ax.set_xlabel('Territory')
plt.savefig('plots/uk_ireland.png')
plt.show()

# Combining Scotland, Wales, and England as United Kingdom
ancestral['Origin'] = ancestral['Origin'].map(lambda x: 'United Kingdom' if x in {'England', 'Wales', 'Scotland'} else x)
ancestral_attrib = ancestral.set_index('Breed').join(attrib, how='inner')

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

fig, ax = plt.subplots()
# pprint(ancestral_attrib_mean_filtered.index)
plt.xticks(rotation=45)
ax.plot(ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Bold'])
ax.plot(ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Calm'])
ax.plot(ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Obedient'])
ax.plot(ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Sociable'])
ax.plot(ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Trainable'])

plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor') 
plt.gcf().subplots_adjust(bottom=0.3, right=.75)
plt.legend(loc=(1.04,0.6))
plt.title('Scores by Country of Ancestry')
ax.set_ylabel('Score')
ax.set_xlabel('Country')
# plt.savefig('plots/ancestry.png')
plt.show()

# data = [ancestral_attrib_mean_filtered.index, ancestral_attrib_mean_filtered['Bold']]
# py.plot(data, filename = 'basic-line', auto_open=True)