#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

import warnings
warnings.filterwarnings('ignore')

# pd.options.display.max_rows = 999

# Import the data
nyc_registry = pd.read_csv('../dogdata/NYC_Dog_Licensing_Dataset_2016-edit.csv')
coren = pd.read_csv('../dogdata/coren-edit.csv')
nyc_census = pd.read_csv('../censusdata/ACS_16_1YR_S0201_with_ann-edit.csv') # use 2016 data
edmonton_registry = pd.read_csv('../dogdata/Edmonton_Pet_Licenses_by_Neighbourhood_2018-edit.csv')
adelaide_registry = pd.read_csv('../dogdata/Dog_Registrations_Adelaide_2016-edit.csv')
seattle_registry = pd.read_csv('../dogdata/Seattle_Pet_Licenses-2018-edit2.csv')
wiki = pd.read_csv('../dogdata/wiki-edit.csv')
turcsan = pd.read_csv('../dogdata/turcsan.csv')

# List of attributes
lst = ['Bold', 'Calm', 'Obedient','Sociable', 'Trainable']
borough = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
# Pare down the Coren data
coren = coren[['Breed', 'Obedient']]
# Combine the Coren and Turcsan datasets
attrib = coren.set_index('Breed').join(turcsan.set_index('Breed'), how='outer')


def describe(df, categ, filename=None, display=True):
    """Show the mean and standard deviation of the data and optionally plot. Optionally save a file of the plot.
    
    Arguments:
        df {DataFrame} -- DataFrame to describe
        categ {str} -- Display category
    
    Keyword Arguments:
        filename {str} -- Name of file to save to (default: {None})
        display {bool} -- Whether or not to display a plot (default: {True})
    """
    print('\n'+categ+' Mean')
    attrib_mean = df[lst].mean()
    print(attrib_mean.round(decimals=2))
    print('\n'+categ+' Standard Deviation')
    print(attrib[lst].std().round(decimals=2))

    plt.title(categ+' Overall Attributes')
    plt.bar(attrib_mean.index, attrib_mean.values)
    plt.ylim([0,0.75])
    if filename is not None:
        plt.savefig('../plots/'+filename)
    if display:
        plt.show()

def describe_breeds(save=False):
    '''Show the intersection of different breeds of dogs according to which dataset they come from. For example, Dogue de Bordeaux is in the Turcsan set but not in the Wiki scraped set.

    Returns:
        None
    '''
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

def plot_by_attrib(df, categ,label, filename=None, display=True):
    """Plot a graph by the attributes provided.
    
    Arguments:
        df {DataFrame} -- DF to plot
        categ {list} -- Categories to plot
        label {str} -- Label for what the data is describing
    
    Keyword Arguments:
        filename {str} -- Name of the file to optionally save (default: {None})
        display {bool} -- Whether or not to display the plot (default: {True})
    """
    fig, ax = plt.subplots()
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor')
    for item in categ:
        ax.plot(df.index, df[item])

    plt.gcf().subplots_adjust(bottom=0.3, right=.75)
    plt.legend(loc=(1.04,0.6))
    plt.title('Scores by '+ label)
    ax.set_ylabel('Score')
    ax.set_xlabel(label)
    if filename is not None:
        plt.savefig('../plots/'+filename)
    if display:
        plt.show()


def splitDataFrameList(df,target_column,separator):
    """Thanks to James Allen, https://gist.github.com/jlln/338b4b0b55bd6984f883
    
    Arguments:
        df {DataFrame} -- DataFrame to split,
        target_column {string} -- The column containing the values to split
        separator {str} -- The symbol used to perform the split
    
    Returns:
        DataFrame -- A dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    """
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


# In[2]:


# Show which dogs are in each dataset.
describe_breeds()


# In[3]:


# Canine attributes by AKC groupings
wiki_akc = wiki[['Breed', 'AKC']]
akc_groups_attrib = wiki_akc.set_index('Breed').join(attrib, how='left')
print('\nAKC Mean')
akc = akc_groups_attrib.groupby('AKC').mean().round(decimals=2)
pprint(akc)
print('\nAKC Standard Deviation')
akc_std = akc_groups_attrib.groupby('AKC').std().round(decimals=2)
pprint(akc_std)
print('\nAKC Count')
akc_count = akc_groups_attrib.groupby('AKC').count()
pprint(akc_count)

# Plot the AKC grouping data
plot_by_attrib(akc, lst, 'AKC Grouping')


# In[4]:


# Strip out NYC dirty values
nyc_registry['Borough'] = nyc_registry['Borough'].map(lambda x: None if x not in {'Brooklyn', 'Bronx', 'Staten Island', 'Manhattan', 'Queens'} else x)
nyc_registry['BreedName'] = nyc_registry['BreedName'].map(lambda x: None if x == 'Unknown' else x)
nyc_registry.dropna(inplace=True)

