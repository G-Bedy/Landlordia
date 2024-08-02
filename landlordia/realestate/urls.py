from django.urls import path

from realestate.views import *


urlpatterns = [
    path('ownerlist/', OwnerAPIList.as_view()),
    path('ownerdetail/<int:pk>/', OwnerAPIRUD.as_view()),

    path('propertylist/', PropertyAPIList.as_view()),
    path('propertydetail/<int:pk>/', PropertyAPIRUD.as_view()),

    path('tenantlist/', TenantAPIList.as_view()),
    path('tenantdetail/<int:pk>/', TenantAPIRUD.as_view()),

    path('leasecontractlist/', LeaseContractAPIList.as_view()),
    path('leasecontractdetail/<int:pk>/', LeaseContractAPIRUD.as_view()),

    path('paymentlist/', PaymentAPIList.as_view()),
    path('paymentdetail/<int:pk>/', PaymentAPIRUD.as_view()),
]
