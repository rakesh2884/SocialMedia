from django.db import models
from SocialMedia import settings
from django.core.validators import FileExtensionValidator

class User(models.Model):
    Roles = (
    (1, "User"),
    (2, "Moderator"),
    (3, "Admin"),
  )
     
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=1000,null=False)
    roles = models.IntegerField(choices=Roles, default=1)
    email=models.EmailField(null=False,blank=True)
    image=models.ImageField(null=False,blank=True,upload_to=settings.UPLOAD_PROFILE_FOLDER)

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption=models.CharField(max_length=1000)
    post=models.FileField(null=False,blank=True,upload_to=settings.UPLOAD_POST_FOLDER, validators=[FileExtensionValidator(allowed_extensions=["jpg",'png','jpeg','mp4'])])
    likes_count=models.IntegerField(null=False,blank=True,default=0)
    comments_count=models.IntegerField(null=False,blank=True,default=0)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment=models.CharField(max_length=200,null=False,blank=True)
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    Like=models.BooleanField(default=False)
