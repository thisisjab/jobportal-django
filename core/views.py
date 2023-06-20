from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, View
from django.core.mail import send_mail
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
from . import forms


class SignUpView(FormView):
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('confirm_email')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)
        return super(SignUpView,self).form_valid(form)


class ConfirmEmailView(TemplateView):
    template_name = 'registration/confirm_your_email.html'


class ActivateView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('activate_successful')
        else:
            return redirect('login')


class ActivateSuccuessfulView(TemplateView):
    template_name = 'registration/email_confirmation_successful.html'
