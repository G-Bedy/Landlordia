from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from users.serializers import UserSerializer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        method = self.request.method
        if method in ['GET', 'PUT', 'PATCH']:
            if self.request.user.is_authenticated:
                user = self.get_object()
                if self.request.user == user or self.request.user.is_staff:
                    return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()]
        return [permissions.IsAdminUser()]

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs['pk'])
        return obj
