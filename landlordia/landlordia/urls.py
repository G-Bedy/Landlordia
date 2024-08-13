from django.contrib import admin
from django.urls import include, path
from yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('realestate.urls', namespace='realestate')),
    path('api/v1/users/', include('users.urls', namespace='users')),
]

urlpatterns += doc_urls
