

from django.db import models
from django.contrib.auth.models import User


class Train(models.Model):
    train_number = models.IntegerField()
    train_name = models.CharField(max_length=100)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    available = models.IntegerField(default=0)
    fare = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(null=True, default=None)
    time = models.TimeField(null=True, default=None)
    
    # Add any additional fields as needed

    def __str__(self):
        return str(self.train_number)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=15)
    mailid = models.EmailField()

    def __str__(self):
        return self.user.username
    
class Passenger(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    nationality = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    berth = models.CharField(max_length=20)
    acCategory = models.CharField(max_length=50)

    def __str__(self):
        return self.name
