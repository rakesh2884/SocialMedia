from rest_framework import serializers

from .models import User
class userProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    confirm_password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields="__all__"
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
class ViewAccountSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class AccountUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    choice=serializers.ChoiceField(choices=['username','password','email','image','roles'])
    new_username=serializers.CharField(required=False)
    new_password=serializers.CharField(required=False)
    new_email=serializers.EmailField(required=False)
    new_image=serializers.ImageField(required=False)
    new_roles=serializers.IntegerField(required=False)
class AccountDeleteSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
class PostCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    caption=serializers.CharField(required=False)
    post=serializers.FileField(required=True)
class PostViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
class PostUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    choice=serializers.ChoiceField(choices=['caption','post'])
    new_caption=serializers.CharField(required=False)
    new_post=serializers.FileField(required=False)
class PostDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
