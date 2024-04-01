from django.db import models
from SocialMedia import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    Roles = (
    (1, "User"),
    (2, "Moderator"),
    (3, "Admin"),
  )
    email = models.EmailField(unique=True)
    roles = models.IntegerField(choices=Roles, default=1)
    image=models.ImageField(null=False,blank=True,upload_to=settings.UPLOAD_PROFILE_FOLDER)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='my_users_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='my_users_permissions',
        blank=True,
    )
    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    caption=models.CharField(max_length=1000)
    post=models.FileField(null=False,blank=True,upload_to=settings.UPLOAD_POST_FOLDER, validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','jpeg','mp4'])])
    likes_count=models.IntegerField(null=False,blank=True,default=0)
    comments_count=models.IntegerField(null=False,blank=True,default=0)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments',null=True)
    comment=models.CharField(max_length=200,null=False,blank=True)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes',null=True)
    like=models.BooleanField(default=False)
