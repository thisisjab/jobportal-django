from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('confirm_your_email', views.ConfirmEmailView.as_view(), name='confirm_email'),
    path('activate/<uidb64>/<token>', views.ActivateView.as_view(), name='activate')
]
