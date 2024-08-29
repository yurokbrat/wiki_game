from django import forms


class StartGameForm(forms.Form):
    start_article = forms.CharField(max_length=255, required=True)
    end_article = forms.CharField(max_length=255, required=True)
