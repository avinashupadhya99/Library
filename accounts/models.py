from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)  
    phoneNumber = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=4)
    semester = models.IntegerField(null=True, blank=True)

    def __str__(self):  
        return self.user.first_name + '(' + self.user.username + ')' 

class OTP(models.Model):
    regno = models.CharField(max_length=10)
    otp = models.IntegerField()

    def __str__(self):
        return self.regno + '(' + str(self.otp) + ')'


