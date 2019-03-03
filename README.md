# Study Design

This study explores dog registration record data from NYC, Edmonton, and Adelaide and combines this data with data about particular attributes of dogs (for example, how bold or trainable they are.) In this study, I'm negotiating the line between making this data publicly accessible (and fun) and ensuring I'm applying analytic rigor. While this study won't be published in an academic journal, I'm transparently including my code and datasets so that those interested can tweak them and discover their own trends.

## Variables evaluated

I performed a Chi-square test to determine if a person's borough is statistically relevant to what type of dog that person owns. I performed the test at the 0.05 significance level. The null hypothesis was that a person's borough does not have a statistically significant relationship with the type of dog he or she owns. I tested this hypothesis for the top 5 dogs in NYC, and found that certain dogs have a statistically significant relationship with the owner's borough. For example, ...

## Results

<!-- For much more on this, please visit [Doggiedatazone.com](http://doggiedatazone.com) -->
![AKC Data](plots/akc.png)

## For future study

There's much more to explore with this data. I may take a stab at some of the following, but others are also welcome to join in:

* New York voter registration information is public, so it might be interesting to correlate what kinds of dogs Republicans, Democrats, and Independent voters prefer.

* Academics have already looked at genetic markers, but it might be interesting to look at genetic markers by location.

* I did not disaggregate German dogs, so it might be interesting to look at aspects of German dogs (perhaps where in Germany they are from ancestrally) to see if there is more of interest.

* I did not dig into census data, including the census tract-level statistics for NYC.

## Note on the code

This code should be ready to use; you can edit/run `analysis.py` from the `src` directory. In another file, I used the  fuzzing add-on `fuzzywuzzy`. You can run the `src/analysis-fuzzy.py` file, but you may need to install fuzzywuzzy by typing `pip install fuzzywuzzy[speedup]`.

## Sources

[City of Adelaide Dog Registrations](https://data.gov.au/dataset/ds-sa-8aa33af5-4146-447e-b9e9-0c00b616cd38/details)

[NYC Dog Licensing Dataset](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp)

[Seattle Pet Licenses](https://catalog.data.gov/dataset/seattle-pet-licenses)

[Edmonton Dog Licenses Dataset](https://data.edmonton.ca/Community-Services/Pet-Licenses-by-Neighbourhood/5squ-mg4w)

[Data on canine intelligence](https://data.world/len/intelligence-of-dogs) by Stanley Coren and others

[Trainability and boldness traits differ between dog breed clusters based on conventional breed categories and genetic relatedness](https://www.researchgate.net/publication/228485434_Trainability_and_boldness_traits_differ_between_dog_breed_clusters_based_on_conventional_breed_categories_and_genetic_relatedness) by Borbála Turcsán, Enikő Kubinyi, Ádám Miklósi

Further research on dogs in the UK: [Estimation of the number and demographics of companion dogs in the UK](https://bmcvetres.biomedcentral.com/articles/10.1186/1746-6148-7-74) by Lucy Asher, Emma L Buckland, C Ianthi Phylactopoulos, Martin C Whiting, Siobhan M Abeyesinghe and Christopher M Wathes

## Notes on the data

Staten Island census data is unavailable
For lowest category of dog intelligence, "obey" was not specified. I am assigning a value of 0.10
Edmonton had almost no data for 2016 and very little for 2017, so I'm using 2018 data.
For further research, someone could use the census tract data in the NYC dataset.
Pulling data from Wikipedia, of course, allows for a small margin of error in the data; however, the data is usually accurate.
Terriers and Toy Terriers were treated as Terriers and Toys in the AKC rankings.
American/English Cocker Spaniel
Compliance could affect the data; certain dog owners may be less likely to register their dogs even though it's required in all three localities.
Mixed breeds were not categorized, and were thus excluded.
Dogs were double-counted for origin.

## Contact the author

Please direct any correspondence to Michael Suttles at: git at mgs.33mail.com.