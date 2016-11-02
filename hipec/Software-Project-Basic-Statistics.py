
# coding: utf-8

# In[7]:

# Code source: Ivy Shi

import numpy as np

# input: multidimensional dictionary: dataset[patientID][surgeryID][record];
# output: stats{}: mean, median, Q1, Q3, std; example: stats['age']['mean']=65.9; stats['age']['median']=70; ...
def getStats(dataset, surgeryID):
    # #assuming first patient ID = 1 
    
    stats = {}
    for var in dataset[(1,surgeryID)]: 
        
        values = [];
        for (patient,surgeryID) in dataset:
            vtype = type(dataset[(1,surgeryID)][var])
            if vtype is int or vtype is float or vtype is long: 
                values.append(dataset[(patient,surgeryID)][var])
        
        if len(values)>0:
            stats[var]={}
            stats[var]['mean']=np.mean(values)
            stats[var]['median']=np.median(values)
            stats[var]['Q1']=np.percentile(values, 25)
            stats[var]['Q3']=np.percentile(values, 75)
            stats[var]['std']=np.std(values, ddof=1) #return sample standard deviation
    return stats

#testing ... 
"""
d = {}
for p in range(1,7):
    d[(p,1)] = {}
    

d[(1,1)]['age'] = 50
d[(2,1)]['age'] = 57
d[(3,1)]['age'] = 60
d[(4,1)]['age'] = 80
d[(5,1)]['age'] = 59
d[(6,1)]['age'] = 53
d[(1,1)]['peritoneal carcinomatosis index'] = 16
d[(2,1)]['peritoneal carcinomatosis index'] = 14
d[(3,1)]['peritoneal carcinomatosis index'] = 15
d[(4,1)]['peritoneal carcinomatosis index'] = 12
d[(5,1)]['peritoneal carcinomatosis index'] = 15
d[(6,1)]['peritoneal carcinomatosis index'] = 13
d[(1,1)]['charlson comorbidity index'] = 5.4
d[(2,1)]['charlson comorbidity index'] = 6.4
d[(3,1)]['charlson comorbidity index'] = 5.8
d[(4,1)]['charlson comorbidity index'] = 5.3
d[(5,1)]['charlson comorbidity index'] = 6.1
d[(6,1)]['charlson comorbidity index'] = 4.8

#assuming:
surgeryID = 1

out = getStats(d, surgeryID)
for v in out:
    print v
    print out[v]

"""

    


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



