from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
# Create your models here.

class Tbl_user(AbstractUser):
    Fld_Profile_pic=models.FileField( upload_to='profiles/', default="images/Screenshot from 2025-02-10 16-40-49.png", blank=True, null=True)

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
    Fld_Insurance_pic=models.FileField( upload_to='profiles/', default="images/Screenshot from 2025-02-10 16-40-49.png", blank=True, null=True)
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

