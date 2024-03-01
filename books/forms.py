from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    age = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        UserProfile.objects.create(
            user=user,
            avatar=self.cleaned_data['avatar'],
            age=self.cleaned_data['age']
        )

        return user



class UserForm(UserChangeForm):
    password = None  # Remove password field from the form

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'age')
