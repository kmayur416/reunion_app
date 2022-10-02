from django.shortcuts import render
from rest_framework.views import APIView
from app.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
class UserCreate(generics.CreateAPIView):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = (AllowAny, )

class Profileview(APIView):

    def get(self,request,pk=None):
        if pk:
            profiles = Profile.objects.filter(book_id=pk).first()
            if profiles:
                serializer = ProfileSerializer(Profile)
                return Response({"status":200, "data" :serializer.data})
            else:
                return Response({'msg':'Data Updated'})

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({"status":200, "data" :serializer.data})
        

    def post(self,request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)