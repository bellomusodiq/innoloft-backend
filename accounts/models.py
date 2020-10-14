from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house_number = models.CharField(max_length=100)
    street = models.CharField(max_length=400)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.username
