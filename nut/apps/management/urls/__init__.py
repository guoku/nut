from django.conf.urls import url, patterns, include
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    'apps.management',
    url(r'^$', RedirectView.as_view(url='/management/dashboard/')),

    url(r'^restful/', include('apps.management.urls.restful')),


    url(r'^dashboard/$', 'views.dashboard', name='management_dashboard'),
    url(r'^selection/', include('apps.management.urls.selection')),
    url(r'^selection_report/', include('apps.management.urls.selection_report')),
    url(r'^entity/', include('apps.management.urls.entities')),
    url(r'^buy-link/', include('apps.management.urls.buy_link')),
    url(r'^user/', include('apps.management.urls.users')),
    url(r'^banner/', include('apps.management.urls.banner')),
    url(r'^note/', include('apps.management.urls.note')),
    url(r'^comment/', include('apps.management.urls.comments')),
    url(r'^edm/', include('apps.management.urls.edm')),
    # url(r'^seller/', include('apps.management.urls.seller')),
    url(r'^seller/', include('apps.seller.urls.management')),


    # TODO: launch image at mobile
    url(r'^marketing/', include('apps.management.urls.marketing')),


    url(r'^brand/', include('apps.management.urls.brand')),
    url(r'^category/', include('apps.management.urls.category')),
    url(r'^t/', include('apps.management.urls.tags')),

    url(r'^article/', include('apps.management.urls.article')),
    url(r'^media/', include('apps.management.urls.media')),

    url(r'^event/', include('apps.management.urls.event')),
    url(r'^event-banner/', include('apps.management.urls.event_banner')),
    url(r'^recommend/', include('apps.management.urls.recommendation')),

    url(r'^search/', include('apps.management.urls.search')),

    url(r'^report/', include('apps.management.urls.report')),

    url(r'^shop/', include('apps.shop.urls.management')),
    url(r'^wechat/', include('apps.wechat.urls.management')),
    url(r'^order_management/', include('apps.order.urls.order_manage')),
    url(r'^sitebanner/', include('apps.site_banner.urls.management')),
    url(r'^top_ad/', include('apps.top_ad.urls.management')),
    url(r'^push/', include('apps.notifications.urls.management')),
    url(r'^editor_report/', include('apps.management.urls.editor_report')),
    url(r'^offline_shop/', include('apps.offline_shop.urls_manage')),
    url(r'^operation_report/', include('apps.management.urls.operation_report')),

    # TODO: entity recommendation from taobao
    url(r'^tbrecommend/', include('apps.management.urls.tbrecommend')),

    # TODO: statistics
    url(r'^statistics/', include('apps.management.urls.statistics')),
)

urlpatterns += patterns(
    'apps.management.views.account',
    url(r'^login/$', 'sign_in', name='management_sign_in'),
)

__author__ = 'edison7500'
