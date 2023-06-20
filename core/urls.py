from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('confirm_your_email', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('activate/<uidb64>/<token>', views.ActivateView.as_view(), name='activate'),
    path(
        'activate/successful/',
        views.ActivateSuccuessfulView.as_view(),
        name='activate_successful',
    ),
]
