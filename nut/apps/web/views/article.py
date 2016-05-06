# coding=utf-8
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from django.forms.models import BaseModelFormSet
from django.views.generic import ListView,\
                                View,\
                                TemplateView,\
                                DetailView,\
                                CreateView
from django.shortcuts import redirect, get_object_or_404,render
from django.http import Http404
from django.template import RequestContext, loader,Context

from apps.core.models import Article,Selection_Article, Article_Dig
from apps.tag.models import Tags
# from apps.core.mixins.views import SortMixin
from apps.core.extend.paginator import ExtentPaginator as Jpaginator
from apps.core.views import BaseJsonView


from apps.web.utils.viewtools import add_side_bar_context_data
from apps.web.forms.articles import WebArticleEditForm
from apps.counter.utils.data import RedisCounterMachine

from braces.views import UserPassesTestMixin,JSONResponseMixin,AjaxResponseMixin,CsrfExemptMixin, LoginRequiredMixin
from django.utils.log import getLogger
from django.conf import settings
from datetime import datetime

from apps.core.tasks.article import dig_task, undig_task
from django import  http
import requests

from web.forms.remark import ArticleRemarkForm
from core.models import Article_Remark

textrank_url = getattr(settings, 'ARTICLE_TEXTRANK_URL', None)

log = getLogger('django')


class ArticleDig(LoginRequiredMixin,JSONResponseMixin,AjaxResponseMixin, View ):
    def post_ajax(self, request, *args, **kwargs):
        _user = request.user
        _aid = self.kwargs.pop('pk', None)
        if _aid is None:
            return http.Http404
        try:
            dig_task.delay(uid=_user.id, aid=_aid)
            return self.render_json_response({'status': 1, 'article_id': _aid})
        except Exception as e :
            log.error("ERROR : %s ", e.message)
            return http.HttpResponseServerError


class ArticleUndig(JSONResponseMixin,LoginRequiredMixin,AjaxResponseMixin,View):
    def post_ajax(self, request, *args, **kwargs):
        _user = request.user
        _aid = self.kwargs.pop('pk', None)
        if _aid is None:
            return http.Http404
        try:
            undig_task.delay(uid=_user.id, aid=_aid)
            return self.render_json_response({'status':0, 'article_id':_aid})
        except Exception as e:
            log.error("ERROR: %s", e.message)
        return http.HttpResponseServerError


class NewSelectionArticleList(JSONResponseMixin, AjaxResponseMixin,ListView):
    template_name = template_name = 'web/article/selection_list_new.html'
    ajax_template_name = 'web/article/partial/selection_ajax_list_new.html'
    paginate_by = 24
    model = Selection_Article
    paginator_class = Jpaginator
    context_object_name = 'selection_articles'
    #
    # def get_queryset(self):
    #     pass;

    def get_refresh_time(self):
        refresh_time = self.request.GET\
                                    .get('t',datetime.now()\
                                                     .strftime('%Y-%m-%d %H:%M:%S'))
        return refresh_time

    def get_queryset(self):
        qs = Selection_Article.objects\
                              .published_until(until_time=self.get_refresh_time())\
                              .order_by('-pub_time')\
                              .select_related('article').using('slave')
                              # .defer('article__content')

        return qs


    def get_ajax(self, request, *args, **kwargs):
        # TODO : add error handling here
        self.object_list = getattr(self,'object_list', self.get_queryset())
        context = self.get_context_data()
        _template = self.ajax_template_name
        _t = loader.get_template(_template)
        _c = RequestContext(request, context)
        _html = _t.render(_c)

        return self.render_json_response({
            'html':_html,
            'errors': 0,
            'has_next_page':context['has_next_page']

        }, status=200)

    def get_read_counts(self,articles):
        counts_dic = RedisCounterMachine.get_read_counts(articles)
        return counts_dic

    def get_context_data(self, **kwargs):
        context = super(NewSelectionArticleList, self).get_context_data(**kwargs)
        selection_articles = context['selection_articles']
        context['refresh_time'] = self.get_refresh_time()
        context['has_next_page'] = context['page_obj'].has_next()
        context['top_article_tags'] = Tags.objects.top_article_tags()

        articles = [sla.article for sla in selection_articles]

        try :
            # make sure use try catch ,
            # if statistic is down
            # the view is still working
            context['read_count'] = self.get_read_counts(articles)

        except Exception as e :
            log.info('the fail to load read count')
            log.info(e.message)

        return context


class EditorDraftList(UserPassesTestMixin,ListView):
    def test_func(self, user):
        if not hasattr(user, 'can_write'):
            return False
        return user.can_write

    def handle_no_permission(self, request):
        return redirect('web_selection')

    template_name = 'web/article/editor_list.html'
    model = Article
    paginate_by = 5
    paginator_class = Jpaginator
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user,publish=Article.draft)


class EditorArticleCreate(UserPassesTestMixin, View):
    def test_func(self, user):

        return user.can_write

    def get(self,request):
        new_article = Article(
            title="标题",
            cover='',
            content="正文",
            publish=Article.draft,
            creator=self.request.user,
        )
        new_article.save()
        return redirect('web_editor_article_edit',new_article.pk)

