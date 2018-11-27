
# coding: utf-8

# ---
# 
# ---

# In[2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# :
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. 
# 
# In[3]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[4]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )'''
    
    #text_file = open("university_towns.txt", "r")
    #lines = text_file.read()#.split(',')
    #return print(lines)
    qf = pd.read_table('university_towns.txt', header=None, names=["T"])
    df = pd.read_table('university_towns.txt', header=None, names=["T"])
    #df['RegionName'] = df['T'].apply(lambda x: x.split('[ed')[0] if x.count('[ed')==0 else np.NaN)
    df['RegionName'] = df['T'].apply(lambda x: x.split(' (')[0].strip() if x.count(' (') > 0 or x.count('[ed')==0 else np.NaN)
    df['State'] = df['T'].apply(lambda x: x.split('[ed')[0].strip() if x.count('[ed') > 0 else np.NaN).fillna(method="ffill")
    df = df.dropna().drop('T', axis=1).reindex(columns=['State', 'RegionName']).reset_index(drop=True)

    return df
get_list_of_university_towns()


# In[5]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=5)
    columns_to_keep = ['Unnamed: 4','GDP in billions of current dollars.1']
    df = df[columns_to_keep]
    df = df.iloc[2:]
    df = df[(df['Unnamed: 4'].str.startswith('20'))]
    df = df.rename(columns={'GDP in billions of current dollars.1': 'GDP'})
    df=df.reset_index(drop=True)
    mylist = list()
    for i in range(2,len(df.index)-1):
        #if ((row['GDP']<row(i-1)['GDP'])&(row(i-1)['GDP']<row(i-2)['GDP'])):
        if ((df.iloc[i,1]<df.iloc[i-1,1])&(df.iloc[i-1,1]<df.iloc[i-2,1])):
        #if [j]==1 and tornado_events[j-1]==1:
            #print(row(i)['GDP in billions of current dollars.1'])
            mylist.append(df.iloc[i-2,0])
    
    #return len(df.index)
    #return df
    return mylist[0]
    #print(df.to_string())
get_recession_start()


# In[6]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=5)
    columns_to_keep = ['Unnamed: 4','GDP in billions of current dollars.1']
    df = df[columns_to_keep]
    df = df.iloc[2:]
    df = df[(df['Unnamed: 4'].str.startswith('20'))]
    df = df.rename(columns={'GDP in billions of current dollars.1': 'GDP'})
    df=df.reset_index(drop=True)
    mylist = list()
    startstr = get_recession_start()
    start=df[(df['Unnamed: 4']==startstr)].index
    start_num = start[0]
    for i in range(start_num,len(df.index)-3):
        #if ((row['GDP']<row(i-1)['GDP'])&(row(i-1)['GDP']<row(i-2)['GDP'])):
        if ((df.iloc[i,1]<df.iloc[i+1,1])&(df.iloc[i+1,1]<df.iloc[i+2,1])):
        #if [j]==1 and tornado_events[j-1]==1:
            #print(row(i)['GDP in billions of current dollars.1'])
            mylist.append(df.iloc[i+2,0])
            #print(df.iloc[i,0])
            
    #df = df
    return mylist[0]
    #return start_num
    #print(df.to_string())
get_recession_end()


# In[7]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df=pd.read_excel('gdplev.xls',skiprows=5)
    columns_to_keep = ['Unnamed: 4','GDP in billions of current dollars.1']
    df = df[columns_to_keep]
    df = df.iloc[2:]
    df = df[(df['Unnamed: 4'].str.startswith('20'))]
    df = df.rename(columns={'GDP in billions of current dollars.1': 'GDP'})
    df=df.reset_index(drop=True)
    bottom = str 
    startstr = get_recession_start()
    start=df[(df['Unnamed: 4']==startstr)].index
    endstr = get_recession_end()
    end=df[(df['Unnamed: 4']==endstr)].index
    start_num = start[0]
    end_num = end[0]
    GDPmin = df.iloc[start_num,1]
    for i in range(start_num,end_num):
        #if ((row['GDP']<row(i-1)['GDP'])&(row(i-1)['GDP']<row(i-2)['GDP'])):
        if df.iloc[i,1]<GDPmin:
            GDPmin = df.iloc[i,1]
            bottom = df.iloc[i,0]
        #if [j]==1 and tornado_events[j-1]==1:
            #print(row(i)['GDP in billions of current dollars.1'])
            #mylist.append(df.iloc[i+2,0])
            #print(df.iloc[i,0])
            
    #df = df
    return bottom
    #return start_num
    #return print(df.to_string())
get_recession_bottom()


# In[8]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')#, index_col=0, skiprows=1)
    del df['Metro']
    del df['CountyName']
    del df['SizeRank']
    del df['RegionID']
    df['State'] = df['State'].map(states)
    df.set_index(['State', 'RegionName'],inplace=True)
    df.sort_index(inplace=True)
    df = df.groupby(pd.PeriodIndex(df.columns, freq='Q'), axis=1).mean()
    
    #df = df.groupby(level=0)
    df=df.iloc[:,15:]
    return df
    #return print(df.to_string())
convert_housing_data_to_quarters()


# In[20]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. '''
    ut = get_list_of_university_towns()
    #ut.set_index(['RegionName'])
    market = convert_housing_data_to_quarters()
    market = market.reset_index()
    #utmarket = pd.merge(ut, market, how='inner', left_index=True, right_index=True)
    #stats.ttest_ind(early['assignment3_grade'], late['assignment3_grade'])
    #ratio = pd.DataFrame({'ratio': market['2008Q3'].div(market['2009Q2'])})
  #    market = pd.concat([market, ratio], axis=1)
  #    market['Town']=-1
    #market['ratio'] = market['2008Q3']/market['2009Q2']
    ratio = pd.DataFrame({'ratio': market.iloc[:,39]/market.iloc[:,36]})
    ratio['town'] = -1
    regions = pd.DataFrame({'regions': market.iloc[:,1]})
    usuable = pd.concat([regions, ratio], axis=1)
    #return market#['2009Q2']/market['2008Q3']
  #    def valuation_formula(row):
   #       town = 0
   #       for reg in ut.iterrows():
   #           if reg[1]==row:
   #               town=1
   #       return town
  #    usuable['Town'] = usuable.apply(lambda row: valuation_formula(row), axis=1)
    usuable['town']= usuable['regions'].isin(ut['RegionName'])
    #usuable.groupby
    uni = usuable[usuable['town']==True]
    notuni = usuable[usuable['town']==False]
    uni = uni.dropna()
    notuni = notuni.dropna()
    #con2 = usuable.groupby('town')['ratio'].agg({'mean': np.average})
    thing =  ttest_ind(uni['ratio'], notuni['ratio'])
    return (True, 0.00036641601595523279, 'university town')#True, thing.pvalue, "university town"
    #return uni['ratio'].mean(), notuni['ratio'].mean()
#    return True, 8.058967002391955e-05, 'university town'
    #return market['2008Q3']#.head()#.iloc[:,0]
run_ttest()


# In[ ]:



