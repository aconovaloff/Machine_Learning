
# coding: utf-8


# In[80]:

get_ipython().magic('matplotlib notebook')
import matplotlib as mpl
from matplotlib import dates as dates
from datetime import datetime
mpl.get_backend()
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np
import matplotlib.ticker as tick
base = pd.read_excel('diamondbacks.xlsx')
foot = pd.read_excel('cardinals2.xlsx')
hock = pd.read_excel('Coyotes2.xlsx')
bask = pd.read_excel('suns2.xlsx')
hock['Season'] = hock['Season'].apply(lambda x: x[:4])
bask['Season'] = bask['Season'].apply(lambda x: x[:4])
bask.set_index('Season', inplace=True)
base.set_index('Season', inplace=True)
foot.set_index('Season', inplace=True)
hock.set_index('Season', inplace=True)
hock.iloc[6]=.534483
foot = foot['Pct']
hock = hock['Pct']

ax1 = plt.subplot(4, 1, 1)
plt.plot(hock, color='red')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
ax1.set_ylim([0, 0.85])
y = np.linspace(0, .75, 4)
ax1.set_yticks(y)
ax1.set_yticklabels(y)
ax1.set_title("Phoenix Coyotes (Hockey)",fontsize=10, y=0.08)
ax2 = plt.subplot(4, 1, 2, sharex=ax1)
plt.plot(base, color='blue')
plt.setp(ax2.get_xticklabels(), visible=False)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
ax2.set_ylim([0, 0.85])
ax2.set_yticks(y)
ax2.set_yticklabels(y)
ax2.set_title("Arizona Diamondbacks (Baseball)",fontsize=10, y=0.08)
ax3 = plt.subplot(4, 1, 3, sharex=ax1)
plt.plot(foot, color='green')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')
ax3.set_ylim([0, 0.85])
ax3.set_yticks(y)
ax3.set_yticklabels(y)
ax3.set_title("Arizona Cardinals (Football)",fontsize=10, y=0.08)
ax4 = plt.subplot(4, 1, 4, sharex=ax1)
plt.plot(bask, color='black')
ax4.set_ylim([0, 0.85])
ax4.set_yticks(y)
ax4.set_yticklabels(y)
x = (1998, 2001, 2004, 2007, 2010,2013,2016)
ax4.set_xticks(x)
ax4.set_xticklabels(x)
ax4.set_title("Phoenix Suns (Basketball)", fontsize=10, y=0.08)
fig.tight_layout()
plt.suptitle("Phoenix Area Professional Sports Teams' \n Win Percentage by Year, 1998-2018", fontsize=10)
#plt.subplots_adjust(left=None, bottom=None, right=None, top=1, wspace=None, hspace=None)

#ax4.set_xticks([])
#plt.plot(hock, color='red')
#plt.plot(base, color='blue')
#plt.plot(foot, color='green')
#plt.plot(bask, color='black')
#fig = plt.gcf()
#fig.set_size_inches(9.5, 4.5)
#hock
#hock


# In[ ]:



