from django.db import models
from django.db.models import Q
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
# import random


class GKUserQuerySet(models.query.QuerySet):
    def writer(self):
        return self.filter(is_active=3)

    def editor(self):
        return self.filter(is_active=2)

    def editor_or_admin(self):
        return self.filter(Q(is_admin=1)| Q(is_active=2))

    def active(self):
        return self.filter(is_active=1)

    def blocked(self):
        return self.filter(is_active=0)

    def deactive(self):
        return self.filter(is_active=-1)

    def admin(self):
        return self.filter(is_admin=True)


class GKUserManager(BaseUserManager):

    def get_queryset(self):
        return GKUserQuerySet(self.model, using = self._db)

    def writer(self):
        return self.get_queryset().writer()

    def editor(self):
        return self.get_query_set().editor()

    def active(self):
        return self.get_query_set().active()

    def blocked(self):
        return self.get_query_set().blocked()

    def deactive(self):
        return self.get_query_set().deactive()

    def deactive_user_list(self):
        user_list = cache.get('deactive_user_list')
        if user_list:
            return user_list

        user_list = self.get_query_set().deactive().values_list('id', flat=True)
        cache.set('deactive_user_list', user_list, timeout=86400)
        return user_list


    def admin(self):
        return self.get_query_set().admin()

    def editor_or_admin(self):
        return self.get_query_set().editor_or_admin()

    def _create_user(self, email, password, is_active, is_admin, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError(_('please given email'))

        user = self.model(email=email, is_active=is_active, is_admin=is_admin, date_joined=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, is_active=1, **extra_fields):

        is_admin = extra_fields.pop("is_admin", False)
        return self._create_user(email, password, is_active, is_admin, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

__author__ = 'edison7500'
