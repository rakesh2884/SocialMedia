from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from .models import User,Post,Like,Comment,Follow
from django.core.files.storage import FileSystemStorage
import os
from .serializers import (RegisterSerializer,LoginSerializer,LogoutSerializer,CredentialSerializer,AccountUpdateSerializer,PostCreateSerializer,ViewSerializer,PostUpdateSerializer \
    ,PostDeleteSerializer,LikeSerializer,CommentSerializer,ViewLikedSerializer,FollowSerializer,ViewFollowingPostSerializer)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)          

class AccountView(APIView):
    def get(self, request, *args, **kwargs):    
        serializer=CredentialSerializer(data=request.data)
        permission_classes = (permissions.IsAuthenticated,)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            user = User.objects.get(username=username)
            return Response({'username':user.username,'password':password,'role':user.Roles[user.roles-1],'email':user.email,'image':str(user.image)},status=status.HTTP_202_ACCEPTED)
            

    def patch(self, request, *args, **kwargs):
        serializer=AccountUpdateSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    choice=serializer.data['choice']
                    if choice=="password":
                        user.password=make_password(serializer.data['new_password'])
                        user.save()
                        return Response({'message':'password changed successfully'},status=status.HTTP_201_CREATED)
                    elif choice == "username":
                        user.username=serializer.data['new_username']
                        user.save()
                        return Response({'message':'username changed successfully'},status=status.HTTP_201_CREATED)
                    elif choice == "email":
                        user.email=serializer.data['new_email']
                        user.save()
                        return Response({'message':'email changed successfully'},status=status.HTTP_201_CREATED)
                    elif choice == "image":
                        image=request.FILES['image']
                        fs = FileSystemStorage(location=settings.UPLOAD_FOLDER)
                        filename = fs.save(image.name, image)
                        i=os.path.join( settings.UPLOAD_PROFILE_FOLDER,image.name)
                        user.image=i
                        user.save()
                        return Response({'message':'image changed successfully'},status=status.HTTP_201_CREATED)
                    elif choice == "roles":
                        user.roles=serializer.data['new_roles']
                        user.save()
                        return Response({'message':'roles changed successfully'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)  
            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        serializer=CredentialSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    user.delete()
                    return Response({'message':'User deleted successfully'},status=status.HTTP_202_ACCEPTED)

            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)

