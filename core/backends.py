from django.contrib.auth import backends, get_user_model
from django.db.models import Q

class AuthenticationBackend(backends.ModelBackend):
    """
    Custom authentication backend for logging in using email or username 
    with password
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        try:
            UserModel = get_user_model()
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            print(user.username, "FIND USER!!!")
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
    # def authenticate(self, username=None, password=None, **kwargs):
    #     UserModel = get_user_model()
    #     user = UserModel.objects.get(
    #         Q(username__iexact=username) | Q(email__iexact=username))
    #     if user.check_password(password):
    #         return user


    # def get_user(self, user_id):
    #     UserModel = get_user_model()
    #     try:
    #         return UserModel.objects.get(pk=user_id)
    #     except UserModel.DoesNotExist:
    #         return None
