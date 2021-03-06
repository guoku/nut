# coding=utf-8
import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count

from apps.core.models import Selection_Entity, Entity, Buy_Link


class Command(BaseCommand):
    def handle(self, *args, **options):
        last_pub_time = Selection_Entity.objects.filter(is_published=True).latest('pub_time').pub_time
        start_pub_time = last_pub_time + datetime.timedelta(days=1)
        start_pub_time = start_pub_time.replace(hour=9, minute=0, second=0, microsecond=0)
        end_pub_time = start_pub_time + datetime.timedelta(hours=15)

        ses = Selection_Entity.objects.filter(is_published=True,
                                              entity__status=Entity.selection,
                                              entity__buy_links__status=Buy_Link.sale,
                                              pub_time__lt=start_pub_time.replace(month=1, day=1),
                                              pub_time__month=start_pub_time.month)
        ses = ses.select_related('entity__likes').annotate(like_count=Count('entity__likes')).order_by('-like_count')
        ses = ses.iterator()

        for pub_time in datetime_range(start_pub_time, end_pub_time, datetime.timedelta(minutes=30)):
            se = next(ses)
            self.stdout.write(u'{pub_time}: {new_pub_time}: {title}'.format(pub_time=se.pub_time,
                                                                            new_pub_time=pub_time,
                                                                            title=se.entity.title))
            se.pub_time = pub_time
            se.save()


def datetime_range(start, end, step):
    """
    :type start: datetime.datetime
    :type end: datetime.datetime
    :type step: datetime.timedelta
    """
    while start < end:
        yield start
        start += step
