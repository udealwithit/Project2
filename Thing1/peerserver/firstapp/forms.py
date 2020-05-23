from django import forms
    
class AreaForm(forms.Form):
    current_area = forms.ChoiceField(choices = [('Area1', "New York"),('Area2', "Camden"),('Area3', "Holtsville"),('Area4', "Newark")])
