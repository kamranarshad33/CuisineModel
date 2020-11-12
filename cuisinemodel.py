import json 
import pandas as pd




with open(data_dir+'/cuisine_data.json') as json_file:
  cuisine= json.load(json_file)

cuisine_df= pd.DataFrame(cuisine)
cuisine_df.head()

"""**DATA TRANSFORMATION AND EDA**

This notebook(https://www.kaggle.com/tanulsingh077/what-s-cooking) describe very good the data in this data set. This data present some issues such as:

1. Special characters in the list of ingredients: **! % & ' ( ) , - . / 0 1 2 3 4 5 6 7 8 9 ® â ç è é í î ú ’ € ™**
2. Strange ingredients like: **'mi', 'mi', 'v8', 'v8'**
3. Apostrophes and Upper classes in some ingredients: **Potatoes O'Brien**
4. Hypens: **oil-cured black olives**
5. Numbers: **2% low fat cheddar chees**
6. Outliers in the number of ingredients/recipe: **65 max, 1 min. **
7. Units: **oz,lb, ounc, %**
8. Regions: **'american cheese slices'**
9. Common ingredients: **salt, onions, olive oil, water...**
"""

raw_ingredients= [ing for ingredients in cuisine_df['ingredients'] for ing in ingredients]

import re

weird_symbols= [' '.join(sorted([char for char in set(' '.join(raw_ingredients)) if re.findall('[^A-Za-z]', char)]))]

wierd_ingredients=[ingredient for ingredient in raw_ingredients if len(ingredient) <= 2]

upper_cases= list(set([ingredient for ingredient in raw_ingredients if re.findall('[A-Z]+', ingredient)]))

apostrophes= list(set([ingredient for ingredient in raw_ingredients if '’' in ingredient]))

hypens= list(set([ingredient for ingredient in raw_ingredients if re.findall('-', ingredient)]))

numbers= list(set([ingredient for ingredient in raw_ingredients if re.findall('[0-9]', ingredient)]))

regions= ['american', 'greek','filipino','indian', 'jamaican', 'italian', 'mexican']
d={}
for k in regions:
  _=[ingredient for ingredient in raw_ingredients if k in ingredient]
  d[k] = _

print(weird_symbols)
print(wierd_ingredients)
print(upper_cases[:5])
print(apostrophes)
print(hypens[:5])
print(numbers[:5])
print(d['italian'][0:5])

import matplotlib.pyplot as plt
from wordcloud import WordCloud

unique_string=('').join(raw_ingredients)
wordcloud= WordCloud(width= 1000, height= 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

#Writing data to a DB
import sqlite3


conn = None
c = None
conn = sqlite3.connect(data_dir+'/cuisine.db',check_same_thread=False)
c = conn.cursor()
