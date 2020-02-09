from django import froms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    passwd = forms.CharField(widget=forms.widget.PasswordInput())
