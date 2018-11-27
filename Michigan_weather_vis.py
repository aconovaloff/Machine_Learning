
# coding: utf-8

#[United Nations](http://data.un.org/) 
#[World Bank](http://data.worldbank.org/)
#[Global Open Data Index](http://index.okfn.org/place/) 
# In[1]:

get_ipython().magic('matplotlib notebook')
import matplotlib as mpl
from matplotlib import dates as dates
from datetime import datetime
mpl.get_backend()
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[3]:

weather = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
weather = weather.sort('Date')
weather['Data_Value'] = weather['Data_Value']*0.1
new_weather = weather[weather['Date'].str.startswith('2015')]
weather = weather[weather['Date'].str.startswith('2015')==False]
weather['Date'] = weather['Date'].apply(lambda x: x[5:] )

weather = weather[weather['Date'].str.startswith('02-29')==False]
#weather['Date'] = pd.to_datetime(weather['Date'],format='%m-%d' )
#weather['Date'] = weather['Date'].dt.strftime('%m-%d' )
max_temps = weather[weather['Element'].str.startswith('TMAX')]
min_temps = weather[weather['Element'].str.startswith('TMIN')]
max_temps = max_temps.groupby('Date')['Data_Value'].max()#agg({'max':np.max()})
min_temps = min_temps.groupby('Date')['Data_Value'].min()
min_temps.index = pd.to_datetime(min_temps.index,format='%m-%d' )
max_temps.index = pd.to_datetime(max_temps.index,format='%m-%d' )
new_weather['Data_Value']=new_weather['Data_Value']
new_weather['Date'] = new_weather['Date'].apply(lambda x: x[5:] )
#new_weather['Date'] = pd.to_datetime(new_weather['Date'],format='%m-%d' )
#new_weather['Date'] = new_weather['Date'].dt.strftime('%m-%d' )
new_weather_max = new_weather[new_weather['Element'].str.startswith('TMAX')]
new_max_temps = new_weather_max.groupby('Date')['Data_Value'].max()
new_weather_min = new_weather[new_weather['Element'].str.startswith('TMIN')]
new_min_temps = new_weather_min.groupby('Date')['Data_Value'].min()
new_min_temps.index = pd.to_datetime(new_min_temps.index,format='%m-%d' )
new_max_temps.index = pd.to_datetime(new_max_temps.index,format='%m-%d' )
#new_min_temps['zero']=0
comp_max = pd.concat([max_temps.rename('all'), new_max_temps.rename('new')], axis=1)
comp_min = pd.concat([min_temps.rename('all'), new_min_temps.rename('new')], axis=1)
comp_max['comp']= -1
def valuation_formula(row):
        if row['all'] >= row['new']:
            return 0
        else:
            return 1
comp_max['comp'] = comp_max.apply(lambda row: valuation_formula(row),axis=1)
comp_max = comp_max[comp_max['comp']==1]
comp_max = comp_max['new']
comp_min['comp']= -1
def valuation_formula2(row):
        if row['all'] <= row['new']:
            return 0
        else:
            return 1
comp_min['comp'] = comp_min.apply(lambda row: valuation_formula2(row),axis=1)
comp_min = comp_min[comp_min['comp']==1]
comp_min = comp_min['new']

#plt.plot(max_temps)
#plt.scatter(comp_min.index, comp_min)
#plt.scatter(comp_max.index, comp_max)
ax = plt.gca()
#xaxis = [datetime.strptime(d, '%Y%m%d') for d, v in min_temps]
#line=max_temps.index
#xaxis=dates.date2num(max_temps.index.to_pydatetime())    # Convert to maplotlib format
#hfmt = dates.DateFormatter('%m\n%d')
#hfmt = dates.DateFormatter('%m')
#months = dates.MonthLocator()
#ax.xaxis.set_major_formatter(months)
#ax.xaxis.set_major_formatter(hfmt)
#pyplot.plt(xaxis, yaxis)
#hfmt = matplotlib.dates.DateFormatter('%m-%d')
#ax = plt.gca()
#ax.xaxis.set_major_formatter(hfmt)
plt.scatter(comp_max.index, comp_max, color='red', s=15, zorder=3)
plt.scatter(comp_min.index, comp_min, color='blue', s=15, zorder=4)
plt.plot(min_temps, color='gray', label='_nolegend_')
plt.plot(max_temps, color='gray', label='_nolegend_')

#ax.set_xlim(1, right)
ax.set_xlim([datetime(1900, 1, 1), datetime(1900, 12, 31)])
#dates.num2date(ax.get_xlim()

#ax.xaxis.set_minor_formatter(dates.DayLocator(interval=3))
xaxis=dates.date2num(max_temps.index.to_pydatetime())    # Convert to maplotlib format
hfmt = dates.DateFormatter('%m\n%d')
hfmt = dates.DateFormatter('%b')
ax.xaxis.set_major_formatter(hfmt)
fig = plt.gcf()
fig.set_size_inches(6.5, 4.5)
#plt.gca().fill_between( (dates.date2num(datetime(1900, 1, 1)), dates.date2num(datetime(1900, 12, 31))),
plt.gca().fill_between( max_temps.index,
                       max_temps, min_temps,
                     facecolor='blue', 
                       alpha=0.25)
plt.gca()
#ax.set_xticks(rotation=70)
plt.setp(ax.get_xticklabels(), rotation=0, horizontalalignment='left')
plt.show()
plt.legend(loc=4, frameon=False)

#L.get_texts()[0].set_text('')
#L.get_texts()[1].set_text('')
plt.xlabel('Month', fontsize=18)
plt.ylabel('Temperature (Celsius)', fontsize=16)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

L = plt.legend( loc = 'lower right')
L.get_texts()[0].set_text('Hotter in 2015')
L.get_texts()[1].set_text('Colder in 2015')
fig.suptitle('test title', fontsize=20)
fig.suptitle('Max/Min Temperatures by Day of the Year \n 2005-2014', fontsize=20)
#max_temps


# In[ ]:




# In[ ]:



