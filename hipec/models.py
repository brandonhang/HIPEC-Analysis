from django.db import models
from django.forms import ModelForm
from django.utils.encoding import python_2_unicode_compatible
import datetime

class SurvivalAnalysis(models.Model):
	""" This function doesn't do anything meaningful outside of adding today's
	date. It serves as a placeholder for when an actual model is implemented
	to calculate results based on input.
	"""
	@staticmethod
	def dummy_function(captured_data):
		today = datetime.date.today()
		captured_data.update({'today': today})
		return captured_data