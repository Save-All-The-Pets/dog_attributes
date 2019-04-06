# Study Design

This study explores dog registration record data from NYC, Seattle, Edmonton, and Adelaide and combines this data with data about particular attributes of dogs (bold, trainable, calm, sociable, and obedient). I look at the attributes according to the AKC grouping the dog is in, its location (by city and for New York, by borough), and the ancestral origin for the dog. I use the Tukey statistical test to compare the means of the dog attributes by New York borough and by city. I also perform hypothesis tests on particular aspects of the data.

## Running the code

This code should be ready to use; the Jupyter Notebook file `analysis.ipynb` is in the `src` directory. Data cleaning was performed on the original datasets in order to ensure consistency. All data is in the `data` directory.
<!-- In another file, I used the  fuzzing add-on `fuzzywuzzy`. You can run the `src/analysis-fuzzy.py` file, but you may need to install fuzzywuzzy by typing `pip install fuzzywuzzy[speedup]`. -->

## For future study

There's much more to explore with this data. I plan to undertake some of the following analyses at a later date:

* Voter registration information is public, so it might be interesting to correlate what kinds of dogs Republicans, Democrats, and Independent voters prefer.

* Academics have already looked at genetic markers, but it might be interesting to look at genetic markers by location.

* I did not dig into census data, including the census tract-level statistics for NYC.

* I did not look at neighborhood-level (zip code) results.

## Sources

[City of Adelaide Dog Registrations](https://data.gov.au/dataset/ds-sa-8aa33af5-4146-447e-b9e9-0c00b616cd38/details)

[NYC Dog Licensing Dataset](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp)

[Seattle Pet Licenses](https://data.seattle.gov/Community/Seattle-Pet-Licenses/jguv-t9rb)

[Edmonton Dog Licenses Dataset](https://data.edmonton.ca/Community-Services/Pet-Licenses-by-Neighbourhood/5squ-mg4w)

[Data on canine intelligence](https://data.world/len/intelligence-of-dogs) by Stanley Coren and others

[Trainability and boldness traits differ between dog breed clusters based on conventional breed categories and genetic relatedness](https://www.researchgate.net/publication/228485434_Trainability_and_boldness_traits_differ_between_dog_breed_clusters_based_on_conventional_breed_categories_and_genetic_relatedness) by Borbála Turcsán, Enikő Kubinyi, Ádám Miklósi

<!-- Further research on dogs in the UK: [Estimation of the number and demographics of companion dogs in the UK](https://bmcvetres.biomedcentral.com/articles/10.1186/1746-6148-7-74) by Lucy Asher, Emma L Buckland, C Ianthi Phylactopoulos, Martin C Whiting, Siobhan M Abeyesinghe and Christopher M Wathes -->
