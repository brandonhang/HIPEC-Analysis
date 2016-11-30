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
	core_karnofsky__upper = forms.IntegerField()
	core_karnofsky__lower = forms.IntegerField()
	core_peritoneal__upper = forms.IntegerField()
	core_peritoneal__lower = forms.IntegerField()
	core_cytoreduction = forms.IntegerField()
	
	# Demographics
	dem_gender = forms.CharField(max_length=8, required=False)
	dem_race = forms.CharField(max_length=32, required=False)
	enable_dem_bmi = forms.IntegerField(required=False)
	dem_bmi__upper = forms.IntegerField(required=False)
	dem_bmi__lower = forms.IntegerField(required=False)
	dem_asa = forms.IntegerField(required=False)
	dem_depression = forms.CharField(max_length=4, required=False)
	dem_beta_block = forms.CharField(max_length=4, required=False)
	dem_antidepr = forms.CharField(max_length=4, required=False)
	dem_smoker = forms.CharField(max_length=4, required=False)
	dem_smoke_status = forms.CharField(max_length=16, required=False)
	enable_dem_smoke_pack = forms.IntegerField(required=False)
	dem_smoke_pack__upper = forms.IntegerField(required=False)
	dem_smoke_pack__lower = forms.IntegerField(required=False)

def hipec_app(request):
	if request.method == 'POST':
		form = HipecVariables(request.POST)
		
		if form.is_valid():
			results = SurvivalAnalysis.filter_data(form.cleaned_data)
			return render(request, 'hipec/results.html', {'results': results})
	
	else:
		form = HipecVariables()
	
	return render(request, 'hipec/index.html', {'form': form})