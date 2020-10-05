from django.db import models

# Create your models here.


class Account(models.Model):
    userid = models.CharField(primary_key=True, max_length=200, blank=False)
    password = models.CharField(max_length=500, blank=True)
    user_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    user_email = models.EmailField(max_length=100, blank=True)
    phonenumber = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "accounts"
