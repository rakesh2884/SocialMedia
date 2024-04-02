from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password','roles','image']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = authenticate(username=username,password=password)
        if not user:
            print (username)
            print (password)
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
class AccountUpdateSerializer(serializers.Serializer):
    choice=serializers.ChoiceField(choices=['username','password','email','image','roles'])
    new_username=serializers.CharField(required=False)
    new_password=serializers.CharField(required=False)
    new_email=serializers.EmailField(required=False)
    new_image=serializers.ImageField(required=False)
    new_roles=serializers.IntegerField(required=False)
class PostCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    caption=serializers.CharField(required=False)
    post=serializers.FileField(required=True)
class ViewSerializer(serializers.Serializer):
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
class LikeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    post_id = serializers.IntegerField(required=True)
class CommentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    comment=serializers.CharField(required=True)
class ViewLikedSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
class FollowSerializer(serializers.Serializer):
    follower_id=serializers.IntegerField(required=True)
    following_id=serializers.IntegerField(required=True)
class ViewFollowingPostSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    following_id=serializers.IntegerField(required=True)

