from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from hipec.models import SurvivalAnalysis
from django import forms

class HipecVariables(forms.Form):
	# Core Variables
	primary_tumor = forms.CharField(max_length = 64)
	age = forms.IntegerField()
	charlson_co_morbidity = forms.IntegerField()
	karnofsky_performance = forms.IntegerField()
	peritoneal_carcinomatosis = forms.IntegerField()
	cytoreduction_completeness = forms.IntegerField()

def hipec_app(request):
	if request.method == 'POST':
		form = HipecVariables(request.POST)
		
		if form.is_valid():
			results = SurvivalAnalysis.dummy_function(form.cleaned_data)
			return render(request, 'hipec/results.html', {'results': results})
	
	else:
		form = HipecVariables()
	
	return render(request, 'hipec/index.html', {'form': form})