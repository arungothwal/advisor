from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import Advisor_Serializer,UserSerializer
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

            serializer = Advisor_Serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "successfully created"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')