class Posts(APIView):
    def post(self, request, *args, **kwargs):
        serializer=PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            post_=request.FILES['post']
            fs = FileSystemStorage(location=settings.UPLOAD_POST_FOLDER)
            filename = fs.save(post_.name, post_)
            p=os.path.join( settings.UPLOAD_POST_FOLDER,post_.name)
            user=User.objects.get(username=username)
            if user and check_password(password,user.password):
                post=Post(user_id=user.id,caption=serializer.data['caption'],post=p)
                post.save()
                return Response({'message':'Post created successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        serializer=ViewSerializer(data=request.data)
        if serializer.is_valid():
            id=serializer.data['id']
            posts=Post.objects.get(id=id)
            if posts:
                return Response({'caption':posts.caption,'post':str(posts.post),'like_count':posts.likes_count,'comments_count':posts.comments_count})
            else:
                return Response({'message':'not exist'})
    def patch(self, request, *args, **kwargs):
        serializer=PostUpdateSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            id=serializer.data['id']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    choice=serializer.data['choice']
                    posts=Post.objects.get(id=id)
                    if choice=="caption":
                        posts.caption=serializer.data['new_caption']
                        posts.save()
                        return Response({'message':'caption changed successfully'},status=status.HTTP_201_CREATED)
                    elif choice == "post":
                        post_=request.FILES['new_post']
                        fs = FileSystemStorage(location=settings.UPLOAD_POST_FOLDER)
                        filename = fs.save(post_.name, post_)
                        p=os.path.join( settings.UPLOAD_POST_FOLDER,post_.name)
                        posts.save()
                        return Response({'message':'post changed successfully'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)  
            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request, *args, **kwargs):
        serializer=PostDeleteSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            id=serializer.data['id']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    posts=Post.objects.get(id=id)
                    posts.delete()
                    return Response({'message':'post deleted successfully'},status=status.HTTP_202_ACCEPTED)

            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)

class Likes(APIView):
    def post(self,request,*args, **kwargs):
        serializer=LikeSerializer(data=request.data)
        if serializer.is_valid():
            user_id=serializer.data['user_id']
            post_id=serializer.data['post_id']
            try:
                posts=Post.objects.get(id=post_id)
                if posts:
                        try:              
                            user=Like.objects.filter(user_id=user_id,post_id=post_id)
                            if user:
                                return Response({'message':'user already liked that post'})  
                            else:
                                like=Like(user_id=user_id,post_id=post_id,like="True")
                                like.save()
                                posts.likes_count+=1
                                posts.save()
                                return Response({'message':'You liked post successfully'},status=status.HTTP_201_CREATED)
                                
                        except:
                            return Response({'message':'user already liked that post'})
                else:
                    return Response({'message':'Post not exist'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message':'Post not exist'},status=status.HTTP_400_BAD_REQUEST)

class Comments(APIView):
    def post(self,request,*args, **kwargs):
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            user_id=serializer.data['user_id']
            post_id=serializer.data['post_id']
            comments=serializer.data['comment']
            try:
                posts=Post.objects.get(id=post_id)
                if posts:
                    comment=Comment(user_id=user_id,post_id=post_id,comment=comments)
                    comment.save()
                    posts.comments_count+=1
                    posts.save()
                    return Response({'message':'You commented on  post successfully'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'message':'Post not exist'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message':'Post not exist'},status=status.HTTP_400_BAD_REQUEST)

class viewLikedPost(APIView):
    def get(self,request,*args, **kwargs):
        serializer=ViewLikedSerializer(data=request.data)
        if serializer.is_valid():
            user_id=serializer.data['user_id']
            likes=Like.objects.get(user_id=user_id)
            if likes:
                try:
                    posts=Post.objects.all(post_id=likes.post_id)
                    for i in posts:
                        return Response("i",status=status.HTTP_200_OK)
                except:
                    return Response({'message':'you didnt like any post'},status=status.HTTP_400_BAD_REQUEST)
class Follows(APIView):
    def post(self,request,*args, **kwargs):
        serializer=FollowSerializer(data=request.data)
        if serializer.is_valid():
            follower_id=serializer.data['follower_id']
            following_id=serializer.data['following_id']
            try:
                user=User.objects.get(id=following_id)
                if user:
                        try:              
                            follows=Follow.objects.filter(follower_id=follower_id,following_id=following_id)
                            if follows:
                                return Response({'message':'user already followed that acount'})  
                            else:
                                follow=Follow(follower_id=follower_id,following_id=following_id,folow="True")
                                follow.save()
                                user.follower+=1
                                user.save()
                                user1=User.objects.get(id=follower_id)
                                user1.following+=1
                                user1.save()
                                return Response({'message':'You followed successfully'},status=status.HTTP_201_CREATED)        
                        except:
                            return Response({'message':'user already followed that account'})
                else:
                    return Response({'message':'user you want to follow not exist'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message':'user you want to follow not exist'},status=status.HTTP_400_BAD_REQUEST)
class UnFollow(APIView):
    def post(self,request,*args, **kwargs):
        serializer=FollowSerializer(data=request.data)
        if serializer.is_valid():
            follower_id=serializer.data['follower_id']
            following_id=serializer.data['following_id']
            try:
                follows=Follow.objects.filter(follower_id=follower_id,following_id=following_id)
                if follows:
                    follows.delete()
                    user=User.objects.get(id=following_id)
                    user.follower-=1
                    user.save()
                    user1=User.objects.get(id=follower_id)
                    user1.following-=1
                    user1.save()
                    return Response({'message':'user unfollowed successfully'},status=status.HTTP_202_ACCEPTED)
                else:

                    return Response({'message':'you doesnt follow user'},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message':'you doesnt follow user'},status=status.HTTP_400_BAD_REQUEST)
class viewFollowingPosts(APIView):
    def get(self,request,*args, **kwargs):
        serializer=ViewFollowingPostSerializer(data=request.data)
        if serializer.is_valid():
            user_id=serializer.data['user_id']
            follows=Follow.objects.filter(following_id=user_id)
            if follows:
                try:
                    posts=Post.objects.all(user_id=serializer.data['following_id'])
                    for i in posts:
                        return Response("i",status=status.HTTP_200_OK)
                except:
                    return Response({'message':'you didnt like any post'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Not exist'})