# Display breed attributes by NYC borough
display = False
norm=False # Do not normalize
nyc_attrib = nyc_registry.set_index('BreedName').join(attrib, how='left')
nyc_attrib = nyc_attrib[['Borough','Calm', 'Trainable', 'Sociable', 'Bold', 'Obedient']]
nyc_attrib_g = nyc_attrib.groupby('Borough')
print('\nNYC Mean:')
nyc_attrib_g_mean = nyc_attrib_g.mean()
pprint(nyc_attrib_g_mean.round(decimals=2))
print('\nNYC Standard Deviation:')
pprint(nyc_attrib_g.std().round(decimals=2))
print('\nNYC Count:')
pprint(nyc_attrib_g.count())
if display:
    plot_by_attrib(nyc_attrib_g_mean, lst, 'NYC Borough')

nyc_breeds = nyc_registry[['Borough', 'BreedName']]
print('\nTop NYC Dogs Count')
pprint(nyc_breeds['BreedName'].value_counts().nlargest(5))
nyc_breeds_grp = nyc_breeds.groupby('Borough')
print('\nTop Dogs By Borough')
for b in borough:
    print('\n'+b)
    print(nyc_breeds_grp.get_group(b)['BreedName'].value_counts(normalize=norm).head(5))


# In[5]:


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
    print('P-value: {}'.format(nyc_chi2[1]))


# In[6]:


# Perform t-tests on NYC data
print('Alternative Hypothesis: dogs from Staten Island are bolder than other dogs in New York.')

non_staten = nyc_attrib[nyc_attrib['Borough'].isin(['Manhattan', 'Queens', 'Bronx', 'Brooklyn'])]
non_staten.dropna(inplace=True)
non_staten_bold = non_staten['Bold']
staten = nyc_attrib[nyc_attrib['Borough'] == 'Staten Island']
staten.dropna(inplace=True)
staten_bold = staten['Bold']
print(stats.ttest_ind(staten_bold, non_staten_bold, equal_var = False))

print('Alternative Hypothesis: dogs from Staten Island are calmer than other dogs in New York.')
non_staten_calm = non_staten['Calm']
staten_calm = staten['Calm']
print(stats.ttest_ind(staten_calm, non_staten_calm, equal_var = False))

## MORE
print('Alternative Hypothesis: dogs from New York are bolder than dogs in Adelaide and Edmonton.')
adelaide_attrib = adelaide_registry.set_index('AnimalBreed').join(attrib, how='left')
edmonton_attrib = edmonton_registry.set_index('BREED').join(attrib, how='left')
seattle_attrib = seattle_registry.set_index('Primary Breed').join(attrib, how='left')
nyc_bold = nyc_attrib['Bold']
nyc_bold.dropna(inplace=True)
ad_ed_attrib = pd.concat([adelaide_attrib, edmonton_attrib])
ad_ed_bold = ad_ed_attrib['Bold']
ad_ed_bold.dropna(inplace=True)
print(stats.ttest_ind(nyc_bold, ad_ed_bold, equal_var = False))

print('Alternative Hypothesis: dogs from Edmonton are more obedient than dogs\n in Adelaide and New York.')
nyc_obedient = nyc_attrib['Obedient']
nyc_obedient.dropna(inplace=True)
ad_ed_obedient = ad_ed_attrib['Obedient']
ad_ed_obedient.dropna(inplace=True)
print(ad_ed_obedient.value_counts())
print(stats.ttest_ind(nyc_obedient, ad_ed_obedient, equal_var = False))


# In[7]:


# Show data on NYC, Seattle, Adelaide, and Edmonton
describe(nyc_attrib, 'NYC')
describe(seattle_attrib, 'Seattle')
describe(adelaide_attrib, 'Adelaide')
describe(edmonton_attrib, 'Edmonton')

adelaide_mean = adelaide_attrib[lst].mean()
edmonton_mean = edmonton_attrib[lst].mean()
nyc_mean = nyc_attrib[lst].mean()


# In[8]:


#3D Plot
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
xs = np.arange(5)
ys = adelaide_mean.values
cs = 'r' * 5
ax1.bar(xs, ys, zs=3, zdir='y', color=cs, alpha=0.8)
ys = edmonton_mean.values
cs = 'g' * 5
ax1.bar(xs, ys, zs=2, zdir='y', color=cs, alpha=0.8 )
ys = nyc_mean.values
cs = 'b' * 5
ax1.bar(xs, ys, zs=1, zdir='y', color=cs, alpha=0.8)

ax1.w_xaxis.set_ticklabels(lst)
ax1.w_yaxis.set_ticklabels(['Adelaide','Edmonton','NYC'])

plt.show()


# In[9]:


# Looking at the UK and Ireland
ancestral = wiki[['Breed', 'Origin']]
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

