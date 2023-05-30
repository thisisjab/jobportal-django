from django.contrib import admin
from . import forms
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    add_form = forms.UserCreationForm
    form = forms.UserChangeForm
    model = models.User
    list_display = [
        'email',
        'username',
        'is_superuser',
        'is_employer',
        'is_job_candidate'
    ]

    def is_employer(self, user):
        return 'YES' if user.employer else 'NO'
        
    def is_job_candidate(self, user):
        return 'YES' if user.jobcandidate else 'NO'
