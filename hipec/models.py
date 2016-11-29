from django.db import models
from django.forms import ModelForm
from django.utils.encoding import python_2_unicode_compatible
import datetime
import os, re
import pandas, numpy
import pickle

class SurvivalAnalysis(models.Model):
	""" This function doesn't do anything meaningful outside of adding today's
	date. It serves as a placeholder for when an actual model is implemented
	to calculate results based on input.
	"""
	@staticmethod
	def dummy_function(captured_data):
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
						'Mortality90': mortality_90
					}
			
			return hipec_data
		''' End read_excel() '''
		
		''' Temporary helper function for testing '''
		def get_all_hipec_data_of(variable, master_data):
			data_list = []
			
			for p_id, patient in master_data.items():
				for op_id, operation in patient['HIPEC'].items():
					if variable in operation:
						if operation[variable] is not None:
							data_list.append(operation[variable])
			
			sorted(data_list)
			return data_list
		''' End get_all_hipec_data_of() '''
		
		''' Test function to return hospital length of stay '''
		def sample_hospital_length_of_stay(data_list):
			q1 = numpy.percentile(data_list, 25)
			median = numpy.percentile(data_list, 50)
			q3 = numpy.percentile(data_list, 75)
			
			return {'Median': median, 'Q1': q1, 'Q3': q3}
		''' End sample_hospital_length_of_stay() '''
		
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
				if boolean not in answer:
					answer[boolean] = 1
				else:
					answer[boolean] += 1
			
			return answer
		''' End sample_yes_no_answer() '''
		
		modded = int(os.path.getmtime('hipec\\data\\HIPEC_data.xlsx'))
		modded = str(modded)
		pickle_path = 'hipec\\data\\hipec_data-' + modded + '.pickle'
		
		try:
			with open(pickle_path, 'rb') as handle:
				hipec_data = pickle.load(handle)
		except IOError:
			hipec_data = filter_excel()
			
			with open(pickle_path, 'wb') as handle:
				pickle.dump(hipec_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
		
		today = datetime.date.today()
		hospital_hist = get_all_hipec_data_of('HospitalStay', hipec_data)
		hospital = sample_hospital_length_of_stay(hospital_hist)
		disposition = get_all_hipec_data_of('Disposition', hipec_data)
		disposition = sample_disposition_status(disposition)
		readmission = get_all_hipec_data_of('Readmission', hipec_data)
		readmission = sample_yes_no_answer(readmission)
		morbidity = get_all_hipec_data_of('Morbidity90', hipec_data)
		morbidity = sample_yes_no_answer(morbidity)
		mortality = get_all_hipec_data_of('Mortality90', hipec_data)
		mortality = sample_yes_no_answer(mortality)
		captured_data.update({'today': today})
		captured_data.update({'HospitalHistogram': hospital_hist})
		captured_data.update({'HospitalRange': hospital})
		captured_data.update({'Disposition': disposition})
		captured_data.update({'Readmission': readmission})
		captured_data.update({'Morbidity': morbidity})
		captured_data.update({'Mortality': mortality})
		
		return captured_data