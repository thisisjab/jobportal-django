from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms


class SignUpView(CreateView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        return super(SignUpView,self).form_valid(form)
