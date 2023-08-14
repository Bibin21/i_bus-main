from django import forms
from .models import BusStop, UserBusPass

class BookPassForm(forms.ModelForm):
    """
    Form for Booking Bus Pass
    """

    def __init__(self, *args, **kwargs):
        bus = kwargs.pop('bus')
        super(BookPassForm, self).__init__(*args, **kwargs)

        self.fields['boarding_point'].queryset = BusStop.objects.filter(bus=bus)
        self.fields['boarding_point'].label = "Select Boarding Point"

        self.fields['expire_at'].label = "Book Pass Till"

    expire_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}))

    class Meta:
        """Model with fields in form."""

        model = UserBusPass
        fields = (
            'boarding_point', 'expire_at'
        )
    