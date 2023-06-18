from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm, UserChangeForm as DefaultUserChangeForm


class UserCreationForm(DefaultUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class UserChangeForm(DefaultUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
