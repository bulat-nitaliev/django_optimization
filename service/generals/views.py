from django.shortcuts import render
from generals.serializers import SubscriptionSerializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from generals.models import Subscription, Client
from django.db.models import Prefetch, F, Sum
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings




class SubscriptionView(ReadOnlyModelViewSet):
    # queryset = Subscription.objects.all().prefetch_related('client').prefetch_related('client__user')
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', 
                 queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')
        )
    )
    
    serializer_class = SubscriptionSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response =  super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        price_cache_name = settings.PRICE_CACHE_NAME
        price_cache = cache.get(price_cache_name)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(price_cache_name, total_price, 60*60)

        response_data['total_amount'] = total_price
        response = response_data
        return Response(response)


