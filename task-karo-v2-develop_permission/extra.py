from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from api.serializers import *
from api.create_token import *
from api.models import *
from fcm_django.models import FCMDevice
from rest_framework.decorators import api_view,action
from rest_framework import viewsets,status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .api.helpers import send_otp_to_phone
from  .api.models import User
from decouple import config
from rest_framework.views import APIView
import boto3 
from botocore.exceptions import NoCredentialsError
from firebase_admin.messaging import Message, Notification

from django.contrib.auth.hashers import make_password , check_password
from .api.mypaginations import MyLimitOffsetpagination
import random
import math
import requests
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


# Create your views here.

#USER API    
class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    http_method_names = ['get','post','put','delete']
    # pagination_class = MyLimitOffsetpagination

    # add user post
    def create(self,request):
        serializer = User_Serializer(data = request.data)
        mobile_number = request.data['mobile_number']
        
        if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status' : 500 , 'errors' : serializer.errors ,'message' : 'something went wrong'})
        
        data = serializer.validated_data
        new_user = serializer.save()
     

        # Either use this
        new_user.password = make_password(request.data['password'])
        print(new_user.password)

        new_user.save()
        user = User.objects.get(user_id = new_user.user_id) 
        token = create_token(user=user)
        return Response({'data' : serializer.data , 
                        "status_code": 200,
                        "response_error": False,
                        'status_message': "User data added successfully!",
                        'token':token})         

    # all user get
    def list(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            user = User.objects.filter(user_id = user)
            serializer = User_Serializer(instance=user,many=True)
            return Response({'data' : serializer.data,
            "status_code": 200,
            "response_error": False,

           'status_message': "User data fetched successfully!",
            'token':token})
    
        else:
            return Response({"status":0,"message":"Invalid credentials"})

        # token = request.META.get("HTTP_AUTHORIZATION")
        # user = decrypt_token(token) 
        # if user:
        #     try:
        #         user = User.objects.all()
        #         serializer = User_Serializer(user,many = True)
        #         print(serializer)
        #         return Response(serializer.data)
        #     except:
        #         return Response({"status":0,"message":"Invalid credentials"})
        # else:
        #     return Response({"status":0,"message":"Invalid credentials"})
       


    # update  user with put
    def update(self,request, pk):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            try:
                user = User.objects.get(user_id = pk)
            except:
                return Response({'status':200,'massage':'user not found'})
            serializer = User_Serializer(user,data = request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(user_id = pk)
                token = create_token(user=user)
                return Response({'data' : serializer.data,
                "status_code": 200,
                "response_error": False,

               'status_message': "User data updated successfully!",
                'token':token})
            return Response({'data' : serializer.data,
            "status_code": 200,
            "response_error": False,
            'errors' : serializer.errors,
            'token':token}) 
        else:
            return Response({"status":0,"message":"Invalid credentials"})
   
    #  user find by id get
    def retrieve(self, request, pk=None):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            if id is not None:
                try:
                    user = User.objects.get(user_id=pk)
                except:
                    return Response({'status':200 , 'massage':'user not found'})
                serializer = User_Serializer(user)
                return Response(serializer.data)

                # user = User.objects.all()
            serializer = User_Serializer(user,many = True)
            return Response(serializer.data)
        else:
            return Response({"status":0,"message":"Invalid credentials"})
    
    # delete user 
    def destroy(self,request,pk):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            try:
                user = User.objects.get(user_id = pk)
                user.is_active = False
                user.delete()
                return Response({'status' : 200,'msg':'data deleted'})
            except Exception as e:
                print(e)
                return Response({'status' : 500,'message' : 'invalid id'})
        else:
            return Response({"status":0,"message":"Invalid credentials"})
     
    @action(methods=['post'], detail=False)
    def login(self, request):
        mobile_number = request.data.get("mobile_number")
        email = request.data.get("email")
        password = request.data.get("password")
        print(mobile_number)
        print(email)
        print(password)
        if mobile_number:
            try:
                user = User.objects.get(mobile_number=mobile_number)
            except:
                return Response({'status':200,'massage':'user not found'})
            if user.mobile_number == mobile_number:
                if user.check_password(password):   
                    token = create_token(user=user)
                    return Response({"data": mobile_number,'status' : 200,'msg':'login success','token':token})
                else:
                    return Response({'status':200,'massage':'invalid password'})
            return Response({'status':200,'msg':" this is from number"})
        else:
            try:
                user = User.objects.get(email=email)
            except:
                return Response({'status':200,'massage':'user not found'})
            if user.email == email:
                if user.check_password(password):   
                    token = create_token(user=user)
                    return Response({"data": email,'status' : 200,'msg':'login success','token':token})
                else:
                    return Response({'status':200,'massage':'invalid number'})
            return Response({'status':200,'msg':" this is from email"})


#  if mobile_number is None or password is None:
#             return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
        
#         user = User.objects.filter(mobile_number=mobile_number).first()
#         email = User.objects.filter(email=email)
#         if not user:
#             return Response({'error': 'Invalid Credentials'})
            
#         if not user.check_password(password):
#             return Response({'error': 'Invalid Credentials'})
            
#         token = Token.objects.get_or_create(user=user)
#         return Response({'token': token[0].key}, status=HTTP_200_OK)
        

#  api/user/tranding
# send_otp
@api_view(['POST'])
def send_otp(request):
    mobile_number =request.data["mobile_number"]
    # print(mobile_number)
    # email = request.data["email"]
    try:
        user = User.objects.get(mobile_number=mobile_number)
        
    except:
        return Response({'msg error':'mobile num not matched'})
        
    if user.mobile_number==mobile_number:
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        # opt = OTPs.objcts.create(OTPs :random_str)
        # otp.save()
        # user_model = User.objects.get(mobile_number=mobile_number)

        url = "https://www.fast2sms.com/dev/bulkV2"
        
        payload = "message={} is the Verification code to log in your Task-Karo account. DO NOT share this code&language=english&route=q&numbers={} ".format(random_str,user.mobile_number)
        headers = {
            'authorization': "kA1TXCPzK2BH7JtmqineSV5FxboZ8EMch4gIwfR9Wl6rpvYus3LqRkKJFhbm8WdXZQBN2xu7wcT9IU0H",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)

        otp = OTPs.objects.create(user=user,otp=random_str)
        otp.save()
        return Response({'status': 200,'otp' : random_str})
     

@api_view(['POST'])
def Verify_OTP(request):
    mobile_number =request.data["mobile_number"]
    otp = request.data["otp_no"]
    try:
        user = User.objects.get(mobile_number=mobile_number)
    except:
        return Response({'msg error':'mobile num not matched'})

    if user.mobile_number==mobile_number:
        otp = OTPs.objects.get(user=user,otp=otp)
        if otp.otp == otp.otp:
            user.is_active = True
            user.save()
            return Response({'status': 200,'msg' : 'otp verified'})
            # return Response({'status': 200,'msg' : 'otp verified'})
        else:
            return Response({'status': 500,'msg' : 'invalid otp'})
    
    


# Parent User Update : updateProfile/id PUT (USER API)
@api_view(['PUT'])
def updateParent(request,user_id):
    user_id = user_id 
    user = User.objects.get(pk = user_id)
    serializer = User_Serializer(user,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'data' : serializer.data})
    return Response({'status': 500 , 'errors' : serializer.errors})


    
# Add Member (USER API)
@api_view(['GET'])
def add_member(request,user_id): 
    
    
   ############################
    if id is not None:
        user = User.objects.get(user_id=user_id)
        serializer = User_Serializer(user)
        return Response(serializer.data)

    user = User.objects.all()
    serializer = User_Serializer(user,many = True)
    return Response(serializer.data)
   

# file upload (post) (USER API)
class ExampleView(viewsets.ViewSet):
    def create(self,request):
        # token = request.META.get("HTTP_AUTHORIZATION")
        # user = decrypt_token(token)  
        # if user:
        user_image = request.FILES.get('user_image')
        # print(user_image)
        if not user_image:
            return Response({"data": {},
            "status_code": 400,
            "status_message": "Please send attachment to upload.",
            "response_error": True
            })
        s3 = boto3.client('s3', aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'))
        try:
            s3.upload_fileobj(user_image,config('AWS_STORAGE_BUCKET_NAME'), f'media/{user_image.name}',ExtraArgs={'ACL':'public-read'})
            response = f"https://{config('AWS_STORAGE_BUCKET_NAME')}.s3.{config('AWS_S3_REGION_NAME')}.amazonaws.com/media/{user_image.name}"
            return Response({'data':response,       
                            "status_code": 200,
                            "status_message": "Document uploaded",
                            "response_error": True})
        except :
            return Response({'status':500,'status_message':'Seems our server is having problem to serve you new access token. Try to login again.'})


# util by get (USER API)
@api_view(['GET'])
def util(request):
    util = {
        "user-relation": [
            {
            "relation": "self",
            'id': 1,
            },
            {
            "relation": "Brother",
            'id': 2,
            },
            {
            "relation": "Sister",
            'id': 3,
            },
            {
            "relation": "Father",
            'id': 4,
            },
            {
            "relation": "Mother",
            'id': 5,
            },
            {
            "relation": "Cousin",
            'id': 6,
            },
            {
            "relation": "Grand Father",
            'id': 7,
            },
            {
            "relation": "Grand Mother",
            'id': 8,
            },
            {
            "relation": "Uncle",
            'id': 9,
            },
            {
            "relation": "Aunty",
            'id': 10,
            },
            {
            "relation": "Niece",
            'id': 11,
            },
            {
            "relation": "Nephew",
            'id': 12,
            },
            {
            "relation": "Others",
            'id': 13,
            },
        ],
        "service_provider_type": [
            {
            "service_type": "Carpenter",
            'id': 1,
            },
            {
            "service_type": "Plumber",
            'id': 2,
            },
            {
            "service_type": "Wifi Provider",
            'id': 3,
            },
            {
            "service_type": "Cable",
            'id': 4,
            },
            {
            "service_type": "Security",
            'id': 5,
            },
            {
            "service_type": "Driver",
            'id': 6,
            },
            {
            "service_type": "Maid",
            'id': 7,
            },
            {
            "service_type": "Electrician",
            'id': 8,
            },
            {
            "service_type": "Construction or Civil Worker",
            'id': 9,
            },
            {
            "service_type": "Helper",
            'id': 10,
            },
            {
            "service_type": "Gardener",
            'id': 11,
            },
            {
            "service_type": "Cleaner",
            'id': 12,
            },
            {
            "service_type": "Waiter",
            'id': 13,
            },
            {
            "service_type": "AC Service",
            'id': 14,
            },
            {
            "service_type": "AC Provider",
            'id': 15,
            },
            {
            "service_type": "Shopkeeper",
            'id': 16,
            },
            {
            "service_type": "Watchman",
            'id': 17,
            },
            {
            "service_type": "Worker",
            'id': 18,
            },
            {
            "service_type": "Security Guard",
            'id': 19,
            },
            {
            "service_type": "Others",
            'id': 20,
            },
        ],
    },
    version =request.GET.get('version',0)
    platform =request.GET.get('platform',0)
    if version == "1.0" and platform == "ios" or version == "1.0.0" and platform == "android" :
        return Response({'data':util,"version/platform": True,'status':200,'massage':'Util types data fetched successfully',"response_error": False})


# LOCATION API
class LocationAPI(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = Location_Serializer
    http_method_names = ['get','post','put','delete']

    # permission_classes = [permissions.IsAuthenticated]

    # create location with post
    def create(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            # try:
                location = Location.objects.create(
                            location_name=request.data.get('location_name'),
                            # family_id = ,
                            city_id=request.data.get('city_id'),
                            state_id=request.data.get('state_id'),
                            latitude=request.data.get('latitude'),
                            longitude=request.data.get('longitude'),
                            address=request.data.get('address'),
                        )
                serializer = Location_Serializer(location)
                return Response({'data':serializer.data,
                "status_code": 201,
                "status_message": "Location data created successfully",
                "response_error": False})

        #     # except:
        # return Response({'data': {},'status':500,'massage':"something went wrong","response_error": True})
        

        #  serializer = Location_Serializer(data = request.data)
        # try:

        #     if not serializer.is_valid():
        #         print("error",serializer.errors)
        #         return Response({'data':{},"status_code": 500,'status_message':{
        #                 "expose": True,
        #                 "statusCode": 400,
        #                 "massage": "state must be a Number",
        #                 "type": "entity.parse.failed"},
        #                 "response_error": True
        #                 })

        #     new_loc = serializer.save()
        #     loc = Location.objects.get(location_id = new_loc.location_id) 
        #     return Response({'data' : serializer.data ,'status': 200 ,  'message' :  "Location data added successfully!", "response_error": False})
        # except Exception as e :
        #         print(e)
        #         return Response({'error': e})           
        
    # all location by get
    def list(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            try:
                loc = Location.objects.filter(family_id__user_id=user)
                # loc = Location.objects.all()
                serializer = Location_Serializer(loc,many = True)
                # print(serializer)
                return Response({'data':serializer.data,
                                "status_code": 200,
                                "status_message": "Location data fetched successfully",

                        "response_error": False})

            except:
                return Response({'data': {},'status':500,'massage':"something went wrong",
                "response_error": True})
        else:
            return Response({'data': {},'status':500,'massage':"something went wrong",
            "response_error": True})
            

    # update location with put
    def update(self,request,pk): 
        # token = request.META.get("HTTP_AUTHORIZATION")
        # user = decrypt_token(token)  
        # if user:
        location = Location.objects.get(pk = pk)
        serializer = Location_Serializer(instance=location,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data ,'status': 200 ,'massage' : 'data updated'})
        return Response({'data':{},'status': 500 , 'errors' : serializer.errors})
        # else:
        #     return Response({'data': {},'status':0,'massage':"something went wrong"})  

    # location by id get
    def retrieve(self, request, pk):
        # token = request.META.get("HTTP_AUTHORIZATION")
        # user = decrypt_token(token)  
        # if user:
        if pk is not None:
            location = Location.objects.get(pk=pk)
            serializer = Location_Serializer(location)
            return Response(serializer.data)

        location = Location.objects.all()
        serializer = Location_Serializer(location,many = True)
        return Response(serializer.data)
        # else:
        #     return Response({'data': {},'status':0,'massage':"something went wrong"})


    #location  delete
    def destroy(self,request,pk):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            location = Location.objects.get(pk = pk)
            location.delete()
            return Response({'status': 200,'massage': 'data deleted'})
        else:
            return Response({'data': {},'status':0,'massage':"something went wrong"})


    #    # token = request.META.get("HTTP_AUTHORIZATION")
    #     # user = decrypt_token(token)  
    #     # if user:
    #     try:
    #         location = Location.objects.get(pk = pk)
    #         location.is_active = False
    #         location.delete()
    #         return Response({'status':200,'msg':'data deleted'})
    #     except Exception as e:
    #         print(e)
    #         return Response({'status' : 500 , 'message' : 'invalid id'})
    #     # else:
    #     #     return Response({'data': {},'status':0,'massage':"something went wrong"})


#location from pincode
@api_view(["POST"])
def Pincode(request,id=None):
    pincode = request.data['pincode']
    try:
        loc = City.objects.filter(pincode=pincode)
        print(loc)
        serializer = City_Serializer(loc,many = True)
        # print(serializer)
        if serializer.data:
            return Response({'data': serializer.data,
                            "status_code": 200,
                            "status_message": "city data fetched successfully",
                            "response_error":False})
    except:
        return Response({'data': {},'status':500,'massage':"something went wrong",
        "response_error": True})
        
        
    # try:
    #     cities = City.objects.filter(state_id=id)
    #     print(cities)
    #     serializer = City_Serializer(cities,many = True)
    #     list = []
        
    #     # print(serializer)
    #     if serializer.data:
    #         return Response({'data': serializer.data,
    #                     "status_code": 200,
    #                     "status_message": "city data fetched successfully",
    #                     "response_error":False})
    #     else:
    #         return Response({'error':serializer.errors})
    # except Exception as e:
    #         print(e)
    #         return Response({'status' : 500 , 'message' : 'invalid id'})



   


# get locatoion by family id (LOCATION API)
@api_view(['GET'])
def findByFamilyIdlocation(request,pk):
    user = User.objects.get(user_id = pk)
    if pk is not None:
        location = Location.objects.get(user_id=pk)
        serializer = Location_Serializer(location)
        return Response(serializer.data)

    location = Location.objects.all()
    serializer = Location_Serializer(location,many = True)
    return Response(serializer.data)


#STATE API 
class  StateAPI(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = State_Serializer
    http_method_names = ['get']

    # get state 
    def list(self,request):
            state = State.objects.all()
            serializer = State_Serializer(state,many = True)
            print(serializer)
            return Response(serializer.data)



# get city by state id
@api_view(['get']) 
def findById(request,id=None):
    try:
        cities = City.objects.filter(state_id=id)
        # print(cities)
        serializer = City_Serializer(cities,many = True)
        list = []
        
        # print(serializer)
        if serializer.data:
            return Response({'data': serializer.data,
                        "status_code": 200,
                        "status_message": "city data fetched successfully",
                        "response_error":False})
        else:
            return Response({'error':serializer.errors})
    except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})


#CITY API 
class CityAPI(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = City_Serializer
    http_method_names = ['get']


    # get state 
    def list(self,request):
            city = City.objects.all()
            serializer = City_Serializer(city,many = True)
            print(serializer)
            return Response(serializer.data)

# COUNTRY API
class CountryAPI(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = Country_Serializer
    http_method_names = ['get']


    # get COUNTRY 
    def list(self,request):
            country = Country.objects.all()
            serializer = Country_Serializer(country,many = True)
            print(serializer)
            return Response(serializer.data)

 

# Service_provider API
class Service_ProviderAPI(viewsets.ModelViewSet):
    queryset = Service_provider.objects.all()
    serializer_class = Service_provider_Serializer
    http_method_names = ['get','post','put','delete']

    #add Service_provider by post
    def create(self,request):
        try:
            serializer = Service_provider_Serializer(data = request.data)
            if not serializer.is_valid():
                    print(serializer.errors)
                    return Response({'status' : 500 , 'errors' : serializer.errors ,'message' : 'something went wrong'})
                
                
            else:
                new_Service_provider = serializer.save()
                service_provider = Service_provider.objects.get(service_provider_id = new_Service_provider.service_provider_id) 
                return Response({'data' : serializer.data ,
                                "status_code": 200,
                                "status_message": "service_provider data fetched successfully",
                                "response_error": False})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

    
    # all Service_provider by get
    def list(self,request):
        try:
            service_provider = Service_provider.objects.all()
            serializer = Service_provider_Serializer(service_provider,many = True)
            print(serializer)
            return Response({'data': serializer.data,
                            "status_code": 200,
                            "status_message":"service_provider data fetched successfully",
                            "response_error": False
                            })

        except:
            return Response({'data': {},'status':500,'massage':"something went wrong"})  



    # update Service_provider with put
    def update(self,request,pk):
        try:
            service_provider = Service_provider.objects.get(pk = pk)
            serializer = Service_provider_Serializer(instance=service_provider,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data ,
                                "status_code": 200,
                                "status_message":"service_provider data updated successfully",
                                "response_error": False
                                })
            return Response({'data':{},'status': 500 , 'errors' : serializer.errors})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

    # Service_provider find  by id get
    def retrieve(self, request, pk):
        # try:
            if pk is not None:
                service_provider = Service_provider.objects.get(pk=pk)
                serializer = Service_provider_Serializer(service_provider)
                return Response({'data': serializer.data,   
                                "status_code": 200,
                                "status_message": "service_provider data fetched successfully",
                                "response_error": False
                                })

            service_provider = Service_provider.objects.all()
            serializer = Service_provider_Serializer(service_provider,many = True)
            return Response(serializer.data)
        # except Exception as e:
        #     print(e)
        #     return Response({'status' : 500 , 'message' : 'invalid id'})

    # Service_provider  delete
    def destroy(self,request,pk):
        try:
            service_provider = Service_provider.objects.get(pk = pk)
            service_provider.is_active = False
            service_provider.delete()
            return Response({'status':200,'msg':'data deleted'})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

# Appliance API
class ApplianceAPI(viewsets.ModelViewSet):
    queryset = Appliances.objects.all()
    serializer_class = Appliances_Serializer
    http_method_names = ['get','post','put','delete']

    #add Appliance by post
    def create(self,request):
        serializer = Appliances_Serializer(data = request.data)
        if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status' : 500 , 'errors' : serializer.errors ,'message' : 'something went wrong'})
            
            
        else:
            new_appliance = serializer.save()
            appliance = Appliances.objects.get(appliance_id = new_appliance.appliance_id) 
            return Response({'data' : serializer.data,
                            "status_code": 200,
                            "status_message": "appliance data fetched successfully",
                            "response_error": False})
        
    # all appliance by get
    def list(self,request):
        try:
            appliance = Appliances.objects.all()
            serializer = Appliances_Serializer(appliance,many = True)
            print(serializer)
            return Response({'data': serializer.data,
                            "status_code": 200,
                            "status_message":"Appliance data fetched successfully",
                            "response_error": False
                            })

        except:
            return Response({'data': {},'status':500,'massage':"something went wrong"})  
        
    

     # update appliance with put
    def update(self,request,pk):
        try:
            appliance = Appliances.objects.get(pk = pk)
            serializer = Appliances_Serializer(instance=appliance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data ,
                                "status_code": 200,
                                "status_message":"appliance data updated successfully",
                                "response_error": False
                                })
            return Response({'data':{},'status': 500 , 'errors' : serializer.errors})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

    # find by id  appliance with get
    def retrieve(self, request, pk):
        try:
            if pk is not None:
                appliance = Appliances.objects.get(pk=pk)
                serializer = Appliances_Serializer(appliance)
                return Response({'data': serializer.data,   
                                "status_code": 200,
                                "status_message": "appliance data fetched successfully",
                                "response_error": False
                                })
        
            appliance = Appliances.objects.all()
            serializer = Appliances_Serializer(appliance,many = True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

    # appliance  delete
    def destroy(self,request,pk):
        try:
            appliance = Appliances.objects.get(pk = pk)
            appliance.is_active = False
            appliance.delete()
            return Response({'status':200,'msg':'data deleted'})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'}) 

# task API
class TaskAPI(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = Task_serializers
    http_method_names = ['get','post','put','delete']

    #add task by post
    def create(self,request):
        serializer = Task_serializers(data=request.data)
        if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status' : 500 , 'errors' : serializer.errors ,'message' : 'something went wrong'})
            
            
        else:
            new_task = serializer.save()
            task = Task.objects.get(task_id = new_task.task_id) 
            return Response({'data' : serializer.data ,
                            "status_code": 200,
                            "status_message": "Todo data fetched successfully",
                            "response_error": False})

    
     # all Todo by get
    def list(self,request):
        try:
            task = Task.objects.all()
            serializer = Task_serializers(task,many = True)
            print(serializer)
            return Response({'data': serializer.data,
                            "status_code": 200,
                            "status_message":"task data fetched successfully",
                            "response_error": False
                            })

        except:
            return Response({'data': {},'status':500,'massage':"something went wrong"})         

    
    # update task with put
    def update(self,request,pk): 
        try:
            task = Task.objects.get(pk = pk)
            serializer = Task_serializers(instance=task,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data ,
                                "status_code": 200,
                                "status_message":"task data updated successfully",
                                "response_error": False
                                })
            return Response({'data':{},'status': 500 , 'errors' : serializer.errors})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})
    
    # task by id get
    def retrieve(self, request, pk):
        try:
            if pk is not None:
                task = Task.objects.get(pk=pk)
                serializer = Task_serializers(task)
                return Response({'data': serializer.data,   
                                "status_code": 200,
                                "status_message": "task data fetched successfully",
                                "response_error": False
                                })

            task = Task_serializers.objects.all()
            serializer = Task_serializers(task,many = True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

    
    # task  delete
    def destroy(self,request,pk):
        try:
            task = Task.objects.get(pk = pk)
            task.is_active = False
            task.delete()
            return Response({'status':200,'msg':'data deleted'})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})
 

@api_view(['GET'])
def fcm(request,id):
 
    if id is not None:
        # print('i m in if')
        # try:
            # print('i m in second try')
            device = FCMDevice.objects.get(user_id=id,type="android")
            
            # print('i m in device')
            print(device)
            status = device.send_message(Message
                                        (notification=Notification(title ="title" ,
                                            body="body of notification" ,
                                            image="url",)))
            # print(type(status))   
            # print('i m in status')
            print(status)
            return Response({'status' : str(status) , 'device' : str(device)})
        # except Exception as e:
        #     print(e)
        #     return Response({'status' : 500 , 'message' : 'invalid id'})

  # SUBSCRIPTION API
class Subscription_PlanAPI(viewsets.ModelViewSet):
    queryset =  Subscription_Plan.objects.all()
    serializer_class = Subscription_Plan_serializers
    http_method_names = ['get','post','put','delete']
        

    # all SUBSCRIPTION by get
    def list(self,request):
        try:
            subscription = Subscription_Plan.objects.all()
            serializer = Subscription_Plan_serializers(subscription,many = True)
            print(serializer)
            return Response({'data': serializer.data,
                            "status_code": 200,
                            "status_message":"Subscription_Plan data fetched successfully",
                            "response_error": False
                            })

        except:
            return Response({'data': {},'status':500,'massage':"something went wrong"})     

    # update SUBSCRIPTION by post
    def update(self,request,pk): 
        try:
            subscription = Subscription_Plan.objects.get(subscription_plan_id = pk)
            serializer = Subscription_Plan_serializers(instance=subscription,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data ,
                                "status_code": 200,
                                "status_message":"task data updated successfully",
                                "response_error": False
                                })
            return Response({'data':{},'status': 500 , 'errors' : serializer.errors})
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})
                
    
    # find by id  SUBSCRIPTION with get
    def retrieve(self, request, pk):
        try:
            if pk is not None:
                subscription = Subscription_Plan.objects.get(pk=pk)
                serializer = Subscription_Plan_serializers(subscription)
                return Response({'data': serializer.data,   
                                "status_code": 200,
                                "status_message": "appliance data fetched successfully",
                                "response_error": False
                                })
        
            subscription = Subscription_Plan.objects.all()
            serializer = Subscription_Plan_serializers(subscription,many = True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'status' : 500 , 'message' : 'invalid id'})

