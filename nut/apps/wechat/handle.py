# coding=utf-8
# from apps.wechat.models import Robots
from apps.core.models import Entity, Selection_Entity, Entity_Like
from apps.wechat.models import Token
from datetime import datetime
from django.utils.log import getLogger
from haystack.query import SearchQuerySet

log = getLogger('django')


def handle_reply(content):
    # log.info(content.decode('utf-8'))
    res = list()

    if content.decode('utf-8') == u'精选':
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)

        for row in entities[:5]:
            res.append(row.entity)
    elif content.decode('utf-8') == u'热门':
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        res = entities[:5]
    else:
        # _entities = Entity.search.query(content.decode('utf-8')).order_by('@weight', '-created_time')
        sqs = SearchQuerySet()
        results = sqs.auto_query(content.decode('utf-8')).order_by('-created_time')

    # log.info(_entities.all())
    # for row in _entities.all():
    #     log.info(row)

        for row in results:
            res.append(row.object)
        log.info(res)
    return res


def handle_event(content):
    # log.info(content)
    items = []
    if content['EventKey'] == "V1001_SELECTION":
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)

        for row in entities[:5]:
            items.append(row.entity)
        # return items
    elif content['EventKey'] == "V1002_POPULAR":
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        items = entities[:5]
    elif content['EventKey'] == "V2001_USER_LIKE":
        open_id = content['FromUserName']
        try:
            token = Token.objects.get(open_id=open_id)
        except Token.DoesNotExist, e:
            log.info(e)
            return None

        el = Entity_Like.objects.filter(user = token.user)
        for row in el[:5]:
            items.append(row.entity)
        # return items

    return items



__author__ = 'edison'
