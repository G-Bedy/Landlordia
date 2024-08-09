from django.urls import path
from realestate.views import (LeaseContractAPIList, LeaseContractAPIRUD,
                              OwnerAPIList, OwnerAPIRUD, PaymentAPIList,
                              PaymentAPIRUD, PropertyAPIList, PropertyAPIRUD,
                              TenantAPIList, TenantAPIRUD)


app_name = 'realestate'


urlpatterns = [
    path('ownerlist/', OwnerAPIList.as_view()),
    path('ownerdetail/<int:pk>/', OwnerAPIRUD.as_view()),

    path('propertylist/', PropertyAPIList.as_view(), name='property_list'),
    path('propertydetail/<int:pk>/', PropertyAPIRUD.as_view()),

    path('tenant/', TenantAPIList.as_view()),
    path('tenant/<int:pk>/', TenantAPIRUD.as_view()),

    path('leasecontractlist/', LeaseContractAPIList.as_view()),
    path('leasecontractdetail/<int:pk>/', LeaseContractAPIRUD.as_view()),

    path('paymentlist/', PaymentAPIList.as_view()),
    path('paymentdetail/<int:pk>/', PaymentAPIRUD.as_view()),
]
