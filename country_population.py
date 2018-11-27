
# coding: utf-8


#from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls)

# In[14]:


import pandas as pd
import numpy as np
energy = pd.read_excel('Energy Indicators.xls', skiprows=16, skip_footer=283-245)
del (energy['Unnamed: 0'],energy['Unnamed: 1'])
energy= energy.rename(columns={'Unnamed: 2': 'Country', 'Energy Supply per capita': 'Energy Supply per Capita', 'Renewable Electricity Production': '% Renewable'})
energy['Country'] = energy['Country'].str.replace(r"\(.*\)","")
energy['Country'] = energy['Country'].str.replace('\d+', '')
energy.set_index('Country', inplace=True)
energy= energy.rename(index={"Republic of Korea": "South Korea","United States of America": "United States","United Kingdom of Great Britain and Northern Ireland": "United Kingdom","China, Hong Kong Special Administrative Region": "Hong Kong"})
energy = energy.drop(energy.index[[0]])
energy.index = energy.index.str.strip()
energy = energy.applymap(lambda x: np.nan if isinstance(x, str) and x.isspace() else x)
energy = energy.replace('...', np.NaN)
energy['Energy Supply'] = energy['Energy Supply']*1000000
#return (energy['Country'].str.startswith('United States of'))
GDP = pd.read_csv('world_bank.csv', skiprows=4)
GDP= GDP.rename(columns={'Country Name': 'Country'})
columns_to_keep = ['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
GDP = GDP[columns_to_keep]
GDP.set_index('Country', inplace=True)
GDP= GDP.rename(index={"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"})
ScimEn=pd.read_excel('scimagojr-3.xlsx')
ScimEn.set_index('Country', inplace=True)


# In[15]:


def answer_one():
    merge1 = pd.merge(energy, GDP, how='inner', left_index=True, right_index=True)
    merge2 = pd.merge(ScimEn, merge1, how='inner', left_index=True, right_index=True)
    merge2 = merge2[(merge2['Rank']<16)]
    return merge2
answer_one()
#['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']


# In[14]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[4]:

def answer_two():
    merge1 = pd.merge(energy, GDP, how='inner', left_index=True, right_index=True)
    merge2 = pd.merge(ScimEn, merge1, how='inner', left_index=True, right_index=True)
    number_small = len(merge2.index)
    merge3 = pd.merge(energy, GDP, how='outer', left_index=True, right_index=True)
    merge4 = pd.merge(ScimEn, merge3, how='outer', left_index=True, right_index=True)
    number_big = len(merge4.index)
    number = number_big - number_small
    return number_big-number_small
answer_two()


# *This function returns a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[7]:

def answer_three():
    Top15 = answer_one()
    avgGDP1 = Top15.groupby(level=0)['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].agg({'avg': np.average})
    avgGDP = avgGDP1.mean(axis=1)
    avgGDP.sort(ascending=False)
    return avgGDP
answer_three()


# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?


# In[10]:

def answer_four():
    Top15 = answer_one()
    change = Top15.loc['United Kingdom', '2015']-Top15.loc['United Kingdom','2006']
    return change
answer_four()


# What is the mean `Energy Supply per Capita`?

# In[12]:

def answer_five():
    Top15 = answer_one()
    #avgEPC = Top15['Energy Supply per Capita'].mean()
    #avgGDP = avgGDP1.mean(axis=1)
    return Top15['Energy Supply per Capita'].mean()
answer_five()


# What country has the maximum % Renewable and what is the percentage?
# In[16]:

def answer_six():
    Top15 = answer_one()
    return Top15['% Renewable'].idxmax(), Top15['% Renewable'].max()
answer_six()


# Return maximum value for this new column and highest ratio

# In[6]:

def answer_seven():
    Top15 = answer_one()
    ratio = (Top15['Self-citations']/Top15['Citations']).idxmax(),(Top15['Self-citations']/Top15['Citations']).max()
    return ratio
answer_seven()


# Creates a column that estimates the population using Energy Supply and Energy Supply per capita. 
# In[32]:

def answer_eight():
    Top15 = answer_one()
    pop_est = (Top15['Energy Supply']/Top15['Energy Supply per Capita'])
    pop_est.sort(ascending=False)
    return pop_est.index[2]
answer_eight()
 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[36]:

def answer_nine():
    Top15 = answer_one()
    Top15['Citable docs per Capita'] = Top15['Citable documents']/((Top15['Energy Supply']/Top15['Energy Supply per Capita']))
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
answer_nine()
    


# In[35]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
#plot9()


# In[ ]:

# % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[94]:

def answer_ten():
    Top15 = answer_one()
    mean = Top15['% Renewable'].median()
    Top15['zoro']=-1
    def valuation_formula(row):
        if row['% Renewable'] >= mean:
            return 1
        else:
            return 0 
    Top15['zoro'] = Top15.apply(lambda row: valuation_formula(row), axis=1)
    HighRenew = Top15.sort_values('Rank')
   # sort = Top15['Rank', 'zoro']
    return HighRenew['zoro']
answer_ten()


# The following dictionary groups the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[125]:

def answer_eleven():
    ContinentDict = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    Top15['popest']= (Top15['Energy Supply']/Top15['Energy Supply per Capita'])
    con = pd.DataFrame(list(ContinentDict.items()),
                      columns=['Country','Continent'])
    con.set_index('Country', inplace=True)
    con2 = pd.merge(con, Top15, how='inner', left_index=True, right_index=True)
    con2 = con2.reset_index()
    #con2.set_index('Continent', inplace=True)
    con2 = con2.groupby('Continent')['popest'].agg({'size':np.size, 'sum': np.sum, 'mean': np.average, 'std':np.std})
    return con2
answer_eleven()


# *This function returns a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Groups with no countries are not included.*

# In[23]:

def answer_twelve():
    ContinentDict = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    con = pd.DataFrame(list(ContinentDict.items()),columns=['Country','Continent'])
    con.set_index('Country', inplace=True)
    con2 = pd.merge(con, Top15, how='inner', left_index=True, right_index=True)
    con2 = con2.reset_index()
    con2['bin']= pd.cut(con2['% Renewable'],5)
    #con2.groupby(['Continent','bins']).size()
    con3 = con2.groupby(['Continent', 'bin'])['Continent'].agg(len)#['% Renewable'].agg({'avg': np.average})
    #def valuation_formula(row):
     #   if (row['% Renewable'] >= mean)&(row['% Renewable'] < mean):
      #      return 1
       # elif:
        #    return 0 
    
    return con3
answer_twelve() 



 
# *This function returns a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[27]:

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst']= (Top15['Energy Supply']/Top15['Energy Supply per Capita'])
    #Top15['PopEst'] = Top15['PopEst'].map('{:,.2f}'.format)
    Top15['PopEst'] = Top15['PopEst'].map('{0:,}'.format)
    return Top15['PopEst']
answer_thirteen()

 
# Use the built in function `plot_optional()` to see a visualization.

# In[ ]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:


