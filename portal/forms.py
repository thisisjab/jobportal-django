from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class JobCandidateProfileForm(forms.ModelForm):
    
    class Meta:
        model = models.JobCandidate
        fields = ['birth_date', 'short_bio', 'description']
        widgets = {
            'birth_date': DateInput()
        }


class EmployerProfileForm(forms.ModelForm):

    class Meta:
        model = models.Employer
        fields = ['short_bio']
