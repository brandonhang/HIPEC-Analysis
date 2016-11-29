from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from hipec.models import SurvivalAnalysis
from django import forms

class HipecVariables(forms.Form):
	# Registry
	registry_name = forms.CharField(max_length=64, required=False)
	registry_dob = forms.DateField(required=False)
	
	# Core Variables
	core_primary_tumor = forms.CharField(max_length=64)
	core_age__upper = forms.IntegerField()
	core_age__lower = forms.IntegerField()
	core_charlson__upper = forms.IntegerField()
	core_charlson__lower = forms.IntegerField()
	core_karnofsky = forms.IntegerField()
	core_peritoneal__upper = forms.IntegerField()
	core_peritoneal__lower = forms.IntegerField()
	core_cytoreduction = forms.IntegerField()

def hipec_app(request):
	if request.method == 'POST':
		form = HipecVariables(request.POST)
		
		if form.is_valid():
			results = SurvivalAnalysis.dummy_function(form.cleaned_data)
			return render(request, 'hipec/results.html', {'results': results})
	
	else:
		form = HipecVariables()
	
	return render(request, 'hipec/index.html', {'form': form})