from django.db import models

# Create your models here.
import random
def otp():
    otp = ''.join(random.choices('0123456789', k=4))
    return otp

class createBank(models.Model):
    bankname=models.CharField( max_length=50)
    bankemail=models.EmailField(unique=True)
    bankpassword=models.CharField(max_length=100)
    def __str__(self):
        return self.bankname



class registerUser(models.Model):
    username=models.CharField(max_length=50)
    useremail=models.EmailField()
    accountno=models.CharField(max_length=100,unique=True)
    amount=models.IntegerField()
    userbank=models.ForeignKey(createBank, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.username

class validateUser(models.Model):
    email=models.EmailField()
    accountno=models.CharField(max_length=100)
    otp=models.CharField(max_length=4,default=otp(),blank=True)

class SignupUser(models.Model):
    password=models.CharField( max_length=50)
    pin=models.CharField(max_length=4)
    userdetails=models.OneToOneField(registerUser,on_delete=models.CASCADE,null=True)
class Transaction(models.Model):
    toaccountno=models.CharField(max_length=100)
    fromaccountno=models.CharField(max_length=100,blank=True)
    frombank=models.ForeignKey(createBank,on_delete=models.CASCADE,related_name="frombank",blank=True)
    tobank=models.ForeignKey(createBank,on_delete=models.CASCADE,related_name="tobank",blank=True)
    amount=models.IntegerField()
    transferred_at=models.DateTimeField(auto_now=True)





