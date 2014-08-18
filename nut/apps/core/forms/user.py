from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.log import getLogger

log = getLogger('django')


from apps.core.models import User_Profile

class UserForm(forms.Form):
    YES_OR_NO = (
        (True, _('yes')),
        (False, _('no')),
    )
    user_id = forms.CharField(label=_('user_id'),
                              widget=forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
                              help_text=_(''))
    email = forms.EmailField(label=_('email'),
                             widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
                             help_text=_(''))
    nickname = forms.CharField(label=_('nickname'),
                               widget=forms.TextInput(attrs={'class':'form-control'}),
                               help_text=_(''))
    is_active = forms.ChoiceField(label=_('active'),
                                    choices=YES_OR_NO,
                                    widget=forms.Select(attrs={'class':'form-control'}),
                                    help_text=_(''))
    gender = forms.ChoiceField(label=_('gender'),
                                choices=User_Profile.GENDER_CHOICES,
                                widget=forms.Select(attrs={'class':'form-control'}),
                               help_text=_(''))
    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'class':'form-control'}),
                          help_text=_(''))
    website = forms.URLField(label=_('website'),
                             widget=forms.TextInput(attrs={'class':'form-control'}),
                             help_text=_(''))
    def save(self):
        _user_id = self.cleaned_data['user_id']
        # user = GKUser.objects.get(pk = _user_id)
        user = get_user_model()._default_manager.get(pk = _user_id)
        log.info(user)

__author__ = 'edison'
