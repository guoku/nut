# coding=utf-8
from datetime import datetime
from xml.sax.saxutils import XMLGenerator

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags, escape
from django.utils.translation import gettext_lazy as _

from apps.core.models import Selection_Entity, Selection_Article, Article, GKUser
from apps.tag.models import Content_Tags, Tags


class SimplerXMLGenerator(XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None, escape=False):
        """Convenience method for adding an element with no children"""
        attrs = {} if attrs is None else attrs
        self.startElement(name, attrs)
        if contents is not None:
            if escape:
                self.characters(contents)
            else:
                if not isinstance(contents, unicode):
                    contents = unicode(contents, self._encoding)
                self._write(contents)
        self.endElement(name)


class CustomFeedGenerator(Rss201rev2Feed):
    mime_type = 'application/xml; charset=utf-8'

    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u"image", item['image'])


class ArticlesFeedGenerator(Rss201rev2Feed):
    mime_type = 'application/xml; charset=utf-8'

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("rss", self.rss_attributes())
        handler.startElement("channel", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        self.endChannelElement(handler)
        handler.endElement("rss")

    def rss_attributes(self):
        attrs = super(ArticlesFeedGenerator, self).rss_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        attrs['xmlns:georss'] = 'http://www.georss.org/georss'
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        return attrs

    def add_item_elements(self, handler, item):
        super(ArticlesFeedGenerator, self).add_item_elements(handler, item)

        if item['content_encoded'] is not None:
            handler.addQuickElement(u'content:encoded', item['content_encoded'], escape=False)


class SelectionFeeds(Feed):
    feed_type = CustomFeedGenerator

    title = _("live different")
    link = '/selected/'
    description = _('guoku selection desc')

    description_template = "web/feeds/selection_description.html"

    def items(self):
        return Selection_Entity.objects.published().filter(pub_time__lt=datetime.now())[:60]

    def item_title(self, item):
        return item.entity

    def item_link(self, item):
        return reverse('web_entity_detail', args=[item.entity.entity_hash])

    def item_description(self, item):
        return item.top_note.note

    def item_author_name(self, item):
        return item.entity.top_note.user.profile.nickname

    def item_pubdate(self, item):
        return item.pub_time

    def item_extra_kwargs(self, item):
        return {'image': item.entity.chief_image}


class ArticlesInterviewFeeds(Feed):
    feed_type = ArticlesFeedGenerator
    title = u'果库'
    link = '/tag/articles/%25E4%25B8%2593%25E8%25AE%25BF/'
    author_email = "hi@guoku.com"
    feed_copyright = "2010-2015 果库. All rights reserved."
    description = '果库消费图文,专访精英卖家,汇集全网秉持理想生活哲学的消费类文章，开拓精英视野与生活想象，涵盖品牌相关报道、卖家创业者专访、潮流资讯、消费见解主张、生活场景清单、购物经验心得分享等。'

    def items(self):
        _tag = Tags.objects.get(name=u'专访')
        article_id_list = Content_Tags.objects.filter(tag=_tag, target_content_type_id=31).values_list(
            'target_object_id').distinct()
        articles = Article.objects.filter(id__in=article_id_list).order_by('-updated_datetime')[:20]
        return articles

    def item_title(self, article):
        return escape(article.title)

    def item_link(self, article):
        return reverse('web_article_page_slug', args=[article.article_slug]) + '?from=feed'

    def item_author_name(self, article):
        return escape(article.creator.profile.nick)

    def item_pubdate(self, article):
        return article.updated_datetime

    def item_description(self, article):
        content = strip_tags(article.content)
        desc = content.split(u'。')
        return escape(desc[0] + u'。')

    def item_extra_kwargs(self, article):
        extra = {
            'content_encoded': ("<![CDATA[%s]]>" % article.bleached_content).encode('utf-8'),
        }
        return extra


class ArticlesFeeds(Feed):
    feed_type = ArticlesFeedGenerator
    title = u'图文频道>>果库|精英消费者南'
    link = "/articles/"
    author_email = "hi@guoku.com"
    feed_copyright = "2010-2015 果库. All rights reserved."
    description = '果库消费图文汇集全网秉持理想生活哲学的消费类文章，开拓精英视野与生活想象，涵盖品牌相关报道、卖家创业者专访、潮流资讯、消费见解主张、生活场景清单、购物经验心得分享等。'

    def items(self):
        return Selection_Article.objects.published().order_by('-pub_time')[0:20]

    def item_title(self, item):
        return escape(item.article.title)

    def item_link(self, item):
        return reverse('web_article_page_slug', args=[item.article.article_slug]) + '?from=feed'

    def item_author_name(self, item):
        return escape(item.article.creator.profile.nick)

    def item_pubdate(self, item):
        return item.pub_time

    def item_description(self, item):
        content = strip_tags(item.article.content)
        desc = content.split(u'。')
        return escape(desc[0] + u'。')

    def item_extra_kwargs(self, item):
        extra = {
            'content_encoded': ("<![CDATA[%s]]>" % smart_str(item.article.feed_content)),
        }
        return extra


class ZKArticleFeeds(ArticlesFeeds):
    def items(self):
        return Selection_Article.objects.published().order_by('-pub_time')[0:10]


class GKEditorSelectionFeed(ArticlesFeeds):
    def items(self):
        editors = list(GKUser.objects.editor())
        return Selection_Article.objects.published().filter(article__creator__in=editors).order_by('-pub_time')[0:20]
