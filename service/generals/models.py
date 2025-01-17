from typing import Any, Iterable
from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from generals.tasks import set_price, set_comment

class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)

    def __str__(self) -> str:
        return self.name

class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )
    plan_types = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)

        

    def __str__(self) -> str:
        return self.plan_types

class Subscription(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(to=Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(to=Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')