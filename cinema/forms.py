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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'age']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'age']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Email',
            'full_name': 'Full Name',
            'phone_number': 'Phone Number',
            'age': 'Age',
        }
        help_texts = {
            'email': 'Please enter a valid email address.',
            'full_name': 'Enter your full name.',
            'phone_number': 'Enter your phone number.',
            'age': 'Enter your age.',
        }
        error_messages = {
            'email': {
                'required': 'Email is required.',
                'invalid': 'Enter a valid email address.',
            },
            'full_name': {
                'required': 'Full name is required.',
            },
            'phone_number': {
                'required': 'Phone number is required.',
            },
            'age': {
                'required': 'Age is required.',
                'invalid': 'Enter a valid age.',
            },
        }        
        
        
from django import forms
from .models import Hall, Show, SeatPlace


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name']


class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['movie', 'showing_date', 'showing_time', 'hall']


class SeatPlaceForm(forms.ModelForm):
    class Meta:
        model = SeatPlace
        fields = ['name', 'hall', 'status', 'price']
