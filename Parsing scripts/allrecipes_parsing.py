import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from os import walk
import numpy as np

"""

Below is the code for data extraction from `allrecipes.com` with additional helper functions. 
We infer information which includes the name of the dish, preparation time, ratings and reviews, the ingredients, 
directions for preparation and nutritional facts. We save all features in different Pandas dataframes for 
easier comparison and analysis and as well we create a Pandas dataframe which contains 
every information gathered from `allrecipes.com`.

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


def to_Mg(text):
    """
    Function to extract number from text and convert units from `g` to `mg`: 3.3g to mg
    
    Parameters: 
        text: string
        
    Return:
        float of extracted number in unit `mg` or np.nan when the unit is unapropriate
    """
    reg = re.match(r'([0-9\.,]+)\s*(g|grams|mg|milligrams)', text)
    if reg:
        num = reg.group(1)
        unit = reg.group(2)
        factor = 1 if ((unit == 'mg') or (unit == 'milligrams')) else 1000
        return float(num) * factor
    else:
        return np.nan


def to_g(text):
    """        
    Function to extract number from text and convert units from `mg` to `g`: 3.3mg to g
    
    Parameters: 
        text: string
        
    Return:
        float of extracted number in unit `g` or np.nan when the unit is unapropriate
    """
    reg = re.match(r'([0-9\.,]+)\s*(g|grams|mg|milligrams)', text)
    if reg:
        num = reg.group(1)
        unit = reg.group(2)
        factor = 1 if ((unit == 'g') or (unit == 'grams')) else 1000
        return float(num) / factor
    else:
        return np.nan


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


nutrition_list, rating_review_list, times_list, ingredient_list, direction_list, files_list, null = ([] for i in range(7))
count=0

# Extract data from allrecipes.com HTML files
File_Folder = 'allrecipes.com'
for root, _, files in walk(File_Folder): 
    for name in files:
        if name not in files_list:
            soup_i = BeautifulSoup(open("allrecipes/" + name, 'rb'), 'html.parser')
            if (soup_i.findAll('a') and soup_i.find('span', class_='itemreviewed')): # make sure there is no blank HTML
                title = soup_i.find('span', class_='itemreviewed').text
                nutrition_list.append({'Title': title, 
                                       'Calories': float(re.search(r'([0-9\.,]+)',str(soup_i.find('span', class_= 'calories').text))[0])\
                                                   if soup_i.find('span', class_= 'calories') else np.nan,    
                                       'Totalcarbs (g)': to_g(soup_i.find('span', class_= 'totalcarbs').text)\
                                                         if soup_i.find('span', class_= 'totalcarbs') else np.nan, 
                                       'Fat (g)': to_g(soup_i.find('span', class_= 'fat').text)\
                                                  if soup_i.find('span', class_= 'fat') else np.nan, 
                                       'Protein (g)': to_g(soup_i.find('span', class_= 'protein').text)\
                                                      if soup_i.find('span', class_= 'protein') else np.nan, 
                                       'Sodium (mg)': to_Mg(soup_i.find('span', class_= 'sodium').text)\
                                                      if soup_i.find('span', class_= 'sodium') else np.nan,
                                       'Cholesterol (mg)': to_Mg(soup_i.find('span', class_= 'cholesterol').text)\
                                                           if soup_i.find('span', class_= 'cholesterol') else np.nan,
                                       'Dietaryfiber (g)': to_g(soup_i.find('span', class_='dietaryfiber').text)\
                                                           if soup_i.find('span', class_='dietaryfiber') else np.nan
                                         })
                rating_review_list.append({'Title': title, 
                                           'Rating': float(re.search(r'(\d*\.\d*)',str(soup_i.find('img', class_="rating")))[0])\
                                                     if soup_i.find('img', class_= 'rating') else np.nan, 
                                           'Reviews': int(soup_i.find('span', class_="count").text.replace(',', ''))\
                                                      if soup_i.find('span', class_="count") else np.nan
                                          })
                if soup_i.find('div', class_='times'):
                    times_list.append({'Title': title, 
                                       'Prep Time (min)': get_minutes(soup_i.find('div', class_='times').contents[1])\
                                                          if soup_i.find('div', class_='times').contents[1] else np.nan,
                                       'Cook Time (min)': get_minutes(soup_i.find('div', class_='times').contents[2])\
                                                          if soup_i.find('div', class_='times').contents[2] else np.nan,
                                       'Ready in (min)': get_minutes(soup_i.find('div', class_='times').contents[3])\
                                                         if soup_i.find('div', class_='times').contents[3] else np.nan
                                      })
                else:
                    times_list.append({'Title': title, 
                                       'Prep Time (min)': np.nan,
                                       'Cook Time (min)': np.nan,
                                       'Total Time (min)': np.nan
                                      })
                ingredients = soup_i.findAll('li', class_="plaincharacterwrap ingredient")
                ingredient_list.append({'Title': title,
                                        'Ingredient': [normalize_string(ingredient.get_text()) for ingredient in ingredients]\
                                                      if ingredients else np.nan
                                       }) 
                directions = soup_i.findAll('span', class_="plaincharacterwrap break")
                direction_list.append({'Title': title,
                                       'Direction': [normalize_string(direction.get_text()) for direction in directions]\
                                                    if directions else np.nan
                                      })
            else:
                null.append({'Title': title,
                             'Name': name
                            })
                print(count, name, 'null')   
        files_list.append({'Title': title,
                            'Name': name
                          })
        count+=1

# Save nutrition list in Pandas dataframe
pd.DataFrame(nutrition_list).to_csv('nutrition_list_allrecipes.csv')

# Save reviews and ratings list in Pandas dataframe
pd.DataFrame(rating_review_list).to_csv('rating_review_allrecipes.csv')

# Save cooking times list in Pandas dataframe
pd.DataFrame(times_list).to_csv('cooking_time_allrecipes.csv')

# Save ingredient list in Pandas dataframe
pd.DataFrame(ingredient_list).to_csv('ingredient_list_allrecipes.csv')

# Save directions list in Pandas dataframe
pd.DataFrame(direction_list).to_csv('direction_list_allrecipes.csv')

# Save list of all HTML files names in Pandas dataframe
pd.DataFrame(files_list).to_csv('files_allrecipes.csv')

# Save list of all invalid HTML files names in Pandas dataframe
pd.DataFrame(null).to_csv('null_allrecipes.csv')

# Save Pandas dataframe with all information
allrecipes_df = pd.DataFrame(nutrition_list).merge(pd.DataFrame(rating_review_list)).merge(pd.DataFrame(times_list))\
                .merge(pd.DataFrame(ingredient_list)).merge(pd.DataFrame(direction_list))
cols = list(allrecipes_df)
cols.insert(0, cols.pop(cols.index('Title')))
allrecipes_df = allrecipes_df.loc[:, cols]
allrecipes_df.drop_duplicates(subset=['Title'], inplace=True)
allrecipes_df.reset_index(inplace=True)
allrecipes_df.drop(columns='index', inplace=True)
allrecipes_df.to_csv('allrecipes_df.csv')