from django.conf.urls import url, patterns
from apps.site_banner.views.management import  SiteBannerCreateView, SiteBannerDeleteView, \
                                       SiteBannerUpdateView, SiteBannerSaveView, SiteBannerActiveListView, \
                                       SiteBannerInactiveListView


# this file' name should be management.py, see shop app for reference

urlpatterns = patterns(
    '',
    url(r'^banners/$', SiteBannerActiveListView.as_view(), name='manage_sitebanners'),
    url(r'^banners/new/$', SiteBannerCreateView.as_view(), name='manage_sitebanners_create'),
    url(r'^banners/(?P<pk>\d+)/update/$', SiteBannerUpdateView.as_view(), name='manage_sitebanners_update'),
    url(r'^banners/(?P<pk>\d+)/delete/$', SiteBannerDeleteView.as_view(), name='manage_sitebanners_delete'),
    url(r'^banners/save/$', SiteBannerSaveView.as_view(), name='manage_sitebanners_save'),
    url(r'^banners/active/$', SiteBannerActiveListView.as_view(), name='manage_sitebanners_active_list'),
    url(r'^banners/inactive/$', SiteBannerInactiveListView.as_view(), name='manage_sitebanners_inactive_list'),
    )