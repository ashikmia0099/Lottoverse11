from django import forms

class TransferForm(forms.Form):
    
    transferd_username = forms.CharField(label= 'Give me Transferd metamask account number', widget= forms.TextInput(attrs={'class': 'form-control mb-4'}))
    amount = forms.DecimalField(label='Transfer Amount', widget=forms.NumberInput(attrs={'class':'form-control'}))



class DepositeForm(forms.Form):
    amount = forms.DecimalField()