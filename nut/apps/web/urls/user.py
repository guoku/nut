from apps.management.views.entities import Add_local, EntitySKUCreateView
from apps.web.views.seller_management import SellerManagement, SellerManagementAddEntity
from django.conf.urls import url, patterns

from apps.web.views.user import UserIndex,\
                                UserLikeView, UserNoteView,\
                                UserTagView, UserArticleView,\
                                UserFansView, UserFollowingsView,\
                                UserPublishedArticleView,UserPublishedSelectionArticleView,\
                                UserLikeArticleView,\
                                UserSendVerifyMail,\
                                UserEntitiesView


from apps.web.views.user import ChangePasswdFormView

urlpatterns = patterns(
    'apps.web.views.user',
    url(r'^settings/$', 'settings', name='web_user_settings'),
    url(r'^change/password/$', ChangePasswdFormView.as_view(), name='web_user_change_password'),
    url(r'^bind/sns/$', 'bind_sns', name='web_user_bind_sns'),
    url(r'^upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),
    url(r'^sendverifymail/$', UserSendVerifyMail.as_view() , name='web_user_mail_verify'),
    # url(r'^seller_management/$', SellerManagement.as_view() , name='web_seller_management'),
    # url(r'^seller_management/entity_list/$', SellerManagement.as_view()),
    # url(r'^seller_management/add_entity/$', SellerManagementAddEntity.as_view() , name='web_seller_management_entity_add'),
    # url(r'^seller_management/(?P<entity_id>\d+)/new/$', EntitySKUCreateView.as_view(), name='management_entity_sku_create'),

    #url(r'^(?P<entity_id>\d+)/skus/$', SKUListView.as_view() , name='sku_list_management'),
    #url(r'^(?P<entity_id>\d+)/skus/new/$', SKUCreateView.as_view() , name='add_sku_management'),
    #url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/delete/$', SKUDeleteView.as_view(), name='sku_delete_management'),
    #url(r'^(?P<entity_id>\d+)/skus/(?P<pk>\d+)/update/$', SKUUpdateView.as_view(), name='sku_update_management'),


    # tmpl user page

    url(r'^(?P<user_id>\d+)/$', UserIndex.as_view(), name='web_user_index'),
    url(r'^(?P<user_id>\d+)/like/$', UserLikeView.as_view(), name='web_user_entity_like'),
    url(r'^(?P<user_id>\d+)/like/(?P<cid>\d+)/category/$', UserLikeView.as_view(), name='web_user_entity_like_by_category'),

    url(r'^(?P<user_id>\d+)/note/$', UserNoteView.as_view(), name='web_user_post_note'),
    url(r'^(?P<user_id>\d+)/tags/$', UserTagView.as_view(), name='web_user_tag'),

    url(r'^(?P<user_id>\d+)/articles/$', UserPublishedSelectionArticleView.as_view(), name='web_user_article'),

    url(r'^(?P<user_id>\d+)/articles/selection/$', UserPublishedSelectionArticleView.as_view(), name='web_user_article_selection'),
    url(r'^(?P<user_id>\d+)/articles/published/$', UserPublishedArticleView.as_view(), name='web_user_article_published'),
    # the list articles which the user likes
    url(r'^(?P<user_id>\d+)/articles/like/$', UserLikeArticleView.as_view(), name='web_user_article_like'),

    url(r'^(?P<user_id>\d+)/fans/$', UserFansView.as_view(), name='web_user_fans'),
    url(r'^(?P<user_id>\d+)/followings/$', UserFollowingsView.as_view(), name='web_user_followings'),


    # url(r'^(?P<user_id>\d+)/$',      'index', name='web_user_index' ),
    # url(r'^(?P<user_id>\d+)/like/$', 'entity_like', name='web_user_entity_like'),
    # url(r'^(?P<user_id>\d+)/note/$', 'post_note', name='web_user_post_note'),
    # url(r'^(?P<user_id>\d+)/tags/$', 'tag', name='web_user_tag'),
    # url(r'^(?P<user_id>\d+)/articles/$', 'articles', name='web_user_article'),
    url(r'^(?P<user_id>\d+)/tags/(?P<tag_name>\w+)/$', 'user_tag_detail', name='web_user_tag_detail'),
    # url(r'^(?P<user_id>\d+)/fans/$', 'fans', name='web_user_fans'),
    # url(r'^(?P<user_id>\d+)/followings/$', 'following', name='web_user_followings'),

    # Azure thinks the user's goods link below is an abandon link.
    url(r'^(?P<user_id>\d+)/goods/$', 'user_goods', name='web_user_goods'),
    # create a goods link for seller
    url(r'^(?P<user_id>\d+)/entities/$', UserEntitiesView.as_view(), name='web_user_entities'),


    url(r'^(?P<user_id>\d+)/follow/$', 'follow_action', name='web_user_follow_action'),
    url(r'^(?P<user_id>\d+)/unfollow/$', 'unfollow_action', name='web_user_unfollow_action'),
)



__author__ = 'edison'
