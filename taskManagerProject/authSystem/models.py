from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    picture = models.ImageField(
        upload_to='profilePics', default='blankUser.jpeg')
    notificationsOn = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.id} - {self.user.username}'