class EditorArticleEdit(LoginRequiredMixin, AjaxResponseMixin,JSONResponseMixin,UserPassesTestMixin,TemplateView):
    fields = ['title']
    template_name = 'web/article/editor_edit.html'
    model = Article
    raise_exception = True

    def test_func(self, user):
        the_article = self.get_article()
        return  user.can_write or (user.is_authorized_author and the_article.creator == user)

    def get_article(self):
        pk = self.kwargs['pk']
        the_article =  get_object_or_404(Article,pk=pk)
        return the_article

    def get(self,request, *args, **kwargs):
        pk = self.kwargs['pk']
        the_article =  self.get_article()
        if request.user.is_writer:
            if the_article.creator != request.user:
                raise Http404('没有找到对应文章，你是作者吗？')

        the_form = WebArticleEditForm(instance=the_article)
        return self.render_to_response({
            'form':the_form,
            'pk': pk,
            'cover_url': the_article.cover_url,
            'is_chief_editor': self.request.user.is_chief_editor
        })

    def post_ajax(self, request, *args, **kwargs):
        res={}
        pk = kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        if request.user.is_writer:
            if article.creator != request.user:
                raise Http404('没有找到对应文章，你是作者吗？')

        atform = WebArticleEditForm(request.POST)

        if atform.is_valid():
            try :
                data = atform.cleaned_data
                article.content = data['content']
                article.title = data['title']
                article.cover = data['cover']
                article.publish = data['publish']
                article.showcover = int(data['showcover'])
                article.save()
            except Exception as e:
                log(e)
                res={
                    'error': 1
                }
            res={
                'status':'1',
                'error':0
            }
        else:
            res={
                'status':'0',
                'error':1
            }

        return self.render_json_response(res)


class ArticleRelated(JSONResponseMixin, AjaxResponseMixin, ListView):

    pass

class ArticleDetail(AjaxResponseMixin,JSONResponseMixin, DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'web/article/onepage.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect('web_selection_articles')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_queryset(self):
        return Article.objects.filter(publish=Article.published)

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        queryset = self.get_queryset()
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            return None
        return obj

    def get_remark(self):
        article_id = self.kwargs.get('pk')
        remarks = Article_Remark.objects.filter(article_id=int(article_id))
        return remarks



    def get_context_data(self,**kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)

        article_remark_form = ArticleRemarkForm()

        article = context['article']
        context['from_app'] = self.request.GET.get('from','normal') == 'app'
        context['is_article_detail'] = True
        context['is_article_creator'] = self.request.user == self.object.creator
        context['can_show_edit'] = (not article.is_selection) and (self.request.user == article.creator)
        context['share_url'] = self.request.build_absolute_uri().replace('m.guoku.com', 'www.guoku.com')
        context['form'] = article_remark_form
        context['remarks'] = self.get_remark()
        dig_status = 0
        if self.request.user.is_authenticated():
            try:
                article.digs.get(user=self.request.user)
                dig_status = 1
            except Article_Dig.DoesNotExist:
                pass

        context['dig_status'] = dig_status
        context = add_side_bar_context_data(context)
        return context

    def get_ajax(self, request, *args, **kwargs):
        page = request.GET.get('page', 2)
        target  = request.GET.get('target', None)
        article = self.get_object()
        related_articles = article.get_related_articles(page)
        _template = 'web/article/partial/article_related_list.html'
        _t = loader.get_template(_template)
        _c =Context({
                'articles':related_articles
            })
        _data = _t.render(_c)
        return self.render_json_response({
            'html': _data,
            'errors': 0,
            'has_next_page': related_articles.has_next()

        })


class ArticleDelete(UserPassesTestMixin, View):
    def test_func(self, user):
        return user.can_write

    def get(self, request, *args , **kwargs):
        pk = kwargs['pk']
        the_article =  get_object_or_404(Article,pk=pk)

        if request.user.is_writer:
            if the_article.creator != request.user:
                raise Http404('没有找到对应文章，你是作者吗？')

#       TODO : check permission here
        the_article.publish = Article.remove
        the_article.save()
        return redirect('web_editor_article_list')



class ArticleTextRankView(BaseJsonView):

    def get_data(self, context):
        article_textrank_url = "%s%s" % (textrank_url, self.article_id)
        log.info(article_textrank_url)
        r = requests.get(article_textrank_url)
        return r.json()

    def get(self, request, *args, **kwargs):
        self.article_id = kwargs.pop('pk', None)
        assert self.article_id is not None

        return super(ArticleTextRankView, self).get(request, *args, **kwargs)

class ArticleRemarkCreate(AjaxResponseMixin, LoginRequiredMixin, JSONResponseMixin, View):

    def get_article(self):
        self.article_id = self.kwargs.get('pk',None)
        article = Article.objects.get(pk=self.article_id)
        return article

    def post_ajax(self, request, *args, **kwargs):
        res = {}
        article_remark = Article_Remark(user=self.request.user, article=self.get_article())
        arform = ArticleRemarkForm(self.request.POST, instance=article_remark)
        user = self.request.user

        if arform.is_valid():
            try:
                data = arform.cleaned_data
                content = data['content']
                reply_to = data['reply_to']
                print data.items()

                arform.save()
                res = {
                'user': user.nickname,
                'content': content,
                'reply_to': reply_to,
                'status': '1',
                'error': 0
                }

            except Exception as e:
                log(e)
                res = {
                    'error': 1
                }

        else:
            res = {
                'status': '0',
                'error': 1
            }

        return self.render_json_response(res)






__author__ = 'edison'
