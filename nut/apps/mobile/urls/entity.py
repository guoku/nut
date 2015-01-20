from django.conf.urls import url, patterns


urlpatterns = patterns(
    'apps.mobile.views.entity',
    url(r'^$', 'entity_list', name='mobile_entity_list'),
    url(r'^guess/$', 'guess', name='mobile_entity_guess'),
    url(r'^(?P<entity_id>\d+)/$', 'detail', name='mobile_entity_detail'),
    url(r'^(?P<entity_id>\d+)/like/(?P<target_status>\d+)/$', 'like_action', name='mobile_entity_like_action'),

    # url(r'^note/$', 'note', name='mobile_entity_note'),

)

urlpatterns += patterns(
    'apps.mobile.views.note',
    url(r'^note/(?P<note_id>\d+)/$', 'detail', name='mobile_entity_note'),
    url(r'(?P<entity_id>\w+)/add/note/$', 'post_note', name='mobile_post_note'),
    url(r'^note/(?P<note_id>\d+)/poke/(?P<target_status>\d+)/$', 'poke', name='mobile_note_poke'),
)


__author__ = 'edison'
