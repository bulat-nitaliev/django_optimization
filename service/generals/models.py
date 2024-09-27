from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client

class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

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

    def __str__(self) -> str:
        return self.plan_types

class Subscription(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(to=Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(to=Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)