from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=120, null=False)
    middlename = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120, null=False)
    date_of_birth = models.DateField()


class Account(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=25, null=False)
    account_name = models.CharField(max_length=225, null = False)
    account_number = models.CharField(max_length=120, null=False)
    available_amount = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)


class DepositTransaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    created_on = models.DateField(auto_now_add=True)


class TransferTransaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=30,null=False, default="bank_name")
    country = models.CharField(max_length=30,null=False,default="country")
    to_account_number = models.CharField(max_length=30,null=False,default="to_account_number")
    to_account_name = models.CharField(max_length=30,null=False,default="to_account_name")
    initialized_on = models.DateField(auto_now_add=True)
    amount = models.IntegerField(null=False)
    status = models.CharField(max_length=25, default='pending')
