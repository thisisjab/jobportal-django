from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm, UserChangeForm as DefaultUserChangeForm


class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
