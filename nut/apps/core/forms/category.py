from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Category, Sub_Category
from apps.core.forms import get_category_choices
from apps.core.utils.image import HandleImage

from django.utils.log import getLogger
from django.conf import settings

log = getLogger('django')
image_path = getattr(settings, 'MOGILEFS_MEDIA_URL', 'images/')


YES_OR_NO = (
    (1, _('yes')),
    (0, _('no')),
)


class CategoryForm(forms.Form):

    cover = forms.FileField(
        label=_('cover'),
        widget=forms.FileInput(),
        required=False,
    )

    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    def clean_status(self):
        _status = self.cleaned_data.get('status')
        return int(_status)


class CreateCategoryForm(CategoryForm):

    def save(self):
        _title = self.cleaned_data.get('title')
        _status = self.cleaned_data.get('status')
        _cover = self.cleaned_data.get('cover')
        # _status = int(_status)
        category = Category(
            title = _title,
            status = _status,
        )

        if _cover:
            # log.info("icon %s" % _cover)
            image_file = HandleImage(_cover)
            cover_file = image_file.save(path=image_path)
            category.cover = cover_file
        category.save()
        return category



class EditCategoryForm(CategoryForm):

    def __init__(self, category, *args, **kwargs):

        self.category_cache = category
        super(EditCategoryForm, self).__init__(*args, **kwargs)

    def save(self):

        _title = self.cleaned_data.get('title')
        _status = self.cleaned_data.get('status')
        _cover = self.cleaned_data.get('cover')
        # _status = int(_status)
        # print _status

        self.category_cache.title = _title
        self.category_cache.status = _status

        if _cover:
            log.info("icon %s" % _cover)
            image_file = HandleImage(_cover)
            cover_file = image_file.save(path=image_path)
            self.category_cache.cover = cover_file

        self.category_cache.save()

        return self.category_cache



class SubCategoryForm(forms.Form):
    title = forms.CharField(
        label=_('title'),
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )

    category = forms.ChoiceField(
        label=_('parent category'),
        choices=get_category_choices(),
        widget=forms.Select(attrs={'class':'form-control'})
    )

    status = forms.ChoiceField(
        label=_('status'),
        choices=YES_OR_NO,
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    icon = forms.ImageField(
        label=_('Select an Image'),
        required=False,
    )


class CreateSubCategoryForm(SubCategoryForm):

    def save(self):
        _title = self.cleaned_data.get('title')
        _category = self.cleaned_data.get('category')
        _icon = self.cleaned_data.get('icon')

        _status = self.cleaned_data.get('status')
        _status = int(_status)

        sub_category = Sub_Category(
            title = _title,
            group_id = _category,
            status = _status,
        )

        if _icon:
            image_file = HandleImage(_icon)
            icon_file = image_file.icon_save(path=image_path)
            sub_category.icon = icon_file

        sub_category.save()
        return sub_category


class EditSubCategoryForm(SubCategoryForm):

    def __init__(self, sub_category, *args, **kwargs):
        self.sub_category = sub_category
        super(EditSubCategoryForm, self).__init__(*args, **kwargs)

        # TODO: disable category cache
        self.fields['category'] = forms.ChoiceField(
            label=_('parent category'),
            choices=get_category_choices(),
            widget=forms.Select(attrs={'class':'form-control'})
        )

    def save(self):
        _title = self.cleaned_data.get('title')
        _category = self.cleaned_data.get('category')
        _icon = self.cleaned_data.get('icon')

        _status = self.cleaned_data.get('status')
        _status = int(_status)

        if _icon:
            log.info("icon %s" % _icon)
            image_file = HandleImage(_icon)
            icon_file = image_file.icon_save(path=image_path)
            self.sub_category.icon = icon_file

        self.sub_category.title = _title
        self.sub_category.group_id = _category
        self.sub_category.status = _status
        self.sub_category.save()



__author__ = 'edison'
