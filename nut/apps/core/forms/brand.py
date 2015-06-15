from django import forms
from django.utils.translation import gettext_lazy as _
from apps.core.models import Brand
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
#
# from apps.core.utils.image import HandleImage
#
# from django.conf import settings
#
# image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


class BrandForm(forms.Form):

    icon = forms.FileField(
        label=_('icon'),
        widget=forms.FileInput(),
        required=False,
    )

    name = forms.CharField(
        label=_('brand name'),
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    alias = forms.CharField(
        label=_('alias'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('optional'),
        required=False,
    )

    national = forms.CharField(
        label=_('national'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        # required=False,
    )

    company = forms.CharField(
        label=_('company'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text=_('optional'),
        required=False,
    )

    website = forms.URLField(
        label=_('website'),
        widget=forms.URLInput(attrs={'class':'form-control'}),
        required=False,
    )

    status = forms.ChoiceField(label=_('status'),
                                choices=Brand.BRAND_STATUS_CHOICES,
                                widget=forms.Select(attrs={'class':'form-control'}),
                                initial=Brand.pending,
                                help_text=_('status'))

    intro = forms.CharField(
        label=_('intro'),
        widget=forms.Textarea(attrs={'class':'form-control'}),
        # min_length=300,
        max_length=500,
        required=False,
    )

    def clean_name(self):
        _name = self.cleaned_data.get('name')
        return _name.strip(' \t\n\r')

    def cleaned_alias(self):
        _alias = self.cleaned_data.get('alias')
        return _alias.strip(' \t\n\r')

    def cleaned_national(self):
        _national = self.cleaned_data.get('national')
        return _national.strip(' \t\n\r')

    def cleaned_company(self):
        _company = self.cleaned_data.get('company')
        return _company.strip(' \t\n\r')

    def clean_intro(self):
        _intro = self.cleaned_data.get('intro')
        return _intro.strip(' \t\n\r')

    #
    # def __init__(self, brand, *args, **kwargs):
    #     self.brand_cache = brand
    #     super(BrandForm, self).__init__(*args, **kwargs)

    def save(self):

        pass


__author__ = 'edison'
