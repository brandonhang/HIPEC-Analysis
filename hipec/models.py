from django.db import models
from django.forms import ModelForm
from django.utils.encoding import python_2_unicode_compatible
import datetime
import os
import re
import pandas

class SurvivalAnalysis(models.Model):
	""" This function doesn't do anything meaningful outside of adding today's
	date. It serves as a placeholder for when an actual model is implemented
	to calculate results based on input.
	"""
	@staticmethod
	def dummy_function(captured_data):
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
					readmission = True if readmit == 'Yes' else False
					
					# Attempt to enforce data type
					try:
						hospital_stay = int(hospital_stay)
					except ValueError:
						hospital_stay = None
					
					# Morbidity and mortality -> booleans
					morb_30 = row['Morbidity < 30Days']
					morb_60 = row['Morbidity 31 to 60 days']
					morb_90 = row['Morbidty 61 to 90days']
					morbidity_30 = True if morb_30 == 'Yes' else False
					morbidity_60 = True if morb_60 == 'Yes' else False
					morbidity_90 = True if morb_90 == 'Yes' else False
					
					mort_30 = row['Mortality at < 30 days']
					mort_60 = row['Mortality at 31 to 60 Days']
					mort_90 = row['Mortality at 61 to 90 Days']
					mortality_30 = True if mort_30 == 'Yes' else False
					mortality_60 = True if mort_60 == 'Yes' else False
					mortality_90 = True if mort_90 == 'Yes' else False
					
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
		
		hipec_data = filter_excel()
		today = datetime.date.today()
		captured_data.update({'today': today})
		return captured_data