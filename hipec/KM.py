
# coding: utf-8

# In[1]:




# In[1]:

import pandas as pd
import numpy as np
import xlrd 
import lifelines
import matplotlib.pyplot as plt


# In[28]:

columns= ['patient','survival','death']
index=np.arange(103)
df = pd.DataFrame(columns=columns, index=index)


# In[29]:

myarray= np.random.random((10,3))
for val, item in enumerate(myarray):
    df.ix[val]=item


# In[30]:

data=[{'id': 1, 'survival':113, 'death':0},
      {'id':2,'survival':62, 'death':1},
      {'id':3, 'survival':178, 'death':0},
]


# In[33]:

df = pd.DataFrame(data)


# In[34]:

from lifelines import KaplanMeierFitter


# In[35]:

kmf = KaplanMeierFitter()


# In[36]:

kmf.fit(durations= df.survival, event_observed= df.death)


# In[37]:

kmf.event_table


# In[39]:

get_ipython().magic(u'matplotlib inline')
kmf.plot()
plt.title("The Kaplan-Meier Estimate for HIPEC Procedures")
plt.ylabel("Probability a patient is alive")
plt.show()


# In[ ]:



