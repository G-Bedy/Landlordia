from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from users.views import (UserListView, UserRegisterView,
                         UserRetrieveUpdateDestroyView)

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('userlist/', UserListView.as_view(), name='user_list'),
    path('register/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='register_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
