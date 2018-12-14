# Title

Title: Unveiling ingredient combinations

Team members: Yan Fu, Kristijan Lopatichki, Zhechen Su

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

# Pipeline
(https://raw.githubusercontent.com/sting1000/img/master/Pipeline%20of%20Project%20Milestone%202.png)

# The structure of repo

Master Branch
1. Input data: .csv files used for data analysis.
2. Scripts: allrecipes_parsing.py, food_parsing.py, foodnetwork_parsing.py, move_webpages_to_folders.py, yummly_parsing.py, scripts used for webscraping and visualization.
3. FINALNOTEBOOK.ipynb: The final notebook for this project.

# Contribution of Groupmember
Yan Fu: web scraping (foodnetwork), WHO dataset analysis and visualization
Kristijan Lopatichki: 
Zhechen Su: 
