from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Login(AbstractUser):
    user_type=models.CharField(max_length=30)
    view_password=models.CharField(max_length=30)

class Brand(models.Model):
    brandname=models.CharField(max_length=30)

class ServicehubReg(models.Model):
    hub_login=models.ForeignKey(Login,on_delete=models.CASCADE)
    hub_name=models.CharField(max_length=30,null=True)
    hub_image=models.ImageField()
    hub_phone=models.CharField(max_length=30,null=True)
    hub_email=models.EmailField(null=True)
    hub_address=models.TextField()
    hub_pin=models.CharField(max_length=30,null=True)
    district=models.CharField(max_length=30)
    hub_licence=models.FileField()

class HubBrands(models.Model):
    hub=models.ForeignKey(ServicehubReg,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    
class Message(models.Model):
    hub=models.ForeignKey(ServicehubReg,on_delete=models.CASCADE)
    message=models.CharField(max_length=30,null=True)
    sendby=models.CharField(max_length=30,null=True,default='admin')
    chatdate=models.DateTimeField(null=True)

class Faq(models.Model):
    hub=models.ForeignKey(ServicehubReg,on_delete=models.CASCADE)
    question=models.CharField(max_length=30)
    answer=models.CharField(max_length=30)

class Serviceproducts(models.Model):
    hubbrands=models.ForeignKey(HubBrands,on_delete=models.CASCADE,null=True)
    productname=models.CharField(max_length=30)

class UserReg(models.Model):
    user_login=models.ForeignKey(Login,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=30,null=True)
    last_name=models.CharField(max_length=30,null=True)
    user_phone=models.CharField(max_length=30,null=True)
    user_email=models.CharField(max_length=30,null=True)
    district=models.CharField(max_length=30)

class Troubleshoot(models.Model):
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE)
    hub=models.ForeignKey(ServicehubReg,on_delete=models.CASCADE)
    message=models.CharField(max_length=30,null=True)
    sendby=models.CharField(max_length=30,null=True,default='user')
    chatdate=models.DateTimeField(null=True)

class Complaint(models.Model):
    hub=models.ForeignKey(ServicehubReg,on_delete=models.CASCADE)
    serviceproduct=models.ForeignKey(Serviceproducts,on_delete=models.CASCADE)
    user=models.ForeignKey(UserReg,on_delete=models.CASCADE,null=True)
    completed_on=models.DateField(null=True)
    model=models.CharField(max_length=30)
    complaint_text=models.TextField()
    booked_on=models.DateField(null=True)
    submitdate=models.DateField(null=True)
    total=models.CharField(max_length=30,null=True)
    paid_on=models.DateField(null=True)
    payment_type=models.CharField(max_length=30,null=True)
    feedback_desc=models.TextField(null=True,blank=True)
    rating=models.CharField(max_length=30,null=True,blank=True)
    payment_status=models.CharField(max_length=30,default='Unpaid')
    complaint_status=models.CharField(max_length=30,default='Pending')

class ComplaintRequire(models.Model):
    complaint=models.ForeignKey(Complaint,on_delete=models.CASCADE)
    require_desc=models.TextField()
    require_price=models.CharField(max_length=30)