#PAYMENT API
class PaymentAPI(viewsets.ModelViewSet):
    queryset =  Payment.objects.all()
    serializer_class = Payment_serializers
    http_method_names = ['get','post','put','delete']

    # all PAYMENT by get  
    def create(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)
        if user :   
            serializer = Payment_serializers(data = request.data)

            if not serializer.is_valid():
                    print(serializer.errors)
                    return Response({'status' : 500 , 'errors' : serializer.errors ,'message' : 'something went wrong'})
            
                
            else:
                new_payment = serializer.save(user_id=user)
                payment = Payment.objects.get(payment_id = new_payment.payment_id) 
                return Response({'data' : serializer.data,
                                "status_code": 200,
                                "status_message": "payment data fetched successfully",
                                "response_error": False})



# Forgot Password API: 
    @action(methods=['post'], detail=False)
    def forgot_password(self,request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = Token.objects.create(user=user)
            data = {
                'token': token.key,
                'user_id': user.user_id
            }
            return Response({"data":data, "status":status.HTTP_200_OK})
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Change Password API: 
    @action(methods=['post'], detail=False)
    def change_password(self,request):
        token = request.META.get('HTTP_TOKEN')
        user_id = request.data.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if user:
            token_object = Token.objects.filter(key=token, user=user).first()
            if token_object:
                password = request.data.get('password')
                user.set_password(password)
                user.save()
                return Response({'message': 'Password updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Token mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)



# PAYMENT API
@api_view(['POST'])

def start_payment(request):
    # id = 1
    # sub = Subscription_Plan.objects.get(user_subscription_id=id)
    # request.data is coming from frontend
    amount = request.data['amount']
    # amount = sub.price
    # name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    print("client")

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
    print(payment)

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create( 
                                 order_amount=amount, 
                                 data = payment)

    # serializer = Payment_serializers(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "amount": amount
    }
    return Response(data)
    

# def handle_payment_success(self,request):
def create(self,request):
    # request.data is coming from frontend
    res = json.loads(request.data)

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    razorpay_order_id = "razorpay_order_id"
    razorpay_payment_id = "razorpay_payment_id"
    raz_signature = "raz_signature"

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    payment = Payment.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY')))
    client = razorpay.Client(auth=(config('PUBLIC_KEY'), config('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    payment.isPaid = True
    payment.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)




#Role API
class RoleAPI(viewsets.ModelViewSet):
    queryset =  Role.objects.all()
    serializer_class = Role_serializers
    http_method_names = ['get','post','put','delete']

    # add ROLE by post  
    def create(self,request): 
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)
        if user :   
            serializer = Role_serializers(data = request.data)

            if not serializer.is_valid():
                    print(serializer.errors)
                    return Response({'status' : 500, 'errors' : serializer.errors,'message' :'something went wrong'})

            else:
                new_role = serializer.save(user_id=user)
                role = Role.objects.get(role_id = new_role.role_id
                ) 
                return Response({'data' : serializer.data,
                "status_code": 200,
                "status_message": "role data fetched successfully",
                "response_error": False})
    
    # update ROLE by post
    def update(self,request,pk): 
        try:
            role = Role.objects.get(role_id = pk)
            serializer = Role_serializers(instance=role,data=request.data,partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,
                "status_code": 200,
                "status_message": "role data updated successfully",
                "response_error": False})
            return Response({'data':{},'status': 500, 'errors' : serializer.errors})

        except Exception as e:
            print(e)
            return Response({'status' : 500, 'errors' : 'invalid id'})

        
    
    # find by id  ROLE with get
    def retrieve(self, request, pk):
        try:
            if pk is not None:
                role = Role.objects.get(pk=pk)
                serializer = Role_serializers(role)
                return Response({'data': serializer.data,
                "status_code": 200,
                "status_message": "role data fetched successfully",
                "response_error": False})
        except Exception as e:
            print(e)
            return Response({'status' : 500, 'errors' : 'invalid id'})

        
    
    # delete ROLE with delete
    def destroy(self, request, pk):
        try:
            if pk is not None:
                role = Role.objects.get(role_id=pk)
                role.delete()
                return Response({'status' : 200,'message' : 'role deleted successfully'})

        except Exception as e:
            print(e)
            return Response({'status' : 500, 'errors' : 'invalid id'})


 # Forgot Password API: 
    @action(methods=['post'], detail=False)
    def forgot_password(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            mobile_number = request.data.get("mobile_number")
            if mobile_number=="":
                return Response({'status': 400,'msg' : 'mobile_number is required'},status=status.HTTP_400_BAD_REQUEST)
            # email = request.data.get("email")
            # if email=="":
                # return Response({'status': 400,'msg' : 'email is required'},status=status.HTTP_400_BAD_REQUEST)
            if mobile_number:
                try:
                    user = User.objects.get(mobile_number=mobile_number)
                    if user.mobile_number==mobile_number:
                        digits = [i for i in range(0, 10)]
                        random_str = ""
                        for i in range(6):
                            index = math.floor(random.random() * 10)
                            random_str += str(digits[index])
                    # opt = OTPs.objcts.create(OTPs :random_str)
                    # otp.save()
                    # user_model = User.objects.get(mobile_number=mobile_number)
                        otp = OTPs.objects.create(user=user,otp=random_str)
                        otp.save()
                        return Response({'status': 200,'otp' : random_str})
                except:
                    return Response({"status":401,"message":"User does not exist"},status = status.HTTP_401_UNAUTHORIZED)
                # if user.mobile_number == mobile_number:
                #     token = create_token(user=user)
                return Response({"data": mobile_number,'status' : 200,'msg':'login success','token':token},status=status.HTTP_200_OK)
            # else:
            #     try:
            #         user = User.objects.get(email=email)
            #         token = create_token(user=user)
            #         return Response({"data": email,'status' : 200,'msg':'login success'},status=status.HTTP_200_OK)
            #     except:
            #         return Response({"status":401,"message":"User does not exist"},status = status.HTTP_401_UNAUTHORIZED)
            # return Response({"data": email,'status' : 200,'msg':'login success'},status=status.HTTP_200_OK)
        else:
            return Response({})

# Reset Password API:
    @action(methods=['post'], detail=False)
    def reset_password(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = decrypt_token(token)  
        if user:
            mobile_number = request.data.get("mobile_number")
            email = request.data.get("email")
            password = request.data.get("password")
            new_password = request.data.get("new_password")
            if mobile_number:
                try:
                    user = User.objects.get(mobile_number=mobile_number)
                    token = create_token(user=user)
                    user.set_password(new_password)
                    user.save()
                    return Response({"data": mobile_number,'status' : 200,'msg':'reset password success','token':token},status=status.HTTP_200_OK)
                except:
                    return Response({'status':203,'massage':'invalid number'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                    # return Response({"data": email,'status' : 200,'msg':'reset password'})
            else:
                try:
                    user = User.objects.get(email=email)
                    token = create_token(user=user)
                    user.set_password(password)
                    user.save()
                    return Response({"data": email,'status' : 200,'msg':'reset password success'},status=status.HTTP_200_OK)
                except:
                    return Response({'status':203,'massage':'invalid email'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response({"status":401,"message":"User does not exist"},status = status.HTTP_401_UNAUTHORIZED)



    # # Reset Password API:
    # @action(methods=['post'], detail=False)
    # def reset_password(self,request):
    #     token = request.META.get("HTTP_AUTHORIZATION")
    #     user = decrypt_token(token)  
    #     if user:
    #         mobile_number = request.data.get("mobile_number")
    #         email = request.data.get("email")
    #         password = request.data.get("password")
    #         new_password = request.data.get("new_password")
    #         if mobile_number:
    #             try:
    #                 user = User.objects.get(mobile_number=mobile_number)
    #                 token = create_token(user=user)
    #                 user.set_password(new_password)
    #                 user.save()
    #                 return Response({"data": mobile_number,'status' : 200,'msg':'reset password success','token':token},status=status.HTTP_200_OK)
    #             except:
    #                 return Response({'status':203,'massage':'invalid number'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    #                 # return Response({"data": email,'status' : 200,'msg':'reset password'})
    #         else:
    #             try:
    #                 user = User.objects.get(email=email)
    #                 token = create_token(user=user)
    #                 user.set_password(password)
    #                 user.save()
    #                 return Response({"data": email,'status' : 200,'msg':'reset password success'},status=status.HTTP_200_OK)
    #             except:
    #                 return Response({'status':203,'massage':'invalid email'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    #     else:
    #         return Response({"status":401,"message":"User does not exist"},status = status.HTTP_401_UNAUTHORIZED)

    # @action(methods=['PUT'], detail=False)
    # def add_member(self,request,pk):
    #     token = request.META.get("HTTP_AUTHORIZATION")
    #     # print("token",token)

    #     user = decrypt_token(token) 
    #     # print("user",user)

    #     serializer = User_Serializer(data = request.data) 
    #     # print("serializer",serializer)

    #     if user:
    #         # if not serializer.is_valid():
    #         #     # print(serializer.errors)
    #         #     return Response({'status' : 204 ,'message' : serializer.errors},status=status.HTTP_204_NO_CONTENT)
    #         # else:
    #             mobile_number = request.data.get("mobile_number")
    #             relation = request.data.get("relation")
    #             if mobile_number == "":
    #                 return Response({"status":400,"Message":"mobile number required"},status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 new_member = User.objects.create(reference_id=user,mobile_number=mobile_number,relation=relation)
    #                 new_member.save()
    #             # family=Family.objects.get(user=pk,relation=relation)
    #             # print("family: ",family)
    #             if relation != "self":
    #                 member_permission = {
    #                             "appliance" :0,
    #                             "service" :0,
    #                             "location" :0,
    #                             "service_provider":0,
    #                             "task":0
    #                         }
    #                 permission = Permissions.objects.create(permission=member_permission,role_id=2,user_id=new_member,family_id=family)
    #             else:
    #                 token = create_token(user=new_member)  
    #                 return Response({'data' : serializer.data ,
    #                     "status_code": 200,
    #                     "response_error": False,
    #                     'status_message': "User data added successfully!",
    #                     'token':token},status=status.HTTP_201_CREATED) 
    #     else:
    #         return Response({"status":401,"message":"User does not exist"},status = status.HTTP_401_UNAUTHORIZED)



# def mobile_validater(mobile_number):
#     # validator_str = "+1234567890".split()
#     validator_str = "+1234567890"
#     list1 = [x for x in validator_str]
#     print(list1)

#     for char in mobile_number:
#         if char not in list1:
#             return True
#         return False