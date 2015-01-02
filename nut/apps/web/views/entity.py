#encoding=utf8

from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.core.utils.http import JSONResponse
from apps.core.models import Entity, Entity_Like, Note, Note_Comment
from apps.web.forms.comment import CommentForm
from apps.web.forms.note import NoteForm
from apps.web.forms.entity import EntityURLFrom, CreateEntityForm
# from apps.core.tasks.entity import like_task

from django.utils.log import getLogger

log = getLogger('django')



def entity_detail(request, entity_hash, templates='web/entity/detail.html'):
    _entity_hash = entity_hash

    _user = None
    _note_forms = None
    if request.user.is_authenticated():
        _user = request.user
        _note_forms = NoteForm()

    _entity = Entity.objects.get(entity_hash = _entity_hash)

    _user_post_note = True
    try:
        _entity.notes.get(user=_user)

    except Note.DoesNotExist:
        _user_post_note = False


    like_status = 0
    try:
        _entity.likes.get(user = _user)
        like_status = 1
    except Entity_Like.DoesNotExist:
        pass

    log.info(_entity.category)

    return render_to_response(
        templates,
        {
            'entity': _entity,
            'like_status': like_status,
            'user':_user,
            'user_post_note':_user_post_note,
            'note_forms':_note_forms,
        },
        context_instance = RequestContext(request),
    )

@login_required
def entity_post_note(request, eid, template='web/entity/partial/ajax_detail_note.html'):
    if request.method == 'POST':
        _user = request.user
        _eid = eid

        _forms = NoteForm(request.POST, user=_user, eid=_eid)
        if _forms.is_valid():
            note = _forms.save()
            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'note': note,
            })
            _data = _t.render(_c)
            return JSONResponse(
                data= {
                    'status':1,
                    'data':_data,
                },
                content_type='text/html; charset=utf-8',
            )

    # else:
    raise HttpResponseNotAllowed


@login_required
def entity_update_note(request, nid):
    if request.method == "POST":
        _user = request.user
        _forms = NoteForm(request.POST, user=_user, nid=nid)
        if _forms.is_valid():
            note = _forms.update()

            return

    # else:
    return HttpResponseNotAllowed

# @login_required
def entity_note_comment(request, nid, template='web/entity/note/comment_list.html'):

    _user = None

    if request.method == "POST":
        if request.user.is_authenticated():
            _user = request.user
        else:
            return HttpResponseRedirect(reverse('web_login'))

        try:
            note = Note.objects.get(pk = nid)
        except Note.DoesNotExist:
            raise Http404
        _forms = CommentForm(note=note, user=_user, data=request.POST)
        if _forms.is_valid():
            # log.info("ok ok ok ok")

            comment = _forms.save()
            template = 'web/entity/note/comment.html'

            _t = loader.get_template(template)
            _c = RequestContext(request, {
                'comment': comment,
            })

            _data = _t.render(_c)

            return JSONResponse(
                data={
                    'data': _data,
                    'status' : '1',
                },
                content_type='text/html; charset=utf-8',
            )
         # log.info(_forms.errors)
        # return
    else:
        _forms = CommentForm()

    _comment_list = Note_Comment.objects.filter(note_id= nid)

    log.info(_comment_list)
    _t = loader.get_template(template)
    _c = RequestContext(request, {
        'comment_list': _comment_list,
        'note_id': nid,
        'forms': _forms
        # 'note_context': _note_context,
    })
    _data = _t.render(_c)

    return JSONResponse(
        data={
            'data':_data,
        },
        content_type='text/html; charset=utf-8',
    )


@login_required
def entity_note_comment_delete(request, comment_id):
    if request.is_ajax():
        _user = request.user
        try:
            comment = Note_Comment.objects.get(user=_user, pk = comment_id)
            comment.delete()
            return JSONResponse(data={'status':1})
        except:
            raise Http404

    return HttpResponseNotAllowed


@login_required
@csrf_exempt
def entity_like(request, eid):
    if request.is_ajax():
        _user = request.user
        try:
            el = Entity_Like.objects.create(
                user = _user,
                entity_id = eid,
            )
            return JSONResponse(data={'status':1})
        except Exception, e:
            log.error("ERROR: %s", e.message)
            # pass
        # result = like_task.apply_async((_user.id, eid), expires=5)
        # if result.get():


    return HttpResponseNotAllowed


@login_required
@csrf_exempt
def entity_unlike(request, eid):
    if request.is_ajax():
        _user = request.user
        try:
            el = Entity_Like.objects.get(entity_id = eid, user = _user)
            el.delete()
            return JSONResponse(data={'status':0})
        except Entity_Like.DoesNotExist:
            raise Http404
        # return JSONResponse()

    return HttpResponseNotAllowed


@login_required
def entity_create(request, template="web/entity/new.html"):

    if request.method == 'POST':
        _forms = CreateEntityForm(request=request, data=request.POST)
        if _forms.is_valid():
            entity = _forms.save()

            return HttpResponseRedirect(reverse('web_entity_detail', args=[entity.entity_hash,]))
        log.info(_forms.errors)
    else:
        _url_froms = EntityURLFrom(request)

        return render_to_response(
            template,
            {
                'url_forms':_url_froms
            },
            context_instance = RequestContext(request),
        )

@login_required
def entity_load(request):

    if request.method == "POST":
        _forms = EntityURLFrom(request=request, data=request.POST)
        if _forms.is_valid():
            _item_info = _forms.load()

            # log.info(_item_info)


            if _item_info.has_key('entity_hash'):
                _res = {
                    'status' : 'EXIST',
                    'data': _item_info,
                }
            else:
                _res = {
                    'status': 'SUCCESS',
                    'data': _item_info,
                }
            return JSONResponse(data=_res)

    raise HttpResponseNotAllowed


__author__ = 'edison'
