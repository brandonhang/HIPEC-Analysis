import pickle
import pandas as pd
import numpy
import lifelines
from lifelines.estimation import KaplanMeierFitter

'''
kaplan meier coordinates, median, and probabilities for progression free survival
'''

with open('disease-prog.pickle', 'rb') as handle:
    data = pickle.load(handle)
    list_patients =[] 
    for patient, data in data.items():
        v_status = data['VitalStatus']
        d_progression = data['DiseaseProgression']
        
        s_time = data['SurvivalTime']
        
        patient_info = []
        
        if d_progression !=None:
            if v_status !=None:
                if v_status == 'Alive' or d_progression == 'False':
                    #patient disease did not progress 
                    progression_status = 0
                else:
                    progression_status = 1
                    #patient disease did progress 
                patient_info.append(progression_status)

                if type(s_time) !=str:
                    patient_info.append(s_time)
                list_patients.append(patient_info)
    df = pd.DataFrame(list_patients)
    num_patients = len(df)
    print(str(num_patients)+ " patients used in analysis")
    

    df.columns= ['Event', 'Duration']
    kmf = KaplanMeierFitter()
    kmf.fit(durations=df.Duration, event_observed=df.Event)

    #median progression free survival in months
    print("median progression free survival: "+str(kmf.median_)+" months")

    #print(kmf.survival_function_)
    
    coordinates =[]
    survival_fx = kmf.survival_function_
    
    coordinates_y = list(survival_fx.values.flatten())
    coordinates_x=[]
    
    for row in survival_fx.iterrows():
        timeline,km_estimate=row
        coordinates_x.append(timeline.tolist())
        
    for(x,y) in zip(coordinates_x,coordinates_y):
        coordinates.append([x,y])
        
    print("curve coordinates:")
    print(coordinates)

    #calculate the progression free survival probability for t=1 year
    surv_for_1 = kmf.predict(12)
    print("probability of proression free survival for 1 year: "+str(surv_for_1))

    #calculate the progression free survival probability for t=3 years
    surv_for_3 = kmf.predict(36)
    print("probability of progression free survival for 3 years: "+str(surv_for_3))

    #calculate the progression free survival probability for t=5 years
    surv_for_5 = kmf.predict(60)
    print("probability of progression free survival for 5 years: "+str(surv_for_5))

   
    
