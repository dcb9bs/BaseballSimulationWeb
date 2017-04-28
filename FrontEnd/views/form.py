from django import forms


class TeamForm(forms.Form):
    team_name = forms.CharField(label="Year and Team Name", max_length=100, required=True)
    professional = forms.BooleanField(initial=False, required=False)


class PlayerForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)
