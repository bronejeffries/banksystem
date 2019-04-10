from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'password','date_joined','email')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = User(
                    email=validated_data['email'],
                    username=validated_data['username']
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'password','date_joined','email','is_staff')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validated_data):
        user = User(
                    email=validated_data['email'],
                    username=validated_data['username']
                    )
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
