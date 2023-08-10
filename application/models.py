from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class Category(models.Model):
    slug = models.CharField(max_length=150,null=False,blank=False,unique=True)
    name = models.CharField(max_length=150,null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    slug = models.CharField(max_length=150,null=False,blank=False,unique=True)
    name = models.CharField(max_length=150,null=False,blank=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False,blank=False)
    price = models.FloatField(null=False,blank=False)
    show_price = models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    special_product = models.BooleanField(default= False, help_text= "if product is special tick it or leave it unticked")
    on_sale = models.BooleanField(default= False, help_text= "if product is on-sale tick it or leave it unticked")
    image = models.ImageField(upload_to="product",null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
status = (
    ("Pending" , "Pending"),
    ("Shipped" , "Shipped"),
    ("Delivered" , "Delivered"),
)
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField(default=0)
    phone = models.CharField(max_length=15)
    house = models.CharField(max_length= 400)
    location = models.CharField(max_length= 500)
    city = models.CharField(max_length= 50)
    pincode = models.CharField(max_length= 400)
    landmark = models.CharField(max_length= 400)
    status = models.CharField(max_length= 20, choices=status,default="Pending")
    date = models.DateField(default= datetime.today)
    
    def __str__(self):
        return (self.product.name +" ----- + by + -----  " + self.user.username)
    
    
    
class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=150)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    
