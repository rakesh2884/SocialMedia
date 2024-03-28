from django.db import models


class User(models.Model):
    Roles = (
    (1, "User"),
    (2, "Moderator"),
    (2, "Admin"),
  )
     
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=1000)
    roles = models.IntegerField(choices=Roles, default=1)
    email=models.EmailField()
    image=models.ImageField(null=False,upload_to='social_platform/media')

    def __str__(self):
        return self.name