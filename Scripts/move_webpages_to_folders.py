from bs4 import BeautifulSoup
import pandas as pd
import os
from os import walk


"""

Dataset 'Cooking recipes': 2.53 GB of zipped data and concludes more than 93,000 html web pages on recipes.
The first part of this script defines the webpage for every HTML file. The data is saved in Pandas dataframe where every HTML has a 
corresponding webpage domain. 
After we classify every webpage, we move the HTML files corresponding to 'allrecipes.com', 'food.com' and 'foodnetwork.com'
in different folders in the second part of the script.

"""

### PART 1

File_Folder = 'recipePages/'
new_website, name_html, null = ([] for i in range(3))
for root, _, files in walk(File_Folder):   # iterate over every file in the file folder 
    for name in files:                     # open every file in the folder with BeautifulSoup
        soup_i = BeautifulSoup(open(File_Folder + name, 'rb'), 'html.parser') 
        if soup_i.findAll('a'):            # if the webpage is not blank, we extract its' domain and the name of the HTML file
            comments=soup_i.find_all(string=lambda text:isinstance(text,Comment))
            new = re.search(r'http://(.*?)/', comments[0].split()[1]).group(1)
            new_website.append(new)
            name_html.append(name)
        else:                              # if the webpage is blank we classify it as a blank
            null.append(name)
            
new_website.reverse()
name_html.reverse()
pd_html = pd.DataFrame([new_website,name_html]).T
pd_html.columns = ['website','htmlfile']
pd_html.to_csv('TotalHtml2Page.csv',index=False)


### PART 2

# Set the website you want to move (we have done it for allrecipes.com, food.com and foodnetwork.com)
HTMLpages = ['allrecipes.com', 'www.food.com', 'www.foodnetwork.com']

# Move HTML files corresponding to each webpage in HTMLpages to a new corresponding folder 

for page in len(HTMLpages):
    pd_tmp = Html2Pages.loc[Html2Pages.website == HTMLpages[page]].copy()
    webname = HTMLpages[page]

    PATH = 'Project/'
    PATHSRC = PATH+'recipePages/'
    PATHDES = PATH+webname+'/'

    # if the destination folder does not exist we create the folder
    if not os.path.isdir(PATHDES):
        os.makedirs(PATHDES)

    # move html from all recipePages to corresponding folder
    for i in range(len(pd_tmp)):
        filename = pd_tmp.iloc[i].htmlfile
        src = PATHSRC+filename
        des = PATHDES
        shutil.move(src,des)