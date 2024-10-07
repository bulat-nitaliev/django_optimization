import datetime
import time
from celery import shared_task
from django.db.models import Prefetch, F
from celery_singleton import Singleton
from django.db import transaction



@shared_task()
def set_price(sub_id):
    
    from generals.models import Subscription

    time.sleep(5)
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().filter(id=sub_id).annotate(
            annotated_price=F('service__full_price') - 
                F('service__full_price') * F('plan__discount_percent')/100.00
                ).first()
        subscription.price = subscription.annotated_price
        subscription.save()

@shared_task()
def set_comment(sub_id):
    
    from generals.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().get(id=sub_id)
        time.sleep(8)
        subscription.comment = str(datetime.datetime.now())
        subscription.save()