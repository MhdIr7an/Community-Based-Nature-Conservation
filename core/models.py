from django.db import models
from django.contrib.auth.models import AbstractUser


from django.utils import timezone

class Base_User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    user_type = models.IntegerField(default=1)
    contact = models.CharField(max_length=25, default='')
    location = models.CharField(max_length=255, default='')
    pincode = models.CharField(max_length=6, default='')
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Base_Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    task = models.CharField(max_length=255)
    organiser_id = models.ForeignKey(Base_User,on_delete=models.CASCADE)
    no_of_volunteers = models.IntegerField()
    event_date = models.DateField()

class Base_Volunteer(models.Model):
    volunteer_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Base_User,on_delete=models.CASCADE)
    event_id = models.ForeignKey(Base_Events,on_delete=models.CASCADE)

class Base_Issue(models.Model):
    issue_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Base_User,on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    img = models.ImageField()
    issues = models.CharField(max_length=255)
    issue_date = models.DateField()
    is_closed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

class Base_Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Base_User,on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, default='')
    img = models.ImageField()
    price = models.FloatField()
    stock = models.IntegerField()
    description = models.CharField(max_length=255)

class Base_Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey(Base_User,on_delete = models.CASCADE,related_name='Supplier_id')
    customer_id = models.ForeignKey(Base_User,on_delete=models.CASCADE,related_name='Customer_id')
    item_id = models.ForeignKey(Base_Items, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    date = models.DateTimeField()
    is_delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(default=None, null=True)
    is_cancelled = models.BooleanField(default=False)    

class Base_Resources(models.Model):
    resource_id = models.AutoField(primary_key=True)
    publisher_id = models.ForeignKey(Base_User,on_delete=models.CASCADE)
    published_file = models.FileField()
    published_date = models.DateTimeField()
    description = models.CharField(max_length=255)

# class Base_DonatorDetails(models.Model):
#     card_id = models.AutoField(primary_key=True)
#     card_number = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     expiry = models.CharField(max_length=255)
#     cvv = models.CharField(max_length=3)

class Base_Donations(models.Model):
    donation_id = models.AutoField(primary_key=True)
    donator_id = models.ForeignKey(Base_User, on_delete=models.CASCADE)
    # donator_details = models.ForeignKey(Base_DonatorDetails, on_delete=models.CASCADE, default='')
    amount = models.FloatField()
    dated = models.DateTimeField()

class Base_Discussions(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Base_User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    issue_id = models.ForeignKey(Base_Issue, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)