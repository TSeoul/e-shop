from django import forms

class OrderForm(forms.Form):
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    first_name = forms.CharField(label='First Name', max_length=50, required=True)
    email = forms.EmailField(label='Email', required=True)
    address = forms.CharField(label='Address', max_length=250, required=True)
    city = forms.CharField(label='City', max_length=100, required=True)
    postal_code = forms.CharField(label='Postal code', max_length=20, widget=forms.NumberInput)
    state = forms.CharField(label='State', max_length=100, widget=forms.TextInput)
    payment_option = forms.CharField(label='Payment Option', max_length=20, required=True)


