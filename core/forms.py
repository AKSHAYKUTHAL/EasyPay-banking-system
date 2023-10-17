from django import forms
from core.models import CreditCard

class CreditCardForm(forms.ModelForm):

    class Meta:
        model = CreditCard
        fields = [ 'card_type','card_tier']