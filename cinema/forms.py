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
        
from django import forms
from .models import SeatPlace

class BookingForm(forms.Form):
    seats = forms.ModelMultipleChoiceField(
        queryset=SeatPlace.objects.none(),  # Will be set in the view
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        show = kwargs.pop('show', None)
        super().__init__(*args, **kwargs)
        if show:
            self.fields['seats'].queryset = SeatPlace.objects.filter(hall=show.hall)