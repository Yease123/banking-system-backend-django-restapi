from rest_framework import serializers
from .models import registerUser,createBank,validateUser,SignupUser,Transaction
from rest_framework_simplejwt.tokens import AccessToken

class BankLoginSerializers(serializers.Serializer):
  
    bankemail=serializers.EmailField(max_length=50)
    bankpassword=serializers.CharField(max_length=100)
        
       

class BankLoginChangeSerializer(serializers.Serializer):
    oldpassword=serializers.CharField(max_length=100)
    bankpassword=serializers.CharField(max_length=100)
        

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
       model=registerUser
       fields="__all__"
    def create(self, validated_data):
        try:
           token=self.context.get('token')
           access_token=AccessToken(token)
           bankemail=access_token.get('email')
           bankobj=createBank.objects.get(bankemail=bankemail)
           if bankobj:
               validated_data['userbank']=bankobj
           else:
               raise serializers.ValidationError("you are not allowed to add user")
        except Exception as error:
            raise serializers.ValidationError("you are not allowed to add user")
        return super().create(validated_data)
   
class ValidateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=validateUser
        fields='__all__'
    def validate(self, attrs):
        accountno=attrs.get('accountno')
        email=attrs.get('email')
        try:
           
           userexists=SignupUser.objects.get(userdetails__accountno=accountno)
           raise serializers.ValidationError("user already signup")
        except SignupUser.DoesNotExist:
            pass

        try:
                deleteuser=validateUser.objects.filter(accountno=accountno,email=email)
                if deleteuser.exists():
                      deleteuser.delete()
                      deleteuser.save()
        except Exception as error:
                pass
               
        
        try:
            userdata=registerUser.objects.filter(useremail=email,accountno=accountno)
            if not  userdata:
                raise serializers.ValidationError("provided credentials are invalid")
            else:
               return super().validate(attrs)
        except Exception as error:
             print(error)
             raise serializers.ValidationError("provided credentials are invalid")
class validateotpSerializer(serializers.Serializer):
    otp=serializers.CharField()
    def validate(self, attrs):
        try:
           token=self.context.get("token")
           access_token=AccessToken(token)
           accountno=access_token.get('accountno')
           userdata=validateUser.objects.get(accountno=accountno)
           tokenotp=userdata.otp
           
           otp=attrs.get('otp')
           print(otp,tokenotp)
           if tokenotp==otp:
               return super().validate(attrs)
           else:
               raise serializers.ValidationError("Wrong otp")
        except Exception as error:
            raise serializers.ValidationError("Wrong otp")
        
        
class  SignupuserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SignupUser
        exclude=['userdetails']
    def validate(self, attrs):
       
            token=self.context.get('token')
            access_token=AccessToken(token)
            accountno=access_token.get("accountno")
            try:
                userunique=SignupUser.objects.get(userdetails__accountno=accountno)
                if  userunique:
                  raise serializers.ValidationError("you are  alreay signup")
            except SignupUser.DoesNotExist:
              pass
            return super().validate(attrs)
    
    def create(self, validated_data):
        try:
            token=self.context.get('token')
            access_token=AccessToken(token)
            accountno=access_token.get("accountno")
            
           
            
            user=registerUser.objects.get(accountno=accountno)
            if user:
                print(user)
                validated_data['userdetails']=user
            else:
                raise serializers.ValidationError("User are not auhorized")

        except Exception as error:
           raise serializers.ValidationError({"error":"some server error occur"})
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    accountno=serializers.CharField()
    password=serializers.CharField()

    def validate(self, attrs):
        accountno=attrs.get("accountno")
        password=attrs.get('password')
        try:
           uservalid=SignupUser.objects.get(password=password,userdetails__accountno=accountno)
        except SignupUser.DoesNotExist:
            
            raise serializers.ValidationError("The account number is not registered.")
        except Exception as error:
            raise serializers.ValidationError("Some server error occur")

        return super().validate(attrs)
class trancationserializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields="__all__"
    def validate(self, attrs):
        try:
            toaccountno=attrs.get('toaccountno')
            userdata=registerUser.objects.get(accountno=toaccountno)
        except registerUser.DoesNotExist:
          raise serializers.ValidationError("Reciver account is not found")
        except Exception as error:
            raise serializers.ValidationError("some server error occur")
        return super().validate(attrs)
    

    def create(self, validated_data):
        token=self.context.get('token')
        access_token=AccessToken(token)
        fromaccountno=access_token.get('accountno')
        toaccountno=validated_data.get('toaccountno')
        try:
            tobankdata=registerUser.objects.get(accountno=toaccountno)
            frombankdata=registerUser.objects.get(accountno=fromaccountno)
            validated_data['tobank']=tobankdata.userbank
            validated_data['frombank']=frombankdata.userbank
            validated_data['fromaccountno']=fromaccountno
        except Exception as error:
           print(error)
           raise serializers.ValidationError("some server error occur")


        
        
      
        return super().create(validated_data)
    

class ShowTransactionSerializers(serializers.ModelSerializer):
     frombank_name = serializers.CharField(source='frombank.bankname', read_only=True)
     tobank_name = serializers.CharField(source='tobank.bankname', read_only=True)
     class Meta:
         model=Transaction
         fields = ['id', 'toaccountno', 'fromaccountno', 'amount', 'transferred_at', 'frombank_name', 'tobank_name']
        
