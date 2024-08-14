from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from users.serializers import UserSerializer

User = get_user_model()


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


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
