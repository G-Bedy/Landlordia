from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'address', 'birth_date']


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'bio', 'address', 'birth_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = {
            'bio': validated_data.pop('bio', ''),
            'address': validated_data.pop('address', ''),
            'birth_date': validated_data.pop('birth_date', None),
        }
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = {
            'bio': validated_data.pop('bio', ''),
            'address': validated_data.pop('address', ''),
            'birth_date': validated_data.pop('birth_date', None),
        }
        instance = super().update(instance, validated_data)
        profile, created = Profile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        profile = getattr(instance, 'profile', None)
        if profile:
            profile_representation = ProfileSerializer(instance.profile).data
            representation.update(profile_representation)
        representation.pop('profile', None)
        return representation


#     в реализации представленной ниже все работает.
#     при POST и GET запросах одинаковый формат JSON.
#     Но в этом случае API пишет что <поля "bio" и "address" обязательны для заполнения>
#     -----------------------------------------------------
#
# class UserSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer(required=False)
#
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'phone_number', 'profile']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         user = User.objects.create_user(**validated_data)
#         if profile_data:
#             Profile.objects.create(user=user, **profile_data)
#         return user
#
#     def update(self, instance, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         instance = super().update(instance, validated_data)
#
#         if profile_data:
#             profile, created = Profile.objects.get_or_create(user=instance)
#             for attr, value in profile_data.items():
#                 setattr(profile, attr, value)
#             profile.save()
#         return instance
#
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#
#         profile = getattr(instance, 'profile', None)
#         if profile:
#             profile_representation = ProfileSerializer(instance.profile).data
#             representation.update(profile_representation)
#         representation.pop('profile', None)
#         return representation
#
#     def to_internal_value(self, data):
#         profile_data = {
#             'bio': data.pop('bio', None),
#             'address': data.pop('address', None),
#             'birth_date': data.pop('birth_date', None),
#         }
#         data['profile'] = profile_data
#         return super().to_internal_value(data)
