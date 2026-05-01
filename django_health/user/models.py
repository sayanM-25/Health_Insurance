from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
# Create your models here.

@deconstructible
class StaticImageStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(
            location=Path(__file__).resolve().parent / 'static' / 'user' / 'images',
            base_url='/static/user/images/',
        )


STATIC_IMAGE_STORAGE = StaticImageStorage()

class Tbl_user(AbstractUser):
    Fld_Profile_pic=models.FileField(storage=STATIC_IMAGE_STORAGE, upload_to='profile_pic/', default="profile_pic/default-profile.svg", blank=True, null=True)

    def __str__(self):
        return f"{self.username}"
    

class Tbl_insurance_plan(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE, related_name='insurance_plans')
    Fld_Plan_name = models.CharField(max_length=100)
    Fld_Description= models.CharField(max_length=100, default="N/A")
    Fld_Coverage_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    Fld_Premium = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    Fld_Period = models.CharField(max_length=7, choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')], default='Monthly')
    Fld_Coverage_details = models.TextField(default="N/A")
    Fld_Insurance_pic=models.FileField(storage=STATIC_IMAGE_STORAGE, upload_to='plan_pic/', default="plan_pic/default-plan.svg", blank=True, null=True)
    Fld_Category = models.CharField(max_length=20, choices=[('individual', 'Individual'),('family','Family'),('senior', 'Senior Citizens'),], default='individual')
    Fld_Validity = models.DateField(blank=True, null=True)
    Fld_Status = models.CharField(max_length=20, choices=[('active', 'Active'), ('expired', 'Expired'), ('pending', 'Pending')], default='pending')

    def __str__(self):
        return f"{self.Fld_Plan_name} - {self.user}"
    

class Tbl_cart(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE)
    plan = models.ForeignKey(Tbl_insurance_plan, on_delete=models.CASCADE)
    Fld_Quantity = models.PositiveIntegerField(default=1)
    is_hidden = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.plan} - {self.user}"
    

class Tbl_Family_member(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE, related_name='family_members')
    plan = models.ForeignKey(Tbl_insurance_plan, on_delete=models.SET_NULL, null=True, blank=True)
    Fld_Name = models.CharField(max_length=100)
    Fld_Plan_type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('family', 'Family')], default='individual')
    Fld_Member_count = models.PositiveIntegerField(default=1)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Fld_Name} - {self.user.first_name}"


class Tbl_Transaction(models.Model):
    user = models.ForeignKey(Tbl_user, on_delete=models.CASCADE)
    plan = models.ForeignKey(Tbl_insurance_plan, on_delete=models.SET_NULL, null=True)
    Fld_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Fld_Date = models.DateTimeField(auto_now_add=True)
    Fld_gst = models.DecimalField(max_digits=5, decimal_places=2)
    Fld_Total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    family_members = models.ManyToManyField(Tbl_Family_member)
    Fld_Paypal_transaction_id = models.CharField(max_length=50, blank=True, null=True) 
    Fld_Created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Fld_Expiration_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.Fld_Expiration_date:
            if self.plan:  
                if self.plan.Fld_Period == 'Monthly':
                    self.Fld_Expiration_date = self.Fld_Created_at + timedelta(days=30)
                elif self.plan.Fld_Period == 'Yearly':
                    self.Fld_Expiration_date = self.Fld_Created_at + timedelta(days=365)
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Transaction {self.id} by {self.user.username}"

