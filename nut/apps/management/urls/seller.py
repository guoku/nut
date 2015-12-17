from django.conf.urls import url, patterns

from apps.seller.views.management import SellerCreateView, SellerListView, SellerUpdateView
urlpatterns = patterns(
    '',
    url(r'^/$', SellerListView.as_view() , name='management_seller_list'),
    url(r'^edit/(?P<eid>\d+)/$', SellerUpdateView.as_view() , name='management_seller_update'),
    url(r'^new/$', SellerCreateView.as_view() , name='management_seller_create'),
)