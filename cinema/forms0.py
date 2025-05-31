from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Review, Order, SeatPlace

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number', 'age', 'password1', 'password2')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('star', 'description')
        widgets = {
            'star': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.Form):
    seats = forms.ModelMultipleChoiceField(
        queryset=SeatPlace.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Выберите места'
    )

    def __init__(self, *args, **kwargs):
        show = kwargs.pop('show', None)
        super().__init__(*args, **kwargs)
        if show:
            # Показываем места, которые доступны в зале конкретного шоу
            self.fields['seats'].queryset = SeatPlace.objects.filter(hall=show.hall, is_available=True)
