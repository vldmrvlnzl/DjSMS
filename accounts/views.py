from django.shortcuts import render
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': user}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)