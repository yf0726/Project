import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from os import walk
import numpy as np

"""

Below is the code for data extraction from `www.foodnetwork.com` with additional helper functions. 
We infer information which includes the name of the dish, preparation time, ratings and reviews, the ingredients and 
directions for preparation. We save all features in different Pandas dataframes for 
easier comparison and analysis and as well we create a Pandas dataframe which contains 
every information gathered from `www.foodnetwork.com`.

"""


def normalize_string(string):
    """
    Function to clean a given string.
    
    Parameters: 
        string: string
        
    Return:
        formatted string
    """
    return re.sub(r'\s+', ' ', string.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ').strip())


def get_minutes(element):
    """        
    Function to get minutes from time element accoring to the regex expression.
    
    Parameters: 
        element: string
        
    Return:
        int minutes of the element
    """
    
    TIME_REGEX = re.compile(
        r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M))?')

    try:
        tstring = element.get_text()
        if '-' in tstring:
            tstring = tstring.split('-')[1]  # sometimes formats are like this: '12-15 minutes'
        matched = TIME_REGEX.search(tstring)

        minutes = int(matched.groupdict().get('minutes') or 0)
        minutes += 60 * int(matched.groupdict().get('hours') or 0)

        return minutes
    except AttributeError:  # if dom_element not found or no matched
        return 0


rating_review_list, times_list, ingredient_list, direction_list, done_list, null = ([] for i in range(7))
count=0

# Extract data from foodnetwork.com HTML files
File_Folder = 'www.foodnetwork.com'
for root, _, files in walk(File_Folder):
    for name in files:
        if name in done_list:
            print('The file has been scrapped.')
            continue
        soup_i = BeautifulSoup(open(FOLDER_PATH + name, 'rb'), 'html.parser')
        if soup_i.findAll('a'):    # make sure there is no blank HTML
            if ('http://www.foodnetwork.com/recipes/' in soup_i.text and soup_i.find("meta", property="og:title")): # make sure the page is for recipe
                title = soup_i.find("meta", property="og:title")['content']
                html = name
                
                if soup_i.find('div',class_="rm-block lead hreview-aggregate review"):
                    rating_tmp = re.findall(r'Rated (\d+) stars', soup_i.find('div',class_="rm-block lead hreview-aggregate review").text)
                else:
                    rating_tmp = []
                                  
                if soup_i.findAll('span', {'class':"lgbtn-text"}):
                    review_tmp = re.findall('(\d+)',soup_i.findAll('span', {'class':"lgbtn-text"})[1].text)
                else:
                    review_tmp = []
                
                rating_review_list.append({ 'Title': title,
                                            'Rating': float(re.findall(r'Rated (\d+) stars', soup_i.find('div',class_="rm-block lead hreview-aggregate review").text)[0])\
                                                      if rating_tmp else np.nan
                                            'Reviews': int(re.findall('(\d+)',soup_i.findAll('span', {'class':"lgbtn-text"})[1].text)[0])\
                                                       if review_tmp else np.nan
                
                if soup_i.find('dd',class_="head duration clrfix"):
                    Total_time = get_minutes(soup_i.find('dd',class_="head duration clrfix"))
                else:
                    Total_time = np.nan
                    
                if soup_i.find('dd',class_="cookTime clrfix"):
                    cook_time = get_minutes(soup_i.find('dd',class_="cookTime clrfix"))
                else:
                    cook_time = []
                
                if soup_i.find('dd',class_="prepTime clrfix"):
                    prep_time = get_minutes(soup_i.find('dd',class_="prepTime clrfix"))
                else:
                    prep_time = []
                    
                times_list.append({ 'Title': title,
                                    'Total Time (min)': Total_time,
                                    'Prep Time (min)': prep_time,
                                    'Cook Time (min)': cook_time,
                                           
                ingredients = soup_i.findAll('li', {'class': 'ingredient'})
                ingredient_list.append({'Title': title,
                                        'Ingredient': [normalize_string(ingredient.get_text()) for ingredient in ingredients]\
                                                      if ingredients else np.nan
                                       }) 
                
                directions = soup_i.findAll('div', class_="instructions")
                direction_list.append({'Title': title,
                                       'Direction': [normalize_string(direction.get_text()) for direction in directions]\
                                                    if directions else np.nan
                                      })
                
            else:
                null.append(name)
                print(count, name, 'not recipe pages')
        else:
            null_list.append(name)
            print(count, name, 'null pages')
        done_list.append(name)
        count+=1


# Save reviews and ratings list in Pandas dataframe
pd.DataFrame(rating_review_list).to_csv('rating_review_foodnetwork.csv')

# Save cooking times list in Pandas dataframe
pd.DataFrame(times_list).to_csv('cooking_time_foodnetwork.csv')

# Save ingredient list in Pandas dataframe
pd.DataFrame(ingredient_list).to_csv('ingredient_list_foodnetwork.csv')

# Save directions list in Pandas dataframe
pd.DataFrame(direction_list).to_csv('direction_list_foodnetwork.csv')

# Save list of all HTML files names in Pandas dataframe
pd.DataFrame(done_list).to_csv('files_foodnetwork.csv')

# Save list of all invalid HTML files names in Pandas dataframe
pd.DataFrame(null).to_csv('null_foodnetwork.csv')

# Save Pandas dataframe with all information
foodnetwork_df = pd.DataFrame(rating_review_list).merge(pd.DataFrame(times_list)).merge(pd.DataFrame(ingredient_list)).merge(pd.DataFrame(direction_list))
cols = list(foodnetwork_df)
cols.insert(0, cols.pop(cols.index('Title')))
foodnetwork_df = foodnetwork_df.loc[:, cols]
foodnetwork_df.drop_duplicates(subset=['Title'], inplace=True)
foodnetwork_df.reset_index(inplace=True)
foodnetwork_df.drop(columns='index', inplace=True)
foodnetwork_df.to_csv('foodnetwork_df.csv')