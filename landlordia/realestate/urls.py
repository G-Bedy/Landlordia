from django.urls import path

from realestate.views import (LeaseContractAPIList, LeaseContractAPIRUD,
                              PaymentAPIList, PaymentAPIRUD, PropertyAPIList,
                              PropertyAPIRUD, TenantAPIList, TenantAPIRUD)

app_name = 'realestate'

urlpatterns = [
    path('property/', PropertyAPIList.as_view(), name='property-list'),
    path('property/<int:pk>/', PropertyAPIRUD.as_view(), name='property-detail'),
    path('tenant/', TenantAPIList.as_view(), name='tenant-list'),
    path('tenant/<int:pk>/', TenantAPIRUD.as_view(), name='tenant-detail'),
    path('leasecontract/', LeaseContractAPIList.as_view(), name='leasecontract-list'),
    path('leasecontract/<int:pk>/', LeaseContractAPIRUD.as_view(), name='leasecontract-detail'),
    path('payment/', PaymentAPIList.as_view(), name='payment-list'),
    path('payment/<int:pk>/', PaymentAPIRUD.as_view(), name='payment-detail'),
]
