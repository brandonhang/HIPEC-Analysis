from django.db import models
from django.forms import ModelForm
from django.utils.encoding import python_2_unicode_compatible
import datetime
import os, re
import pandas, numpy
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
			data = pandas.read_excel('hipec\\data\\HIPEC_data.xlsx')
			regex = re.compile('CC-[0-2]')
			
			for row_index, row in data.iterrows():
				p_id = row['HIPEC Study ID']
				data_type = row['Event Name']
				
				''' Registry info not yet implemented.  Keeping in
				source code via a commented out conditional as a
				reminder that it will need to be implemented as the
				next step in patient data filtering '''
				# Build demographic information
				'''if 'Registry' in data_type:
					'''
				# Build HIPEC information
				#else:
				if 'Registry' not in data_type:
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
					
					# Additional data for survival calculations
					s_time = row['Survival time from Surgery']
					vitals = row['Vital Status at analysis/SSDI']
					
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
						'HospitalStay': hospital_stay,
						'Disposition': str(disposition),
						'Readmission': readmission,
						'Morbidity30': morbidity_30,
						'Morbidity60': morbidity_60,
						'Morbidity90': morbidity_90,
						'Mortality30': mortality_30,
						'Mortality60': mortality_60,
						'Mortality90': mortality_90,
						'SurvivalTime': survival_t,
						'VitalStatus': vital_stat
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
		
		def sample_disposition_status(data_list):
			dispo = {}
			
			for disp in data_list:
				if disp not in dispo:
					dispo[disp] = 1
				else:
					dispo[disp] += 1
			
			return dispo
		''' End sample_disposition_status() '''
		
		''' Test function to return readmission, morbidity, and mortality '''
		def sample_yes_no_answer(data_list):
			answer = {}
			
			for boolean in data_list:
				bool_key = ''
				
				if boolean == True:
					bool_key = 'Yes'
				elif boolean == False:
					bool_key = 'No'
				else:
					bool_key = 'NoData'
				
				if bool_key not in answer:
					answer[bool_key] = 1
				else:
					answer[bool_key] += 1
			
			return answer
		''' End sample_yes_no_answer() '''
		
		''' Filters out and returns patient information based on the core
		variable parameters. '''
		def filter_patient_data(data):
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
						and op_data['KPS'] == captured_data['core_karnofsky'] \
						and op_data['PCI'] >= captured_data['core_peritoneal__lower'] \
						and op_data['PCI'] <= captured_data['core_peritoneal__upper'] \
						and op_data['CC'] == captured_data['core_cytoreduction']:
						
						filtered[(p_id, op_num)] = op_data
			
			return filtered
		''' End filter_patient_data() '''
		
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
		
		# A lot of the values below are used more for testing proof-of-concept
		today = datetime.date.today()
		hospital = get_all_hipec_data_of('HospitalStay', filtered_data)
		disposition = get_all_hipec_data_of('Disposition', filtered_data)
		disposition = sample_disposition_status(disposition)
		readmission = get_all_hipec_data_of('Readmission', filtered_data)
		readmission = sample_yes_no_answer(readmission)
		morbidity = get_all_hipec_data_of('Morbidity90', filtered_data)
		morbidity = sample_yes_no_answer(morbidity)
		mortality = get_all_hipec_data_of('Mortality90', filtered_data)
		mortality = sample_yes_no_answer(mortality)
		captured_data.update({'today': today})
		captured_data.update({'HospitalHistogram': hospital})
		captured_data.update({'HospitalRange': hospital})
		captured_data.update({'Disposition': disposition})
		captured_data.update({'Readmission': readmission})
		captured_data.update({'Morbidity': morbidity})
		captured_data.update({'Mortality': mortality})
		
		return captured_data