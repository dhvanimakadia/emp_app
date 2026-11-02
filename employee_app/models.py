from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
     name = models.CharField(max_length=30, null=False)
     location = models.CharField(max_length=30)


     def __str__(self):
         return self.name

class Role(models.Model):
     name = models.CharField(max_length=30, null=False)

     def __str__(self):
         return self.name

class Employee(models.Model):
     first_name = models.CharField(max_length=30,null=False)
     last_name = models.CharField(max_length=30,null=False)
     dept = models.ForeignKey(Department, on_delete=models.CASCADE)
     salary = models.IntegerField(default=0)
     bonus = models.IntegerField(default=0)
     role = models.ForeignKey(Role, on_delete=models.CASCADE)
     phone = models.IntegerField(default=0)
     hire_date = models.DateField()

     def __str__(self):
         return f"{self.first_name} {self.last_name} {self.phone}"

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username