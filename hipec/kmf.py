import pickle
import pandas as pd
import numpy
import lifelines
from lifelines.estimation import KaplanMeierFitter
import math


with open('filtered_data.pickle', 'rb') as handle:
    data = pickle.load(handle)
    
    list_patients =[]
    for patient, data in data.items():
        patient_info= []
        v_status=(data['VitalStatus'])
        s_time = (data['SurvivalTime'])
        if v_status == 'Alive' or 'Dead':
            
            if v_status == 'Alive':
                v_status = 0
                               
            else:
                v_status = 1
            
            patient_info.append(v_status)
            
                
            
            if type(s_time)!=str:
                patient_info.append(s_time)
                
            list_patients.append(patient_info)
    
    df = pd.DataFrame(list_patients)
    
    df.columns = ['Event','Duration']
    kmf = KaplanMeierFitter()
    kmf.fit(durations=df.Duration, event_observed=df.Event)
    
    #median survival in months 
    print("median survival: "+str(kmf.median_)+ " months")
    
   
    #print(kmf.survival_function_)
 
    coordinates=[]  
    survival_fx= (kmf.survival_function_)
    coordinates_y=list(survival_fx.values.flatten())
    
    
  
    coordinates_x=[]
    for row in survival_fx.iterrows():
        timeline,km_estimate=row
        coordinates_x.append(timeline.tolist())
    

    for(x,y) in zip(coordinates_x,coordinates_y):
        coordinates.append([x,y])
    print("curve coordinates:")
    print(coordinates)  
 
    
    #calculate the survival probability for t=1 year
    surv_for_1=kmf.predict(12)
    print("probability of survival for 1 year: "+str(surv_for_1))

    #caluclate the survival probability for t=3 years
    surv_for_3=kmf.predict(36)
    print("probability of survival for 3 years: "+str(surv_for_3))

    #calculate the survival probability for t=5
    surv_for_5=kmf.predict(60)
    print("probability of surval for 5 years: "+str(surv_for_5))


   
