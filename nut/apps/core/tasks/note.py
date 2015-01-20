from celery.task import task
from apps.core.tasks import BaseTask
from apps.core.models import Note_Poke

from django.utils.log import getLogger

log = getLogger('django')


@task(base=BaseTask)
def post_note(uid, nid):

    try:
        Note_Poke.objects.get(user_id=uid, note_id=nid)
    except Note_Poke.DoesNotExist:
        np =  Note_Poke(
            user_id=uid,
            note_id=nid,
        )
        np.save()
    # pass

@task(base=BaseTask)
def depoke_note(uid, nid):
    try:
        np = Note_Poke.objects.get(user_id=uid, note_id=nid)
        np.delete()
    except Note_Poke.DoesNotExist, e:
        log.info("INFO: %s" % e.message)

__author__ = 'edison'
