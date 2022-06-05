from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=255, required=True)
    is_part = forms.BooleanField(required=True)
    board_id = forms.IntegerField(min_value=1, required=True)
    board_type = forms.IntegerField(min_value=1, max_value=4, required=True)
    body = forms.CharField(min_length=15, required=True)

