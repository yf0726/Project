import requests
import os
import sys
import pandas as pd
import numpy as np
import json
import re
import shutil
from tqdm import tqdm
import glob
import csv
import matplotlib as plt
import pprint
%matplotlib inline
import warnings
import folium
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup


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
    reg = re.match(r'\D*([0-9\.,]+)\s*(g|grams|mg|milligrams)', text)
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
    reg = re.match(r'\D*([0-9\.,]+)\s*(g|grams|mg|milligrams)', text)
    if reg:
        num = reg.group(1)
        unit = reg.group(2)
        factor = 1 if ((unit == 'g') or (unit == 'grams')) else 1000
        return float(num) / factor
    else:
        return np.nan

def find_num(text):
    """        
    Function to get numbers from text.

    Parameters: 
        text: string
        
    Return:
        float number from the text
    """
    reg = re.match(r'\D*([0-9\.,]+)', text)
    if reg:
        num = reg.group(1)
        return float(num)
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


def find_rating(ss):
    """
    Function to get rating from soup element accoring to the regex expression.
    
    Parameters: 
        ss: soup element
        
    Return:
        float rating
    """
    rat = ss.find('div', class_="rating-average")
    if rat:
        r = re.search(r'(half-star|empty-star)\D*([0-9]+)', str(rat))
        if r:
            half = 0.5 if r.group(1)=='half-star' else 0.0
            return float(r.group(2))-1+half
        else:
            return 5.0
    else:
        return np.nan


recipe_file = open('yummly.json', 'a')
invalid_json_files = open('invalid.txt', 'a')
users_ratings = {}
counter = 0
directory = '/Users/zhenchensu/2018-ADA/Project/metadata'
for file in os.listdir(directory):
    filename = os.fsdecode(os.path.join(directory, file))
    counter+=1
    
    try:
        with open(filename) as json_data:
            d = pd.DataFrame(json.load(json_data))
            URL = 'https://www.yummly.com/recipe/'         
            rs = d['id']
            for r_ in rs:
                try:
                    r = requests.get(URL +r_)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    print(soup.title)
                    raw_val =soup.findAll('span',class_="raw-value")
                    flag_raw = 1 if raw_val else 0
                    len_raw = len(raw_val)
                    Title = soup.find('h1').text.replace('"', '\\"')
                    Calories = find_num(soup.find('div',class_="recipe-summary-item nutrition").text)
                    Totalcarbs = to_g(raw_val[3].text) if flag_raw and len_raw>3 else np.nan
                    Fat = to_g(raw_val[1].text) if flag_raw and len_raw>1 else np.nan
                    Protein = to_g(raw_val[2].text) if flag_raw and len_raw>2 else np.nan
                    Sodium = to_Mg(raw_val[0].text) if flag_raw else np.nan
                    Cholesterol = to_Mg(soup.findAll('td')[5].text) if soup.findAll('td')and len(soup.findAll('td'))>5 else np.nan
                    Dietaryfiber = to_g(raw_val[4].text) if flag_raw and len_raw>4 else np.nan
                    Review_num = re.search(r'\(([0-9]+)\)', soup.findAll('span', class_="count")[0].text)
                    Review_num = int(Review_num.group(1)) if Review_num else 0
                    Rating = find_rating(soup)
                    Time = get_minutes(soup.findAll('div', class_="recipe-summary-item ")[1].text)
                    recipe_file.write('{{"Title":"{}", "id":"{}", "Calories":"{}", "Totalcarbs (g)":"{}",\
                                      "Fat (g)":"{}", "Protein (g)":"{}", "Sodium (mg)":"{}", "Cholesterol (mg)":"{}",\
                                      "Dietaryfiber (g)":"{}", "Rating":"{}", "Reviews":{}, "Ready in (min)":"{}"}},\n'\
                                      .format(Title, r_, Calories, Totalcarbs, Fat, Protein,\
                                              Sodium, Cholesterol, Dietaryfiber, Rating, Review_num, Time))                 
                except AttributeError as err:
                    print('Error in:', r_)
        print(filename)
        shutil.move(filename, done)
    except:
        print(str.format("Error occured: {}",sys.exc_info()))
        invalid_json_files.write(filename+'/n')


directory = '/Users/zhenchensu/2018-ADA/Project/metadata'
data_other = pd.DataFrame()
for file in os.listdir(directory):
    filename = os.fsdecode(os.path.join(directory, file))
    data_other = pd.concat([data_other, pd.read_json(filename)])
data_yum = pd.read_json('yummly.json',orient='records')


pd.merge(data_yum, data_other, on='id').to_csv('yammly_parsing.csv')

# Save nutrition list in Pandas dataframe
pd.DataFrame(data_yum[['id', "Calories", "Totalcarbs (g)",\
                        "Fat (g)", "Protein (g)", "Sodium (mg)", "Cholesterol (mg)",\
                        "Dietaryfiber (g)"]]).to_csv('nutrition_list_yammly.csv')

# Save reviews and ratings list in Pandas dataframe
pd.DataFrame(data_yum[['id', 'Rating', 'Reviews']]).to_csv('rating_review_yammly.csv')

# Save cooking times list in Pandas dataframe
pd.DataFrame(data_yum[['id', 'Ready in (min)']]).to_csv('cooking_time_yammly.csv')

# Save ingredient list in Pandas dataframe
pd.DataFrame(data_yum[['id', 'ingredients']]).to_csv('ingredient_list_yammly.csv')

