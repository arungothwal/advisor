from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import AdvisorSerializer, UserSerializer, BookingSerializer, GetAdvisorsSerializer
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated,IsAdminUser


'''Advisor creation api'''


class CreateAdvisor(APIView):
    def post(self,request):
        try:
            data =request.data
            advisor_name = request.data.get('name')
            advisor_pic = request.data.get('pic')
            if advisor_name is None or advisor_pic is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

            serializer = AdvisorSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


"""User Registration Api"""


class CreateUser(APIView):
    def post(self, request):
        try:
            params = request.data
            user_name = request.data.get('name')
            if user_name is None :
                return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
            user = UserSerializer(data=params)
            if user.is_valid(raise_exception=True):
                userObj = user.save()
                userObj.set_password(params['password'])
                userObj.is_active = True
                userObj.save()
                return Response({'message':"Register Succesfully", "userid": userObj.id}, status=status.HTTP_200_OK,content_type='application/json')
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


"""user login"""


class Login(APIView):

    def post(self, request):
        try:
            params = request.data
            user_exist = User.objects.filter(Q(email=params['email']) and Q(password =params['password']))

            user = authenticate(email=params['email'], password=params['password'])
            if user:
                user_data = UserSerializer(user)
                id = user_data.data['id']
                login(request, user)
                return Response(
                    {"message": "Logged in successfully.", "user_id": id, "token": user.create_jwt()},
                    status=status.HTTP_200_OK)
            if not user_exist:
                return Response({"message": "Please enter correct credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


"""Advisor List"""


class Advisorlist(APIView):
    def get(self,request,**kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
            if not user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            advisor_data = Advisor.objects.all()
            serializer = AdvisorSerializer(advisor_data, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK, content_type='application/json')
        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')


'''Book-call with advisor'''

class BookCall(APIView):

    def post(self, request, **kwargs):
        try:
            params = request.data
            user = User.objects.get(id=kwargs['user_id'])
            if not user:
                return Response({"message": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
            advisor = Advisor.objects.get(id=kwargs['advisor_id'])
            if not advisor:
                return Response({"message": "advisor not found"}, status=status.HTTP_400_BAD_REQUEST)
            data = {'user_id': user.id, 'advisor_id': advisor.id, 'booking_time': params['booking_time']}
            booking = BookingSerializer(data=data)
            if booking.is_valid(raise_exception=True):
                booking.save()
                return Response({"message": 'successfully booked call'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Error", "data": None}, status=status.HTTP_400_BAD_REQUEST)


class BookingDetails(APIView):
    def get(self,request,**kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
            if not user:
                return Response( status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            data = Advisor.objects.all()
            serializer = GetAdvisorsSerializer(data,many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK,content_type='application/json')
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
