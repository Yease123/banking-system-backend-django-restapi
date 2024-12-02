from django.contrib import admin
from .models import createBank,registerUser,validateUser,SignupUser,Transaction
# Register your models here.
@admin.register(createBank)
class adminCreateBank(admin.ModelAdmin):
    list_display=["id","bankname","bankpassword","bankemail"]
    ordering=['id']

@admin.register(registerUser)
class adminCreateBank(admin.ModelAdmin):
    list_display=["id","username","useremail","userbank","amount","accountno"]
    ordering=['id']
@admin.register(validateUser)
class adminCreateBank(admin.ModelAdmin):
    list_display=["id","email","accountno","otp"]
    ordering=['id']
@admin.register(SignupUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['id',"password","pin","userdetails"]
    ordering=['id']
@admin.register(Transaction)
class admintranscation(admin.ModelAdmin):
    list_display=["id","fromaccountno","toaccountno","frombank","tobank","amount","transferred_at"]
    ordering=['id']