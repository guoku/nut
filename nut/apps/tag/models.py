from django.db import models, connection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from apps.core.models import BaseModel

from django.db.models import Count
from django.core.cache import cache

from django.utils.log import getLogger

from urllib import  quote
# from apps.core.manager import dictfetchall
import random

log = getLogger('django')

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class ContentTagQuerySet(models.query.QuerySet):
    def user_tags(self, user):
        # deprecated , need add deprecate WARNING
        content_tags  = self.using('slave').filter(creator=user).select_related('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        return content_tags

    def user_tags_unique(self, user):
        content_tags  = self.using('slave').filter(creator=user).select_related('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        tags = [ct.tag for ct in content_tags]
        tags = set(tags)
        return list(tags)

    def popular(self):
        return self.using('slave').annotate(tcount=Count('tag')).order_by('-tcount')[:300]

    def entity_tags(self, nid_list):
        return self.using('slave').filter(target_object_id__in=nid_list).values('tag','tag__name','tag__hash').annotate(ncount=Count('tag')).order_by('-ncount')

    def article_tags(self, article_id):
        _tag_list =  self.using('slave')\
                    .filter(target_object_id=article_id, target_content_type_id=31)\
                    .values_list('tag__name', flat=True)
        return sorted(list(set(list(_tag_list))))


class ContentTagManager(models.Manager):

    def user_tags_unique(self, _user):
        return self.get_queryset().user_tags_unique(_user)

    def popular_entity_tag(self):
        key = 'new_entity_tag_popular_all'
        res = cache.get(key)
        if res:
            return list(res)

        res = self.get_queryset().popular()
        #TODO : make the timeout to 1 day
        cache.set(key, res , timeout=86400)
        return res

    def popular_random(self, tag_count=15):
        key = 'new_entity_tag_popular_random_%s' % tag_count
        res = cache.get(key)
        log.info(res)
        if res:
            return res

        popularTags = self.popular_entity_tag()
        if popularTags.count < tag_count:
            res =  popularTags;
        else:
            res =  random.sample(popularTags, tag_count)
        #TODO: make the timeout to 15 minute
        cache.set(key, res , timeout=900)

        return res

    def get_queryset(self):
        return ContentTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):

        obj = self.raw('SELECT id, tag_id, COUNT(tag_id) AS entity_count \
                        FROM tag_content_tags WHERE creator_id=%s AND target_content_type_id = 24 GROUP BY tag_id ORDER BY entity_count DESC' % user)

        res = list()
        for row in obj:
            data = {
                'tag_id': row.tag_id,
                'tag': row.tag.name,
                'tag_hash': row.tag.hash,
                'entity_count': row.entity_count,
            }
            # print  dict
            res.append(data)
            # print row.tag
        return res

    def query_user_tags(self,user):
        #in user index page , use this query will reduce page query a lot
        # if use raw sql :
        # a . all user tags will be selected ,
        # b .  and every row will cause an other db hit (row.tag.name)
        # after test , switch to  query_user_tags
        return self.get_queryset().user_tags(user)


    def tags(self, tag_id_list):
        key_string = ','.join(str(s) for s in tag_id_list)
        obj = self.raw("SELECT id, tag_id, COUNT(tag_id) AS entity_count \
                        FROM tag_content_tags WHERE tag_id IN (%s) AND target_content_type_id = 24 GROUP BY tag_id ORDER BY entity_count DESC" % key_string)
        res = list()
        for row in obj:
            data = {
                'tag_id': row.tag_id,
                'tag': row.tag.name,
                'tag_hash': row.tag.hash,
                'entity_count': row.entity_count,
            }
            res.append(data)

        return res

    def article_tags(self, article_id):
        res = self.get_queryset().article_tags(article_id)
        return res

    def entity_tags(self, nid_list):
        res = self.get_queryset().entity_tags(nid_list)
        return res


class TagsQueryset(models.query.QuerySet):
    def top_article_tags(self):
        #this list is set by editor
        res = self.using('slave').filter(isTopArticleTag=True,content_tags__target_content_type_id=31).distinct()
                                 # .annotate(acount=Count('content_tags')).order_by('-acount')
        return res

    def hot_article_tags(self):
        # this.list is generated by an crontab mission, see script/tags/
        # notice there is an RANDOM operation before return the list
        hot_content_tag_list = Content_Tags.objects.filter(target_content_type_id=31)\
                                                   .values('tag')\
                                                   .select_related('tag')\
                                                   .annotate(acount=Count('tag'))\
                                                   .order_by('-acount').distinct()[:50]
        tag_ids = [ctag.get('tag') for ctag in hot_content_tag_list]
        # random.shuffle(tag_ids)
        return self.filter(id__in=tag_ids)





class TagsManager(models.Manager):
    def get_queryset(self):
        return TagsQueryset(self.model, using = self._db)

    def get_hot_article_tag_key(self):
        return 'tag:article:hot'

    def hot_article_tags(self):
        # most used article tags (by editor)
        #hot article tag is generated by system
        #most time the the key is filled
        # in 48's crontab , there is a mission run every night to generate hot_article_tags
        # so most of the time , the key in cache has values in it (unless cache is flushed for some reason)
        key = self.get_hot_article_tag_key()
        tag_list = cache.get(key, None)
        if tag_list is None:
            tag_list = self.get_queryset().hot_article_tags()
            tag_list = random.sample(list(tag_list), 10)
            cache.set(key, tag_list, 3600*24)
        return tag_list

    def top_article_tags(self):
        #top article tag is set by operation team
        return self.get_queryset().top_article_tags()
        # tags = Content_Tags.objects.filter(tag__isTopArticleTag=True).aggregate('tag')
        # tag_list = self.get_queryset().filter(isTopArticleTag=True)
        # content_tags = Content_Tags.objects.filter(tag__in=tag_list, target_content_type_id=31).group_by('target_object_id')

        # return tags


class Tags(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    hash = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.BooleanField(default=False)
    image = models.URLField(max_length=255, null=True)
    # state fields
    isTopArticleTag = models.BooleanField(default=False, db_index=True)
    isPubishedEntityTag = models.BooleanField(default=False)
    description = models.CharField(max_length=1024, null=True, blank=True)

    objects = TagsManager()

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    @property
    def quoted_tag_name(self):
        return quote(self.name.encode('utf-8'))

    @property
    def tag_hash(self):
        return self.hash[:8]

    @property
    def note_count(self):
        return self.content_tags_set.filter(target_content_type_id=24).count()

    def get_absolute_url(self):
        return "/tag/%s/" % self.name

    @property
    def articles(self):
        return self.content_tags_set.filter(target_content_type_id=31)

    @property
    def articlesCount(self):
        return self.articles.values('target_object_id').distinct().count()


class Content_Tags(BaseModel):
    tag = models.ForeignKey(Tags)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_tags')

    target_content_type = models.ForeignKey(ContentType, related_name='tag_target', blank=True, null=True)
    target_object_id = models.BigIntegerField(null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, editable=True, db_index=True)

    objects = ContentTagManager()

    class Meta:
        unique_together = ('tag', 'creator', 'target_content_type', 'target_object_id')
        ordering = ["-created_datetime"]


__author__ = 'xiejiaxin'
