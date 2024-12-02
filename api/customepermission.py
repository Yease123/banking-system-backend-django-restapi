from rest_framework.permissions import BasePermission
from .models import createBank,registerUser,SignupUser
from rest_framework_simplejwt.tokens import AccessToken
class LoginChangeValidation(BasePermission):
    def has_permission(self, request, view):
     try:
        token=request.headers.get('Authorization')
        access_token=AccessToken(token)
        bankemail=access_token.get('email')
        bankpassword=access_token.get('password')
      
        bankdata=createBank.objects.get(bankemail=bankemail,bankpassword=bankpassword)
        if bankdata:
               return True
        else:
               return False
           
     except Exception as error:
            return False

class otpvalidation(BasePermission):
     def has_permission(self, request, view):
         
          try:
              token=request.headers.get('Authorization')
              access_token=AccessToken(token)
              email=access_token.get('email')
              accountno=access_token.get('accountno')
              userdata=registerUser.objects.filter(accountno=accountno,useremail=email)
              if userdata.exists():
                   return True
              else:
                   return False

          except Exception as error:
              return False


class transactionvalidation(BasePermission):
     def has_permission(self, request, view):
          token=request.headers.get('Authorization')
          if token:
               access_token=AccessToken(token)
               email=access_token.get('email')
               accountno=access_token.get('accountno')
               id=access_token.get('id')
               password=access_token.get('password')
               pin=access_token.get('pin')
               try:
                    userdata=SignupUser.objects.get(id=id,password=password,userdetails__accountno=accountno)

               except SignupUser.DoesNotExist:
                    return False
               except Exception as error:
                    print(error)
                    return False
               return True
          else:
               return False
          

class eitherpermission(BasePermission):
   def has_permission(self, request, view):
        token=request.headers.get('Authorization')
        if not token:
             return False
        
        try:
          access_token=AccessToken(token)
          email=access_token.get('email')
          password=access_token.get('password')
          accountno=access_token.get('accountno')
          userdata=SignupUser.objects.get(password=password,userdetails__accountno=accountno)
        except Exception as error:
             print(error)
             try:
              bankdata=createBank.objects.get(bankemail=email,bankpassword=password)
             except createBank.DoesNotExist:
                    return False
             except Exception as error:
              
               return False
             return True
        return True
          
