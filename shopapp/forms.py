from django import forms

class CustomerForm(forms.Form):
    customer_name = forms.CharField(label='Customer Name', max_length=100)
    customer_mobile = forms.CharField(label='Customer Mobile', max_length=20)
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('online', 'Online'),
    )
    payment_mode = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
