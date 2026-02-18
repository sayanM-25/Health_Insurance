from django.contrib import admin
from .models import Tbl_user,Tbl_insurance_plan,Tbl_cart,Tbl_Family_member,Tbl_Transaction

# Register your models here.
admin.site.register((Tbl_user,Tbl_insurance_plan,Tbl_cart,Tbl_Family_member,Tbl_Transaction))
# admin.site.register(Tbl_insurance_plan)

