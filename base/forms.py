from django.forms import ModelForm
from .models import Room



class RoomForm(ModelForm):
    class Meta:
        model = Room
        # use full models inputs
        # fields = '__all__'
        fields = '__all__'
        exclude = ["host","participants"]

