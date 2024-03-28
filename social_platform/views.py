from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from .models import User
from django.core.files.storage import FileSystemStorage
import os
import re
from .serializers import userProfileSerializer,LoginSerializer,ViewAccountSerializer,AccountUpdateSerializer,AccountDeleteSerializer


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = userProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            image=request.FILES['image']
            fs = FileSystemStorage(location=settings.UPLOAD_FOLDER)
            filename = fs.save(image.name, image)
            i=os.path.join( settings.UPLOAD_FOLDER,image.name)
            try:
                user=User.objects.get(username=username)
                if user:
                    return Response({'message':'user already exist'},status=status.HTTP_400_BAD_REQUEST)
            except:    
                if len(password) < 8:
                    return Response({'message':'Make sure your password is at lest 8 letters'},status=status.HTTP_400_BAD_REQUEST) 
                elif re.search('[0-9]',password) is None:
                    return Response({'message':'Make sure your password has a number in it'},status=status.HTTP_400_BAD_REQUEST)
                elif re.search('[A-Z]',password) is None: 
                    return Response({'message':'Make sure your password has a capital letter in it'},status=status.HTTP_400_BAD_REQUEST)
                elif re.search('[^a-zA-Z0-9]',password) is None:
                    return Response({'message':'Make sure your password has a special character in it'},status=status.HTTP_400_BAD_REQUEST) 
                elif password!=serializer.data['confirm_password']:
                    return Response({'message':'password not match'},status=status.HTTP_400_BAD_REQUEST)
                user=User(username=username,password=make_password(password),email=serializer.data['email'],roles=serializer.data['roles'],image=i)
                user.save()
                return Response({'message':'Register successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    return Response({'message':'Login successful','token':token,'image':str(user.image)},status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    def get(self, request, *args, **kwargs):
        serializer=ViewAccountSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.data['username']
            password=serializer.data['password']
            try:
                user = User.objects.get(username=username)
                if user and check_password(password,user.password):
                    return Response({'username':user.username,'password':password,'role':user.Roles[user.roles-1],'email':user.email,'image':str(user.image)},status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':'Enter All Fields'},status=status.HTTP_400_BAD_REQUEST)
            

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
                        i=os.path.join( settings.UPLOAD_FOLDER,image.name)
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
        serializer=AccountDeleteSerializer(data=request.data)
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