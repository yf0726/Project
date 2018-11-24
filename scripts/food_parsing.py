import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
from os import walk
import numpy as np

"""

Below is the code for data extraction from `www.food.com` with additional helper functions. 
We infer information which includes the name of the dish, preparation time, reviews, the ingredients, 
directions for preparation and nutritional facts. We save all features in different Pandas dataframes for 
easier comparison and analysis and as well we create a Pandas dataframe which contains 
every information gathered from `www.food.com`.

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

# Extract data from www.food.com HTML files
File_Folder = 'www.food.com'
for root, _, files in walk(File_Folder):   #return three list 
    for name in files:
        if name not in file_list:
            soup_i = BeautifulSoup(open("food/" + name, 'rb'), 'html.parser')
            if soup_i.findAll('a'):    #make sure there is no blank HTML
                if ('food.com' in soup_i.text and soup_i.find('dt', class_="nutrition")) and soup_i.findAll('li', {'class': 'ingredient'}): 
                    title = soup_i.find('h1', {'itemprop': "name"}).text
                    nutrition_list.append({'Title': title, 
                                           'Calories': float(re.search(r'(\d*\.?\d*)',str(soup_i.findAll('dt', class_="nutrition")[0].find('span', itemprop="calories").text)).group(1))\
                                                       if soup_i.findAll('dt', class_="nutrition")[0].find('span', itemprop="calories").text else np.nan,    
                                           'Totalcarbs (g)': to_g(soup_i.findAll('dt', class_="nutrition")[6].find('span', itemprop="carbohydrateContent").text 
                                                                  + soup_i.findAll('dt', class_="nutrition")[6].find('span', class_="type" ).text), 
                                           'Fat (g)': to_g(soup_i.findAll('dt', class_="sub nutrition")[0].find('span', itemprop="fatContent").text 
                                                           + soup_i.findAll('dt', class_="sub nutrition")[0].find('span', class_="type" ).text), 
                                           'Protein (g)': to_g(soup_i.findAll('dt', class_="nutrition")[-1].find('span', itemprop="proteinContent").text 
                                                               + soup_i.findAll('dt', class_="nutrition")[-1].find('span', class_="type" ).text), 
                                           'Sodium (mg)': to_Mg(soup_i.findAll('dt', class_="nutrition")[5].find('span', itemprop="sodiumContent").text 
                                                                + soup_i.findAll('dt', class_="nutrition")[5].find('span', class_="type" ).text),
                                           'Cholesterol (mg)': to_Mg(soup_i.findAll('dt', class_="nutrition")[4].find('span', itemprop="cholesterolContent").text 
                                                                     + soup_i.findAll('dt', class_="nutrition")[4].find('span', class_="type" ).text),
                                           'Dietaryfiber (g)': to_g(soup_i.findAll('dt', class_="nutrition")[7].find('span', itemprop="fiberContent").text 
                                                                    + soup_i.findAll('dt', class_="nutrition")[7].find('span', class_="type" ).text)
                                             })
                    rating_review_list.append({'Title': title, 
                                               'Rating': np.nan, # this webpage does not have recipe ratings
                                               'Reviews': check(int(re.search(r'Reviews\((\d*)',soup_i.find('ul', class_="menu button-nav").text).group(1)))
                                              })
                    times_list.append({'Title': title, 
                                       'Prep Time (min)': get_minutes(check(soup_i.find('p', class_="preptime").text)),
                                       'Cook Time (min)': get_minutes(check(soup_i.find('p', class_="cooktime").text)),
                                       'Total Time (min)': get_minutes(check(soup_i.find('h3', class_="duration").text))
                                      })
                    ingredients = soup_i.findAll('li', {'class': 'ingredient'})
                    ingredient_list.append({'Title': title,
                                            'Ingredients': [normalize_string(ingredient.get_text()) for ingredient in ingredients]\
                                                          if ingredients else np.nan
                                           }) 
                    directions = soup_i.findAll('span', class_="instructions")
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
pd.DataFrame(nutrition_list).to_csv('nutrition_list_food.csv')

# Save reviews and ratings list in Pandas dataframe
pd.DataFrame(rating_review_list).to_csv('rating_review_food.csv')

# Save cooking times list in Pandas dataframe
pd.DataFrame(times_list).to_csv('cooking_time_food.csv')

# Save ingredient list in Pandas dataframe
pd.DataFrame(ingredient_list).to_csv('ingredient_list_food.csv')

# Save directions list in Pandas dataframe
pd.DataFrame(direction_list).to_csv('direction_list_food.csv')

# Save list of all HTML files names in Pandas dataframe
pd.DataFrame(files_list).to_csv('files_food.csv')

# Save list of all invalid HTML files names in Pandas dataframe
pd.DataFrame(null).to_csv('null_food.csv')

# Save Pandas dataframe with all information
food_df = pd.DataFrame(nutrition_list).merge(pd.DataFrame(rating_review_list)).merge(pd.DataFrame(times_list))\
                .merge(pd.DataFrame(ingredient_list)).merge(pd.DataFrame(direction_list))
cols = list(food_df)
cols.insert(0, cols.pop(cols.index('Title')))
food_df = food_df.loc[:, cols]
food_df.drop_duplicates(subset=['Title'], inplace=True)
food_df.reset_index(inplace=True)
food_df.drop(columns='index', inplace=True)
food_df.to_csv('food_df.csv')