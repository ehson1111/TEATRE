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
        fields = ['seat_number', 'hall', 'is_available', 'price']
