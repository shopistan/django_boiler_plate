"""
user serializer
"""
from django.contrib.auth.models import Group, Permission, ContentType
from rest_framework import serializers

from .models import User
from rest_auth.serializers import PasswordResetSerializer, settings
from rest_auth.registration.serializers import setup_user_email


class PermissionSerializer(serializers.ModelSerializer):
    """
    permission serializer
    """
    class Meta:
        """
        meta
        """
        model = Permission
        fields = '__all__'

class ContentTypeSerializer(serializers.ModelSerializer):
    """
    permission serializer
    """

    class Meta:
        """
        meta
        """
        model = ContentType
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """
    group serializer
    """

    class Meta:
        """
        class meta
        """
        model = Group
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        """

        Args:
            validated_data:

        Returns:

        """
        permissions_data = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)
        for permission_data in permissions_data:
            try:
                group.permissions.add(permission_data["id"])
            except KeyError:
                group.permissions.add(permission_data)
        group.save()
        return group

    def update(self, instance, validated_data):
        """

        Args:
            instance:
            validated_data:

        Returns:

        """
        permissions_data = validated_data.pop('permissions')
        instance.permissions.clear()  # delete call to db
        instance.save()
        for permission_data in permissions_data:
            try:
                instance.permissions.add(permission_data["id"])  # insert call to db
            except KeyError:
                instance.permissions.add(permission_data)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    # Because User and Group are in many-to-many relations so you can directly add the
    # group field in the users serializers. For more details follow django.contrib.auth.models
    # package and User inherits AbstactUser and AbstractUser inherits PermissionsMixin
    # which has groups as many to many field.

    class Meta:
        """
        meta
        """
        model = User
        groups = GroupSerializer(many=True)
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',
            'is_staff', 'groups', 'phone', 'is_verified', 'is_active', 'is_superuser', 'role')
        extra_kwargs = {'password': {'write_only': True}}
        # read_only_fields = ['email']
        depth = 1

    def create(self, validated_data):
        """

        Args:
            validated_data:

        Returns:

        """
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        for group_data in groups_data:
            try:
                user.groups.add(group_data["id"])
            except KeyError:
                user.groups.add(group_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """

        Args:
            instance:
            validated_data:

        Returns:

        """
        # instance.email = validated_data.get('email', instance.email)
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.phone = validated_data.pop('phone')
        instance.email = validated_data.pop('email')
        instance.is_superuser = validated_data.pop('is_superuser')
        instance.is_staff = validated_data.pop('is_staff')
        instance.is_active = validated_data.pop('is_active')
        instance.groups.clear()  # delete call to db
        for group_data in groups_data:
            try:
                instance.groups.add(group_data["id"])  # insert call to db
            except KeyError:
                instance.groups.add(group_data)
        if not (password is None or password == '' or password == 'null' or password == 'undefined'):
            instance.set_password(password)
        role = validated_data.pop('role')
        if role:
            instance.role = role
            instance.groups.add(role)
        instance.save()
        return instance