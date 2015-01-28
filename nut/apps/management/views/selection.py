from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import Selection_Entity, Entity_Like
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage
from apps.core.forms.selection import SelectionForm, SetPublishDatetimeForm
from datetime import datetime, timedelta

from django.utils.log import getLogger

log = getLogger('django')

def published(request, template="management/selection/list.html"):
    _page = request.GET.get('page', 1)

    s = Selection_Entity.objects.published()
    # log.info(s.query)
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    # log.info(selections.object_list)
    # innqs = selections.object_list
    # _entities = Entity.objects.filter(id__in=list(selections.object_list))

    return render_to_response(
        template,
        {
            'selections': selections,
            'pending_count': Selection_Entity.objects.pending().count()
            # 'entities': _entities,
        },
        context_instance = RequestContext(request)
    )


def pending(request, template="management/selection/list.html"):

    _page = request.GET.get('page', 1)
    s = Selection_Entity.objects.pending()
    # log.info(s.query)
    paginator = ExtentPaginator(s, 30)

    try:
        selections = paginator.page(_page)
    except PageNotAnInteger:
        selections = paginator.page(1)
    except EmptyPage:
        raise Http404

    # _entities = Entity.objects.filter(id__in=list(selections.object_list))

    return render_to_response(
        template,
        {
            'selections': selections,
            'pending_count': Selection_Entity.objects.pending().count()
            # 'entities': _entities,
        },
        context_instance = RequestContext(request)
    )


def edit_publish(request, sid, template="management/selection/edit_publish.html"):
    # return HttpResponse("OK")
    try:
        selection = Selection_Entity.objects.get(pk=sid)
    except Selection_Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = SelectionForm(selection=selection, data=request.POST)
        if _forms.is_valid():
            _forms.update()

    else:
        _forms = SelectionForm(selection=selection)

    return render_to_response(
        template,
        {
            'selection': selection,
            'forms': _forms,
            'button': _('update'),
        },
        context_instance = RequestContext(request)
    )


def set_publish_datetime(request, template="management/selection/set_publish_datetime.html"):

    if request.is_ajax():
        template = "management/selection/set_publish_datetime.html"

    if request.method == "POST":
        _forms = SetPublishDatetimeForm(request.POST)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(reverse('management_selection_published'))
    else:
        _forms = SetPublishDatetimeForm()

    return render_to_response(
        template,
        {
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


def popular(request, template="management/selection/popular.html"):


    days = timedelta(days=7)
    now_string = datetime.now().strftime("%Y-%m-%d")
    dt = datetime.now() - days


    query = "select id, entity_id, count(*) as lcount from core_entity_like where created_time between '%s' and '%s' group by entity_id order by lcount desc" % (dt.strftime("%Y-%m-%d"), now_string)
    _entity_list = Entity_Like.objects.raw(query)

    log.info(_entity_list.query)
    # for like in  entity_list:
    #     log.info(like.entity )

    return render_to_response(
        template,
        {
            'popular_entity_list':_entity_list[:60],
        },
        context_instance = RequestContext(request)
    )

__author__ = 'edison7500'
