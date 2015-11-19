from apps.mobile.models import LaunchBoard
from django import forms
from django.utils.translation import gettext_lazy as _


class LaunchBoardForm(forms.Form):
    YES_OR_NO = (
        (0, _('no')),
        (1, _('yes')),
    )

    launchImage = forms.FileField(widget=forms.FileInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    action = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    status = forms.ChoiceField(
        label=_('enable'),
        choices=YES_OR_NO,
        widget=forms.Select( attrs={'class':'form-control'}, ),
        required=False,
        help_text=_(''),
        initial=0,
    )

    def save(self):
        pass



__author__ = 'edison7500'
