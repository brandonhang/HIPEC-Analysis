
# coding: utf-8

# In[2]:

import random

def predictOutcomeDemo(symptoms):
    #generating a random set of coefficents
    coeff = {}
    for k in symptoms.keys():
        coeff[k] = random.random()*10 #random number between [0,10)
    coeff['const'] = 10.8
    print (coeff)
    
    #predict the outcome
    outcome = coeff['const']
    for k in coeff.keys():
        if (k!='const'):
            outcome = outcome + coeff[k]*symptoms[k]
    
    return outcome

input = {'age': 1, 'charlson_comorbidity_index': 2, 'karnofsky_performance_status': 4, 'peritoneal_carcinomatosis_index': 1, 'completeness_of_cytoreduction_score': 1}
print (input)

print ('\nsurvival time (year)', predictOutcomeDemo(input))
    


# In[ ]:




# In[ ]:



