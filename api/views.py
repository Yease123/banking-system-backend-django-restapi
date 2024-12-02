from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BankLoginSerializers,BankLoginChangeSerializer,RegisterUserSerializer,ValidateUserSerializer,validateotpSerializer,SignupuserSerializer,LoginSerializer,trancationserializer,ShowTransactionSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import createBank,registerUser,validateUser,SignupUser,Transaction
from rest_framework_simplejwt.tokens import AccessToken
from .customepermission import LoginChangeValidation,otpvalidation,transactionvalidation,eitherpermission
from .customethrottle import changeBankthrottle
from django.db.models import Q
def get_tokens_for_Banklogin(user):
    refresh = RefreshToken.for_user(user)

    refresh['email']=user.bankemail
    
    refresh['password']=user.bankpassword

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class BankLoginApi(APIView):
    def post(self,request,fromat=None):
        serializers=BankLoginSerializers(data=request.data)
        if serializers.is_valid():
            try:
                 bankemail=serializers.validated_data.get('bankemail')
                 bankpassword=serializers.validated_data.get('bankpassword')
                 bankdata=createBank.objects.get(bankemail=bankemail,bankpassword=bankpassword)
                 if bankdata:
                    token=get_tokens_for_Banklogin(user=bankdata)
                    return Response({"success":"You are loggedin sucessfully","token":token},status=status.HTTP_200_OK)
            except Exception as error:
                return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)

               
        else:
            return Response(serializers.errors,status=status.HTTP_401_UNAUTHORIZED)

class ChangeBankApi(APIView):
    throttle_classes=[changeBankthrottle]
    permission_classes=[LoginChangeValidation]
   
    def post(self,request,format=None):
       
            try:
             serializers=BankLoginChangeSerializer(data=request.data)
             if serializers.is_valid():
               bankpassword=serializers.validated_data.get('bankpassword')
               oldpassword=serializers.validated_data.get('oldpassword')
               token=request.headers.get('Authorization')
               access_token=AccessToken(token)
               email=access_token.get('email')
               print(email)
               bankdata=createBank.objects.get(bankemail=email)
               if bankdata.bankpassword==oldpassword:
                bankdata.bankpassword=bankpassword
                bankdata.save()
                return Response({"sucess":"Your Password is updated sucessfully"},status=status.HTTP_200_OK)
               else:
                   return Response({"success":"Your old password is invalid try again"},status=status.HTTP_406_NOT_ACCEPTABLE)
             else:
                return Response({"error":serializers.errors})
            except Exception as error:
                return Response({"error":"you are not allowed to change password"},status=status.HTTP_406_NOT_ACCEPTABLE)
       
                

class RegisterUserApi(APIView):
    permission_classes=[LoginChangeValidation]
    def post(self,request,format=None):
        try:
           
            serializers=RegisterUserSerializer(data=request.data,context={"token":request.headers.get("Authorization")})
            if serializers.is_valid():
                
                user=serializers.save()
                print(user)
                return Response({"success":"User added Sucessfully"},status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors)
        
        except Exception as error:
             print(error)
             return Response({"error":"server error occur"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
    def put(self,request,pk,format=None):
         try:
            userdata=registerUser.objects.get(id=pk)
            serializers=RegisterUserSerializer(userdata,data=request.data)
            if serializers.is_valid():
              serializers.save()
              return Response({"success":"User data edited Sucessfully"},status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors)
        
         except Exception as error:
             return Response({"error":"some server error occur"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_tokens_for_validateuser(user):
    refresh = RefreshToken.for_user(user)

    refresh['email']=user.email
    
    refresh['accountno']=user.accountno
    refresh['id']=user.id
    refresh['otp']=user.otp
   

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class ValidateUserApi(APIView):
    throttle_classes=[changeBankthrottle]
    def post(self,request,format=None):
        try:
            serializers=ValidateUserSerializer(data=request.data)
            if serializers.is_valid():
                user=serializers.save()
                token=get_tokens_for_validateuser(user)
                return Response({"success":"otp is send to your email verify yourself",'token':token},status=status.HTTP_200_OK)
            else:
                return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


        except Exception as error:
            print(error)
            return Response({"error":"some server error occurs"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def get_tokens_for_otpvalidation(user):
    refresh = RefreshToken.for_user(user)

    refresh['email']=user.useremail
    
    refresh['accountno']=user.accountno
    
    refresh['id']=user.id
    
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class ValidateOtpApi(APIView):
    permission_classes=[otpvalidation]
    def post(self,request,format=None):
        token=request.headers.get('Authorization')
        serializers=validateotpSerializer(data=request.data,context={'token':token})
        if serializers.is_valid():
            try:
                
                if token:
                    access_token=AccessToken(token)
                    email=access_token.get('email')
                    accountno=access_token.get('accountno')
                    userdata=registerUser.objects.get(useremail=email,accountno=accountno)
                    generatetoken=get_tokens_for_otpvalidation(user=userdata)
                    return Response({"success":"Your are Verified now set up your credentials","token":generatetoken})
                else:
                     return Response({"error":"Your are not Authorized"})
            except Exception as error:
                print(error)
                return Response({"error":"some server error occur"})
        else:
            return Response(serializers.errors)



class SignupUserApi(APIView):
    permission_classes=[otpvalidation]
    def post(self,request,format=None):
        serializers=SignupuserSerializer(data=request.data,context={"token":request.headers.get('Authorization')})
        if serializers.is_valid():
            serializers.save()
            return Response({"success":"You have created your Password and Pin"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)
        

def get_tokens_for_userlogin(user):
    refresh = RefreshToken.for_user(user)

    refresh['email']=user.userdetails.accountno
    
    refresh['accountno']=user.userdetails.accountno
    
    refresh['id']=user.id
    refresh['password']=user.password
    refresh['pin']=user.pin
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class LoginusersApi(APIView):
    def post(self,request,format=None):
        serializers=LoginSerializer(data=request.data)
        if serializers.is_valid():
            accoutno=serializers.validated_data.get('accountno')
            try:
                userdata=SignupUser.objects.get(userdetails__accountno=accoutno)
                token=get_tokens_for_userlogin(user=userdata)
            except Exception as error:
                return Response({"error":"some server error "})
            return Response({"success":"You are logged in successfully","token":token})
        else:
            return Response(serializers.errors)
        
from django.db import transaction
class transactionApi(APIView):
    permission_classes=[transactionvalidation]
    def post(self,request,format=None):
        token=request.headers.get("Authorization")
        pin=request.data.get('pin')
        if not pin:
            return Response({"error":"Please enter a pin"})
        serilalizers=trancationserializer(data=request.data,context={"token":token})
        if serilalizers.is_valid():
            access_token=AccessToken(token)
            realpin=access_token.get('pin')
            if realpin!=pin:
                return Response({"error":"Invalid Pin"})
            try:
              
               fromdata=registerUser.objects.get(accountno=access_token.get('accountno'))
               todata=registerUser.objects.get(accountno=serilalizers.validated_data.get('toaccountno'))
            except Exception as error:
                print(error)
                return Response({"error":"Some server error occur"})
            with transaction.atomic():
                fromdata.amount=fromdata.amount-serilalizers.validated_data.get('amount')
                todata.amount=todata.amount+serilalizers.validated_data.get('amount')
                fromdata.save()
                todata.save()

                serilalizers.save()
            return Response({"success":"Transcation successfull"})
        else:
            return Response(serilalizers.errors)
        
class Showtransactionapi(APIView):
    permission_classes=[eitherpermission]
    def get(self,request,format=None):
        try:
           token=request.headers.get('Authorization')
           access_token=AccessToken(token)
           email=access_token.get('email')
           
           accountno=access_token.get('accountno')
           if accountno:
                transactions =Transaction.objects.filter(Q(toaccountno=accountno) | Q(fromaccountno=accountno))
           else:
               transactions =Transaction.objects.filter(Q(frombank__bankemail=email) | Q(tobank__bankemail=email))
          
           serializers=ShowTransactionSerializers(transactions,many=True)
           return Response({"data":serializers.data},status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({"error":"Some server error occur"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        