# Plot the UK and Ireland data
# Remove Wales since it only has one dog for some of the data
ancestral_uk_ire_mean.drop('Wales', inplace=True)
plot_by_attrib(ancestral_uk_ire_mean, lst, 'UK and Irish Ancestry')

# Combining Scotland, Wales, and England as United Kingdom
ancestral['Origin'] = ancestral['Origin'].map(lambda x: 'United Kingdom' if x in {'England', 'Wales', 'Scotland'} else x)
ancestral_attrib = ancestral.set_index('Breed').join(attrib, how='inner')

# Show data on attributes of dogs given their ancestral home
ancestral_attrib.dropna(inplace=True)
ancestral_attrib2 = splitDataFrameList(ancestral_attrib,'Origin', '/')
ancestral_attrib2['Origin'] = ancestral_attrib2['Origin'].map(lambda x: 'China' if x == 'Tibet (China)' else x)
ancestral_attrib_grp = ancestral_attrib2.groupby('Origin')
ancestral_attrib_count = ancestral_attrib_grp.count()
ancestral_attrib_mean = ancestral_attrib_grp.mean().round(decimals=2)
ancestral_attrib_std = ancestral_attrib_grp.std().round(decimals=2)

# Only display values where there are more than two dogs
ancestral_attrib_mean_filtered = ancestral_attrib_mean[ancestral_attrib_count['Bold'] > 2]
ancestral_attrib_std_filtered = ancestral_attrib_std[ancestral_attrib_count['Bold'] > 2]

print('\nAncestral Origin Mean, n>2')
pprint(ancestral_attrib_mean_filtered)
print('\nAncestral Origin Standard Deviation')
pprint(ancestral_attrib_std_filtered)
print('\nAncestral Origin Count')
pprint(ancestral_attrib_count)

# Plot by country of origin
plot_by_attrib(ancestral_attrib_mean_filtered, lst, 'Country of Origin')


# In[10]:


print('Alternative Hypothesis: Dogs with ancestry from the UK are bolder than other dogs.')
ancestral_uk = ancestral_attrib2[ancestral_attrib2['Origin'] == 'United Kingdom']
ancestral_not_uk = ancestral_attrib2[~(ancestral_attrib2['Origin'] == 'United Kingdom')]
ancestral_uk_bold = ancestral_uk['Bold']
print('Ancestral UK Bold Mean:')
print(ancestral_uk_bold.mean())
ancestral_uk_bold.dropna(inplace=True)
ancestral_not_uk_bold = ancestral_not_uk['Bold']
ancestral_not_uk_bold.dropna(inplace=True)
print('Ancestral Non-UK Bold Mean:')
print(ancestral_not_uk_bold.mean())
print(stats.ttest_ind(ancestral_uk_bold, ancestral_not_uk_bold, equal_var = False))


# In[11]:


print('Null Hypothesis: The average obedience of UK dogs is the same as non-UK dogs.')
print('Alternative Hypothesis: The average obedience of UK dogs is different from non-UK dogs.')
ancestral_uk_obedient = ancestral_uk['Obedient']
ancestral_not_uk_obedient = ancestral_not_uk['Obedient']
print(stats.ttest_ind(ancestral_uk_obedient, ancestral_not_uk_obedient, equal_var = False))


# ## German dogs

# In[12]:


print('Alternative Hypothesis: Dogs with German ancestry are more obedient than other dogs.')
ancestral_ger = ancestral_attrib2[ancestral_attrib2['Origin'] == 'Germany']
ancestral_not_ger = ancestral_attrib2[~(ancestral_attrib2['Origin'] == 'Germany')]
ancestral_ger_obedient = ancestral_ger['Obedient']
print('Ancestral Germany Obedient Mean:')
print(ancestral_ger_obedient.mean())
ancestral_ger_obedient.dropna(inplace=True)
ancestral_not_ger_obedient = ancestral_not_ger['Obedient']
ancestral_not_ger_obedient.dropna(inplace=True)
print('Ancestral Non-Germany Obedient Mean:')
print(ancestral_not_ger_obedient.mean())
print(stats.ttest_ind(ancestral_ger_obedient, ancestral_not_ger_obedient, equal_var = False))


# In[13]:


print('Alternative Hypothesis: Dogs with German ancestry are less calm than other dogs.')
ancestral_ger_calm = ancestral_ger['Calm']
print('Ancestral Germany Calm Mean:')
print(ancestral_ger_calm.mean())
ancestral_ger_calm.dropna(inplace=True)
ancestral_not_ger_calm = ancestral_not_ger['Calm']
ancestral_not_ger_calm.dropna(inplace=True)
print('Ancestral Non-Germany Calm Mean:')
print(ancestral_not_ger_calm.mean())
print(stats.ttest_ind(ancestral_ger_calm, ancestral_not_ger_calm, equal_var = False))


# In[ ]:




