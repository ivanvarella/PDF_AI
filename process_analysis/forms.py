from django.forms import ModelForm
from .models import Process

class ProcessForm(ModelForm):
    class Meta:
        model = Process
        fields = ['arquivo']