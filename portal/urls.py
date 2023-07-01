from django.urls import path
from . import views


app_name = 'portal'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/jobcandidate/create', views.JobCandidateProfileCreateView.as_view(), name='jobcandidate_create'),
    path('profile/jobcandidate/<int:pk>/update', views.JobCandidateProfileUpdateView.as_view(), name='jobcandidate_update')
]
