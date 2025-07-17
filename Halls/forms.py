from django import forms
from .models import Shar
from .models import Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client
from .models import Halls



# نموذج إضافة تعليق (Shar)
class SharForm(forms.ModelForm):
    class Meta:
        model = Shar
        fields = ['name', 'email', 'body']

# نموذج إضافة أو تعديل قاعة (Halls)
class HallForm(forms.ModelForm):
    class Meta:
        model = Halls
        fields = ['name', 'capacity', 'price', 'address', 'body', 'photo']

