from django.urls import path

from .views import (
    RegisterView,
    ResetPasswordView,
    ResetPasswordDoneView,
    ResetPasswordConfirmView,
    ResetPasswordCompleteView,
    LoginEmailView,
)

app_name = "profiles"

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration_user"),
    path("login/", LoginEmailView.as_view(), name="login"),

    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path("password-reset-sent/", ResetPasswordDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", ResetPasswordConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", ResetPasswordCompleteView.as_view(), name="password_reset_complete"),
]
