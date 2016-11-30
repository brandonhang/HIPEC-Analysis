from django.db import models
from django.forms import ModelForm
from django.utils.encoding import python_2_unicode_compatible
import datetime
import os, re
import pandas as pd
import numpy as np
import math
import lifelines
from lifelines.estimation import KaplanMeierFitter

import pickle

class SurvivalAnalysis(models.Model):
	''' This function filters out the HIPEC Excel data for relevant patient
	information.  It is then used to generate the output page. '''
	@staticmethod
	def filter_data(captured_data):
		''' This function reads in a Yes/No response and returns True/False.
		It returns None if the response is not 'Yes' or 'No'. '''
		def parse_boolean(boolean):
			if boolean == 'Yes':
				return True
			elif boolean == 'No':
				return False
			else:
				return None
		''' End parse_boolean() '''
		
		''' This function reads in the Excel file of (deidentified) patient
		information and cleans it for the relevant filters necessary for the
		web app. '''
		def filter_excel():
			ordinals = {
				'First': 1,
				'Second': 2,
				'Third': 3,
				'Fourth': 4,
				'Fifth': 5,
				'Sixth': 6,
				'Seventh': 7,
				'Eighth': 8,
				'Ninth': 9
			}
			
			hipec_data = {}
			data = pd.read_excel('hipec\\data\\HIPEC_data.xlsx')
			regex = re.compile('CC-[0-2]')
			
			for row_index, row in data.iterrows():
				p_id = row['HIPEC Study ID']
				data_type = row['Event Name']
				
				''' Creates a cleaned data structure to view and manipulate
				patient data in a more Python usable format. '''
				# Build demographic information
				if 'Registry' in data_type:
					gender = row['Gender']
					race = row['Race']
					
					gender = str(gender)
					race = str(race)
					
					if gender == 'nan':
						gender = None
					if race == 'nan':
						gender = None
					
					# Set up hash-ception if non-existent
					if p_id not in hipec_data:
						hipec_data[p_id] = {}
					
					hipec_data[p_id]['Gender'] = gender
					hipec_data[p_id]['Race'] = race
				
				# Build HIPEC information
				else:
					hipec_num = data_type.split(' ')
					hipec_num = hipec_num[0]
					hipec_index = ordinals[hipec_num]
					
					# Core filters
					tumor = row['Diagnosis']
					age = row['Age at HIPEC']
					cci = row['CCI']
					kps = row["Karnofsky's Performance Status"]
					pci = row[' Intra Op PCI Score ']
					cc_score = row['Post-Op-CC-Score']
					num_prev_hipecs = hipec_index
					
					# Additional data for survival calculations
					s_time = row['Survival time from Surgery']
					vitals = row['Vital Status at analysis/SSDI']
					diseasel = row['Disease Progression']
					
					# Demographic information related to HIPEC operations
					bmi = row['Pre Op BMI']
					asa = row['ASA']
					depression = row['History of Depression Pre Op']
					beta_b = row['Beta Blocker']
					antidepr = row['Antidepressant']
					smoker = row['Smoker']
					smoke_s = row['Smoking Status']
					pack_years = row['Number of pack-years']
					
					# Attempt to enforce data types
					try:
						age = float(age)
					except ValueError:
						age = None
					
					try:
						cci = int(cci)
					except ValueError:
						cci = None
					
					try:
						kps = int(kps)
					except ValueError:
						kps = None
					
					try:
						pci = int(pci)
					except ValueError:
						pci = None
					
					# Attempt to parse CC score from string
					if isinstance(cc_score, basestring):
						cc_score = regex.match(cc_score)
					else:
						cc_score = None
					
					if cc_score is not None:
						cc_score = cc_score.group()
						cc_score = int(cc_score[3])
					
					# Clean demographic data associated with HIPEC operations
					try:
						bmi = float(bmi)
					except ValueError:
						bmi = None
					
					try:
						asa = asa[4]
					except IndexError:
						asa = None
					except TypeError:
						asa = None
					
					depression = parse_boolean(depression)
					beta_b = parse_boolean(beta_b)
					antidepr = parse_boolean(antidepr)
					smoker = parse_boolean(smoker)
					smoke_s = str(smoke_s)
					
					if 'No Data' in smoke_s or smoke_s == 'nan':
						smoke_s = None
					
					try:
						pack_years = int(pack_years)
					except ValueError:
						pack_years = None
					
					# Core outcomes
					hospital_stay = row['Hospital Length of Stay']
					disposition = row['Discharge Disposition']
					readmit = row['Readmission']
					readmission = parse_boolean(readmit)
					
					# Attempt to enforce data type
					try:
						hospital_stay = int(hospital_stay)
					except ValueError:
						hospital_stay = None
					
					disposition = str(disposition)
					
					if 'No Data' in disposition or disposition == 'nan':
						disposition = None
					
					# Clean survival calculation data
					try:
						survival_t = float(s_time)
					except ValueError:
						survival_t = None
					
					vital_stat = str(vitals)
					
					if 'No Data' in vital_stat or vital_stat == 'nan':
						vital_stat = None
					
					diseasel = parse_boolean(diseasel)
					
					# Morbidity and mortality -> booleans
					morb_30 = row['Morbidity < 30Days']
					morb_60 = row['Morbidity 31 to 60 days']
					morb_90 = row['Morbidty 61 to 90days']
					morbidity_30 = parse_boolean(morb_30)
					morbidity_60 = parse_boolean(morb_60)
					morbidity_90 = parse_boolean(morb_90)
					
					mort_30 = row['Mortality at < 30 days']
					mort_60 = row['Mortality at 31 to 60 Days']
					mort_90 = row['Mortality at 61 to 90 Days']
					mortality_30 = parse_boolean(mort_30)
					mortality_60 = parse_boolean(mort_60)
					mortality_90 = parse_boolean(mort_90)
					
					# Set up hash-ception if non-existent
					if p_id not in hipec_data:
						hipec_data[p_id] = {}
					
					if 'HIPEC' not in hipec_data[p_id]:
						hipec_data[p_id]['HIPEC'] = {}
					
					# Build HIPEC hash
					hipec_data[p_id]['HIPEC'][hipec_index] = {
						'PrimaryTumor': str(tumor),
						'Age': age,
						'CCI': cci,
						'KPS': kps,
						'PCI': pci,
						'CC': cc_score,
						'PreviousHIPECs': num_prev_hipecs,
						'HospitalStay': hospital_stay,
						'Disposition': disposition,
						'Readmission': readmission,
						'Morbidity30': morbidity_30,
						'Morbidity60': morbidity_60,
						'Morbidity90': morbidity_90,
						'Mortality30': mortality_30,
						'Mortality60': mortality_60,
						'Mortality90': mortality_90,
						'SurvivalTime': survival_t,
						'VitalStatus': vital_stat,
						'DiseaseProgression': diseasel,
						'BMI': bmi,
						'ASA': asa,
						'PreOpDepression': depression,
						'BetaBlocker': beta_b,
						'Antidepressant': antidepr,
						'Smoker': smoker,
						'SmokerStatus': smoke_s,
						'SmokePackYears': pack_years
					}
			
			return hipec_data
		''' End read_excel() '''
		
		''' Temporary helper function for testing '''
		def get_all_hipec_data_of(variable, master_data):
			data_list = []
			
			for id_op_key, patient in master_data.items():
				data_list.append(patient[variable])
			
			return data_list
		''' End get_all_hipec_data_of() '''
		
		''' Function to return percent discharged home '''
		def home_disposition(data_list):
			home = 0
			total = 0
			
			for disp in data_list:
				if disp == 'Home':
					home += 1
				
				total += 1
			
			if total == 0:
				return 0
			else:
				percent = home / float(total)
				percent = int(round(percent * 100))
				return percent
		''' End home_disposition() '''
		
		''' Function to calculate readmission rate '''
		def calc_readmit(data_list):
			true = 0
			total = 0
			
			for boolean in data_list:
				if boolean == True:
					true += 1
				
				total += 1
			
			if total == 0:
				return 0
			else:
				percent = true / float(total)
				percent = int(round(percent * 100))
				return percent
		''' End calc_readmit() '''
		
		''' Function to calculate morbidity and mortality '''
		def calc_morb_mort(mode, data):
			# Morbidity calculation
			if mode:
				mor30 = get_all_hipec_data_of('Morbidity30', data)
				mor60 = get_all_hipec_data_of('Morbidity60', data)
				mor90 = get_all_hipec_data_of('Morbidity90', data)
			# Mortality calculation
			else:
				mor30 = get_all_hipec_data_of('Mortality30', data)
				mor60 = get_all_hipec_data_of('Mortality60', data)
				mor90 = get_all_hipec_data_of('Mortality90', data)
			
			true = 0
			total = 0
			
			for index, value in enumerate(mor30):
				if mor30[index] == True:
					true += 1
				elif mor60[index] == True:
					true += 1
				elif mor90[index] == True:
					true += 1
				
				total += 1
			
			if total == 0:
				return 0
			else:
				percent = true / float(total)
				
				if (mode):
					percent = int(round(percent * 100))
				else:
					percent = '%.1f' % round(percent * 100, 1)
				
				return percent
		''' End calc_morb_mort() '''
		
		''' Parses filtered data and calculates basic statistics '''
		def getStats(dataset):
			stats = {}
			
			keys = list(dataset.keys())
			for var in dataset[keys[0]]: 
				values = [];
				for (patient,surgeryID) in dataset:
					if (var in dataset[(patient,surgeryID)]):
						vtype = type(dataset[(patient,surgeryID)][var])
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
		''' End getStats() '''
		
		''' Filters out and returns patient information based on the core
		variable parameters. '''
		def filter_patient_data(data):
			registry = {
				'dem_gender': 'Gender',
				'dem_race': 'Race'
			}
			optionals = {
				'dem_asa': 'ASA',
				'dem_depression': 'PreOpDepression',
				'dem_beta_block': 'BetaBlocker',
				'dem_antidepr': 'Antidepressant',
				'dem_smoker': 'Smoker',
				'dem_smoke_status': 'SmokerStatus'
			}
			filtered = {}
			
			for p_id, patient in data.items():
				# Filtering of demographic info would go here
				# 'continue' if demographics don't match
				for op_num, op_data in patient['HIPEC'].items():
					if op_data['PrimaryTumor'] == captured_data['core_primary_tumor'] \
						and op_data['Age'] >= captured_data['core_age__lower'] \
						and op_data['Age'] <= captured_data['core_age__upper'] \
						and op_data['CCI'] >= captured_data['core_charlson__lower'] \
						and op_data['CCI'] <= captured_data['core_charlson__upper'] \
						and op_data['KPS'] >= captured_data['core_karnofsky__lower'] \
						and op_data['KPS'] <= captured_data['core_karnofsky__upper'] \
						and op_data['PCI'] >= captured_data['core_peritoneal__lower'] \
						and op_data['PCI'] <= captured_data['core_peritoneal__upper'] \
						and op_data['CC'] == captured_data['core_cytoreduction']:
						
						add_data = True
						
						# Check optional registry parameters if relevant
						if add_data:
							for optional_param, optional_var in registry.items():
								if captured_data[optional_param] != None and \
									captured_data[optional_param] != '':
									
									if patient[optional_var] != \
										captured_data[optional_param]:
										
										add_data = False
										break
							
						# Check optional parameters if relevant
						if add_data:
							for optional_param, optional_var in optionals.items():
								if captured_data[optional_param] != None and \
									captured_data[optional_param] != '':
									
									if op_data[optional_var] != \
										captured_data[optional_param]:
										
										add_data = False
										break
						
						# Check if BMI is defined
						if add_data:
							if captured_data['enable_dem_bmi'] != None:
								if op_data['BMI'] < captured_data['dem_bmi__lower'] \
									or op_data['BMI'] > captured_data['dem_bmi__upper']:
									
									add_data = False
						
						# Check if number of pack/years is defined
						if add_data:
							if captured_data['enable_dem_smoke_pack'] != None:
								if op_data['SmokePackYears'] < captured_data['dem_smoke_pack__lower'] \
									or op_data['SmokePackYears'] > captured_data['dem_smoke_pack__upper']:
									
									add_data = False
						
						if add_data:
							filtered[(p_id, op_num)] = op_data
			
			return filtered
		''' End filter_patient_data() '''
		
		''' Build overall survival analysis statistics '''
		def overall_survival_analysis(data):
			list_patients =[]
			for patient, data in data.items():
				patient_info= []
				v_status= data['VitalStatus']
				s_time= data['SurvivalTime']
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
			num_patients = len(df)
			
			df.columns = ['Event','Duration']
			kmf = KaplanMeierFitter()
			kmf.fit(durations=df.Duration, event_observed=df.Event)
			
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
			
			#calculate the survival probability for t=1 year
			surv_for_1=kmf.predict(12)
			
			#caluclate the survival probability for t=3 years
			surv_for_3=kmf.predict(36)
			
			#calculate the survival probability for t=5
			surv_for_5=kmf.predict(60)
			
			surv_median = int(round(kmf.median_))
			year_1_surv = int(round(surv_for_1 * 100))
			year_3_surv = int(round(surv_for_3 * 100))
			year_5_surv = int(round(surv_for_5 * 100))
			
			overall_surv_stats = {}
			overall_surv_stats['Coordinates'] = coordinates
			overall_surv_stats['Median'] = surv_median
			overall_surv_stats['1Year'] = year_1_surv
			overall_surv_stats['3Year'] = year_3_surv
			overall_surv_stats['5Year'] = year_5_surv
			
			return overall_surv_stats
		''' End overall_survival_analysis() '''
		
		''' Build progression free survival statistics '''
		def progression_free_analysis(data):
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
			
			df.columns= ['Event', 'Duration']
			kmf = KaplanMeierFitter()
			kmf.fit(durations=df.Duration, event_observed=df.Event)
			
			coordinates =[]
			survival_fx = kmf.survival_function_
			
			coordinates_y = list(survival_fx.values.flatten())
			coordinates_x=[]
			
			for row in survival_fx.iterrows():
				timeline,km_estimate=row
				coordinates_x.append(timeline.tolist())
				
			for(x,y) in zip(coordinates_x,coordinates_y):
				coordinates.append([x,y])
			
			#calculate the progression free survival probability for t=1 year
			surv_for_1 = kmf.predict(12)
			
			#calculate the progression free survival probability for t=3 years
			surv_for_3 = kmf.predict(36)
			
			#calculate the progression free survival probability for t=5 years
			surv_for_5 = kmf.predict(60)
			
			surv_median = int(round(kmf.median_))
			year_1_surv = int(round(surv_for_1 * 100))
			year_3_surv = int(round(surv_for_3 * 100))
			year_5_surv = int(round(surv_for_5 * 100))
			
			prog_free_stats = {}
			prog_free_stats['Coordinates'] = coordinates
			prog_free_stats['Median'] = surv_median
			prog_free_stats['1Year'] = year_1_surv
			prog_free_stats['3Year'] = year_3_surv
			prog_free_stats['5Year'] = year_5_surv
			
			return prog_free_stats
		''' End progression_free_analysis() '''
		
		# Setup the Python pickle object file
		modded = int(os.path.getmtime('hipec\\data\\HIPEC_data.xlsx'))
		modded = str(modded)
		pickle_path = 'hipec\\data\\hipec_data-' + modded + '.pickle'
		
		# Attempt to load the Python pickle, otherwise create a new one
		try:
			with open(pickle_path, 'rb') as handle:
				hipec_data = pickle.load(handle)
		except IOError:
			hipec_data = filter_excel()
			
			with open(pickle_path, 'wb') as handle:
				pickle.dump(hipec_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
		# Filter out the data
		filtered_data = filter_patient_data(hipec_data)
		
		# Response if no data exists to meet all criteria; not yet implemented
		if len(filtered_data) == 0:
			return captured_data
		
		# Basic statistical data
		basic_stats = getStats(filtered_data)
		# Overall survival
		overall_survival = overall_survival_analysis(filtered_data)
		# Progression-free survival
		progression_free = progression_free_analysis(filtered_data)
		# Number of data points
		num_patients = len(filtered_data)
		
		# Filtering and processing of data
		today = datetime.date.today()
		hospital = get_all_hipec_data_of('HospitalStay', filtered_data)
		disposition = get_all_hipec_data_of('Disposition', filtered_data)
		disposition = home_disposition(disposition)
		readmission = get_all_hipec_data_of('Readmission', filtered_data)
		readmission = calc_readmit(readmission)
		morbidity = calc_morb_mort(True, filtered_data)
		mortality = calc_morb_mort(False, filtered_data)
		hospital_iqr = basic_stats['HospitalStay']['Q3'] - basic_stats['HospitalStay']['Q1']
		
		# Add processed data to dictionary to return
		captured_data.update({'today': today})
		captured_data.update({'HospitalHistogram': hospital})
		captured_data.update({'HospitalIQR': hospital_iqr})
		captured_data.update(
			{'HospitalMedian': basic_stats['HospitalStay']['median']}
		)
		captured_data.update({'OverallSurvival': overall_survival})
		captured_data.update({'ProgressionFree': progression_free})
		captured_data.update({'Disposition': disposition})
		captured_data.update({'Readmission': readmission})
		captured_data.update({'Morbidity': morbidity})
		captured_data.update({'Mortality': mortality})
		captured_data.update({'N': num_patients})
		
		return captured_data