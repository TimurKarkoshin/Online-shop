from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from profiles.models import avatar_upload_path


class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователя"""

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "group",
            "email",
        )

    def clean_email(self):
        """Проверка email на уникальность"""

        email = self.cleaned_data.get("email").strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(_("Такая почта уже зарегистрированная"))

        return email


class EmailAuthenticationForm(forms.Form):
    """Форма аутентификации пользователя с помощью email"""

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        user = self.authenticate_email()
        if not user:
            raise forms.ValidationError(_("Вы ввели не корректные данные."))
        else:
            self.user = user
        return self.cleaned_data

    def authenticate_user(self):
        """Аутентификации пользователя"""

        return authenticate(username=self.user.email, password=self.cleaned_data.get("password"))

    def authenticate_email(self):
        """Возвращает объект пользователя, если он аутентифицирован, иначе None"""

        email = self.cleaned_data.get("email", None)
        if email:
            try:
                user = User.objects.get(email__iexact=email)  # получаем объект пользователя по email
                if user.check_password(self.cleaned_data.get("password", "")):
                    return user
            except ObjectDoesNotExist:
                return None
        return None


class UserForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """

    regex_phone = RegexValidator(
        regex=r"^((8|\+7|)(\d{10}))$", message=_("Формат номера телефона должен быть: +79999999999 или 89999999999")
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "value": "",
                    "type": "text",
                    "data-validate": "require",
                    "placeholder": "Имя",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "value": "",
                    "type": "text",
                    "data-validate": "require",
                    "placeholder": "Фамилия",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "name": "mail",
                    "type": "text",
                    "value": "send@test.test",
                    "data-validate": "require",
                }
            ),
        }

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "name": "avatar",
                "data-validate": "onlyImgAvatar",
                "url_to_upload": avatar_upload_path,
            }
        ),
        required=False,
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "name": "phone",
                "type": "text",
                "value": "+70000000000",
                "data-validate": [regex_phone],
            }
        ),
        required=False,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "name": "password1",
                "type": "password",
                "placeholder": "Тут можно изменить пароль",
            }
        ),
        required=False,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "name": "password",
                "type": "password",
                "placeholder": "Введите пароль повторно",
            }
        ),
        required=False,
    )

    def clean_email(self):
        """Проверка email на уникальность"""

        email = self.cleaned_data.get("email").strip()

        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise ValidationError(_("Такая почта уже зарегистрированная"))
        return email
