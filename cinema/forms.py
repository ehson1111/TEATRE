from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Парол', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Такрори парол', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'age']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Паролҳо мувофиқат намекунанд")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
