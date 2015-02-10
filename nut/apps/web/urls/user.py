from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.web.views.user',
    url(r'^settings/$', 'settings', name='web_user_settings'),
    url(r'^change/password/$', 'change_password', name='web_user_change_password'),
    url(r'^upload/avatar/$', 'upload_avatar', name='web_user_upload_avatar'),

    url(r'^(?P<user_id>\d+)/$', 'index', name='web_user_index' ),
    url(r'^(?P<user_id>\d+)/like/$', 'entity_like', name='web_user_entity_like'),
    url(r'^(?P<user_id>\d+)/note/$', 'post_note', name='web_user_post_note'),
    url(r'^(?P<user_id>\d+)/tags/$', 'tag', name='web_user_tag'),
    url(r'^(?P<user_id>\d+)/tags/(?P<tag_hash>\w+)/$', 'user_tag_detail', name='web_user_tag_detail'),
    url(r'^(?P<user_id>\d+)/fans/$', 'fans', name='web_user_fans'),
    url(r'^(?P<user_id>\d+)/followings/$', 'following', name='web_user_followings'),

    url(r'^(?P<user_id>\d+)/follow/$', 'follow_action', name='web_user_follow_action'),
    url(r'^(?P<user_id>\d+)/unfollow/$', 'unfollow_action', name='web_user_unfollow_action'),
)



__author__ = 'edison'
