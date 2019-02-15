
import pandas as pd


# Generate the URLS on Wikipedia for each dog breed
base_url = 'https://en.wikipedia.org/wiki/'
akc_breeds_info = pd.read_csv('dogdata/akc_breed_info_clean.csv')
breed = akc_breeds_info['Breed']
urls = []

f = open('dogdata/urls.txt','w')
for i in breed:
    f.write(base_url + i.replace(' ','_') + '\n')
f.close()
