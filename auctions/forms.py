from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Listing

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['owner', 'date', 'watchlist']
