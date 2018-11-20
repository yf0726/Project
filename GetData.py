import numpy as np
from os import walk
import re
import requests
from bs4 import BeautifulSoup


def toMg(text):
    """
        This function changes unit in text like 3.3g to mg
    """
    reg = re.match(r'([0-9\.,]+)\s*(g|grams|mg|milligrams)', text)
    if reg:
        num = reg.group(1)
        unit = reg.group(2)
        factor = 1 if ((unit == 'mg') or (unit == 'milligrams')) else 1000
        return float(num) * factor
    else:
        return np.nan



File_Folder = '/Users/zhenchensu/recipePages'
nutrition_list = []
for root, _, files in walk(File_Folder):   #return three list 
    for name in files:
        print(name)
        soup_i = BeautifulSoup(open("/Users/zhenchensu/recipePages/" + name, 'rb'), 'html.parser')
        if soup_i.findAll('a'):    #make sure there is no blank HTML
            if ('allrecipes.com' in soup_i.text
                and soup_i.find('b', text= 'Amount Per Serving')):      # make sure html have info we need
                title = soup_i.find('span', class_='itemreviewed').text  # get the title
                kcal = float(soup_i.find('span', class_= 'calories').text)  # get the calories
                carb = soup_i.find('span', class_= 'totalcarbs').text
                fat = soup_i.find('span', class_= 'fat').text
                prot = soup_i.find('span', class_= 'protein').text
                sodium = soup_i.find('span', class_= 'sodium').text
                chol = soup_i.find('span', class_= 'cholesterol').text
                nutrition_list.append({'web':'allrecipes',
                                          'title': title, 
                                          'kcal': kcal, 
                                          'carb(mg)': toMg(carb), 
                                          'fat(mg)': toMg(fat), 
                                          'prot(mg)': toMg(prot), 
                                          'sodium(mg)': toMg(sodium),
                                          'chol(mg)': toMg(chol)
                                         })
            if ('food.com' in soup_i.text
                and soup_i.find('h1', {'itemprop': "name"})):      # make sure html have info we need
                title = soup_i.find('h1', {'itemprop': "name"}).text  # get the title
                kcal = float(soup_i.findAll('dt', class_="nutrition")[0].find('span', itemprop="calories").text)  # get the calories
                carb = (soup_i.findAll('dt', class_="nutrition")[6].find('span', itemprop="carbohydrateContent").text 
                        + soup_i.findAll('dt', class_="nutrition")[6].find('span', class_="type" ).text)
                fat = (soup_i.findAll('dt', class_="sub nutrition")[0].find('span', itemprop="fatContent").text 
                       + soup_i.findAll('dt', class_="sub nutrition")[0].find('span', class_="type" ).text)
                prot = (soup_i.findAll('dt', class_="nutrition")[-1].find('span', itemprop="proteinContent").text 
                       + soup_i.findAll('dt', class_="nutrition")[-1].find('span', class_="type" ).text)
                sodium = (soup_i.findAll('dt', class_="nutrition")[5].find('span', itemprop="sodiumContent").text 
                       + soup_i.findAll('dt', class_="nutrition")[5].find('span', class_="type" ).text)
                chol = (soup_i.findAll('dt', class_="nutrition")[4].find('span', itemprop="cholesterolContent").text 
                       + soup_i.findAll('dt', class_="nutrition")[4].find('span', class_="type" ).text)
                nutrition_list.append({'web':'food',
                                          'title': title, 
                                          'kcal': kcal, 
                                          'carb(mg)': toMg(carb), 
                                          'fat(mg)': toMg(fat), 
                                          'prot(mg)': toMg(prot), 
                                          'sodium(mg)': toMg(sodium),
                                          'chol(mg)': toMg(chol)
                                         })
                
                
            """
            if ('yummly.com' in soup_i.text
                and soup_i.find('b', text= 'Amount Per Serving')):      # make sure html have info we need
                title = soup_i.find('span', class_='itemreviewed').text  # get the title
                kcal = float(soup_i.find('span', class_= 'calories').text)  # get the calories
                carb = soup_i.find('span', class_= 'totalcarbs').text
                fat = soup_i.find('span', class_= 'fat').text
                prot = soup_i.find('span', class_= 'protein').text
                sodium = soup_i.find('span', class_= 'sodium').text
                chol = soup_i.find('span', class_= 'cholesterol').text
                nutrition_list.append({'web':'allrecipes',
                                          'title': title, 
                                          'kcal': kcal, 
                                          'carb(mg)': toMg(carb), 
                                          'fat(mg)': toMg(fat), 
                                          'prot(mg)': toMg(prot), 
                                          'sodium(mg)': toMg(sodium),
                                          'chol(mg)': toMg(chol)
                                         })
            if ('myrecipes.com' in soup_i.text
                and soup_i.find('b', text= 'Amount Per Serving')):      # make sure html have info we need
                title = soup_i.find('span', class_='itemreviewed').text  # get the title
                kcal = float(soup_i.find('span', class_= 'calories').text)  # get the calories
                carb = soup_i.find('span', class_= 'totalcarbs').text
                fat = soup_i.find('span', class_= 'fat').text
                prot = soup_i.find('span', class_= 'protein').text
                sodium = soup_i.find('span', class_= 'sodium').text
                chol = soup_i.find('span', class_= 'cholesterol').text
                nutrition_list.append({'web':'allrecipes',
                                          'title': title, 
                                          'kcal': kcal, 
                                          'carb(mg)': toMg(carb), 
                                          'fat(mg)': toMg(fat), 
                                          'prot(mg)': toMg(prot), 
                                          'sodium(mg)': toMg(sodium),
                                          'chol(mg)': toMg(chol)
                                         })
            """
nutrition = pd.DataFrame(nutrition_list)
nutrition

