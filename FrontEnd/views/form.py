from django import forms


class TeamForm(forms.Form):
    team_name = forms.CharField(label="Year and Team Name", max_length=100, required=True)
    professional = forms.BooleanField(initial=False, required=False)


class PlayerForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100, required=True)
    last_name = forms.CharField(label="Last Name", max_length=100, required=True)


class PitcherForm(forms.Form):
    opponents_free_bases = forms.IntegerField(min_value=0)
    opponents_singles = forms.IntegerField(min_value=0)
    opponents_doubles = forms.IntegerField(min_value=0)
    opponents_triples = forms.IntegerField(min_value=0)
    opponents_homeruns = forms.IntegerField(min_value=0)
    opponents_strikeouts = forms.IntegerField(min_value=0)
    opponents_at_bats = forms.IntegerField(min_value=0)


class BatterForm(forms.Form):
    free_bases = forms.IntegerField(min_value=0)
    singles = forms.IntegerField(min_value=0)
    doubles = forms.IntegerField(min_value=0)
    triples = forms.IntegerField(min_value=0)
    homeruns = forms.IntegerField(min_value=0)
    strikeouts = forms.IntegerField(min_value=0)
    at_bats = forms.IntegerField(min_value=0)
