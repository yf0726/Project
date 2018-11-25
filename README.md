# Title

Title: Unveiling ingredient combinations

Team members: Yan Fu, Kristijan Lopatichki, Zhechen Su

---

# Update for Milestone2


# The structure of repo

Master Branch
1. Input data: allrecipes_df.csv, food_df.csv, foodnetwork_df.csv, TotalHtml2Page.csv, yummly_df.csv 
2. Parsing scripts: allrecipes_parsing.py, food_parsing.py, foodnetwork_parsing.py, move_webpages_to_folders.py, yummly_parsing.py
3. Milestone_2.ipynb


`Input data` folder includes datasets we download and extract through `.py` scripts in Parsing scripts;

`Parsing scripts` folder includes one preprocessing and four web scraping script code with comments. We put them together to make our notebook clear and make more space for analysis;

`Milestone_2.ipynb` clean and analyze data we have and thus show our way to implement the data in ML3.


# Pipeline of ML2
![Pipeline of ML2](https://raw.githubusercontent.com/sting1000/img/master/Pipeline%20of%20Project%20Milestone%202.png)

# What's next

1. Ingredient pairs
After having a view of ingredients, we need to think about how to define pairs of ingredients. The ingredient should be the key ingredients in each recipe, for instance in `Chicken Curry Pasta`, ingredient pairs are (chicken, potato), (potato, pasta), (chicken, pasta). Based on this particular stucture which is quite similar to human society, we are going to import `NLTK`, a Natural Language Toolkit or `pyvis.network` to build the network of ingredients. And according to the results, we will analyze the cluster and relation to recipe/region/health. 

2. Regional Differences
By analyzing the ingredient of regional recipes, we found out that key ingredients vary a lot. For example in Chinese cuisine, the three most common used items are soy sauce, ginger and garlic. In France, however, the top three ingredients are butter, salt and milk. Such big difference in ingredients makes cooking methods various as well as nutrition features. As a result recipes appear in thousands of patterns. With the help of regional difference, we can explore people's eating habits and preferences. Is ingredient-based relationship geographical, climatic or cultural?

3. Relate to Health
After having a conlusion about regional cuisine difference, we want to know if a relationship exists between recipes and health for a certain region. Threfore, it is necessary to measure how healthy some repcipes are. It should be intuitive and take into account the main aspects of nutrition to discover this. 

We import the Nutri-Score presented by OpenFood. It is a system of notes from A(good) to E(bad) on the front of food products to allow for a simple comparison of the nutritional quality of products. [This website](https://fr.openfoodfacts.org/score-nutritionnel-experimental-france) shows details about formula for calculating the nutritional score, the thresholds of the notes and various adaptation proposals. The advantage is that it's very easy to understand for a customer who has no knowledge in nutrition.

---


# Abstract

Food is nothing less than an essential part of life and a major global economic force. Different cuisines use different ingredients and sometimes certain pairs of ingredients have really high frequency in worldwide recipes. We want to explore the traditional pairings we know, while also revealing non-traditional and surprising combinations in different cuisines through our analysis. 

In this project, we define ‘key ingredient’ as the most commonly used ingredient; and ‘ingredient combination’ as pairs of ingredients that are always used together. We investigate on popularity of recipes and cooking methods and ingredient combinations to know more food characteristics. These characteristics are not only interesting, but they also provide us with a new perspective on food patterns which is closely related to public health, revealing the possible relationship between food ingredients and public health data.

Mainly we are going to use three data sets: `cooking recipe`, `open food dataset` and `Global Health Observatory data repository`. We can obtain recipe ingredients, cooking methods, countries and regional health data from these data sets and our analysis will be based on them.

# Research questions

* What are the most popular recipes? Do popular cuisines have special preference on cooking method, ingredients or preparation time?

* What are the key ingredients for different cuisines and recipes? 

* Does ingredient-based relationship (similarity or dissimilarity) exist between various regional cuisines? If it does, could it be geographical, climatic or cultural? 

* Can we find a relationship between regional ingredients and public health data?


# Dataset

In this project, we decide to use `cooking recipes` as our main dataset, and we will also combine the data from `open food dataset` and `Global Health Observatory data repository`. 

Cooking recipe: 2.53 GB of zipped data and concludes more than 93,000 html web pages on recipes. From each web page we infer information which includes the name of the dish, preparation time, the ingredients, directions for preparation and nutritional facts. Also, we notice the number of reviews differ between recipes, and we think we can use the number of reviews as a proof for popularity.

http://infolab.stanford.edu/~west1/from-cookies-to-cooks/recipePages.zip

Open food dataset: 1.6 GB in csv format. Open Food Facts is a free and open dataset gathering information and data on food products from around the world. We can find the name of a product, ingredients, countries and also nutrition facts. We use the open food dataset when we want to know the country of certain recipes from Cooking recipe dataset as well as the basic information of each ingredient in recipes. 

https://world.openfoodfacts.org/data

Global Health Observatory data repository from WHO: The global health observatory data repository is very comprehensive and it includes data sets on various perspectives, including statistics from all countries on non communicable disease (NCD), prevalence of obesity, raised blood pressure and raised cholesterol etc. These data sets can be downloaded in .csv format or json format. 

http://apps.who.int/gho/data/node.home

Through combining the information from these datasets, we can obtain ingredients, culinary techniques, nutritional facts, popularity and geographical distribution of cuisines worldwide. And with the dataset from WHO, we can even go further to analyze the possible relationship between recipes and public health.

# A list of internal milestones up until project milestone 2

`2018.11.04 - 2018.11.11` 
Collect and clean data from datasets. Discard numerous invalid HTML addresses and redundant data in the datasets. We will proceed by extracting useful information and then we will display the information in dataframe through Pandas. Data exploratory will help us define what kind of data we have and what can we infer from it. With these information we obtain, we will assess our questions in Milestone 1 again and adjust them if necessary. Also we should define how to calculate popularity from all information we have.

`2018.11.12 - 2018.11.19`
Analyze and organize data structure. In this part, we are going to enrich, filter, transform the data according to our needs and explore the inner correlation between variables. Show our raw results in proper plot, which can help us make variables’ relationship clear. Then, according to the results, we could make different tables to keep categorized data like Nutrition, Popularity, Cooking Method etc.
  
`2018.11.20 - 2018.11.25 `
Create future plan in notebook. Review and check the work we have done. Discuss the methods and write the specific structure of functions we need to use next. Comment them then make a clear target we are going to achieve at the end.
