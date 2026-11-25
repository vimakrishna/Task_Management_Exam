from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from task_exam.serializers import RegisterSerializer, TaskSerializer
from task_exam.models import TaskDb
from rest_framework import authentication, permissions
from task_exam.permissions import OwnerOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        form_data = request.data
        serializer_instance = RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User was created successfully..!"},status=201)
        else:
            return Response({"message":"Invalid data provided...!"}, status=400)

class LoginView(ObtainAuthToken):

    

    def post(self, request):
        serializer_instance = self.serializer_class(data=request.data)
        if serializer_instance.is_valid():
            user = serializer_instance.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "Message": "Login successful..!",
                "Token": token.key}, status=200)
        return Response(serializer_instance.errors, status=400)
    
class TaskListCreateView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = TaskDb.objects.filter(created_by=request.user)
        serializer_instance = TaskSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=200)

    def post(self, request):

        form_data = request.data
        serializer_instance = TaskSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "Message": "Task created successfully..!",
                "Task Details": serializer_instance.data}, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)

class TaskRetrieveUpdateDeleteView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, OwnerOnly]

    def get(self, request, pk):

        task_object = get_object_or_404(TaskDb, id=pk)
        self.check_object_permissions(request, task_object)
        serializer_instance = TaskSerializer(task_object)
        return Response(data=serializer_instance.data, status=200)

    def put(self, request, pk):

        task_object = get_object_or_404(TaskDb, id=pk)
        self.check_object_permissions(request, task_object)
        form_data = request.data
        serializer_instance = TaskSerializer(data=form_data, instance=task_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message": "Task details updated successfully..!",
                "Updated Details": serializer_instance.data}, status=200)
        else:
            return Response(data=serializer_instance.errors, status=400)

    def delete(self, request, pk):

        task_object = get_object_or_404(TaskDb, id=pk)
        self.check_object_permissions(request, task_object)
        task_object.delete()
        return Response(data={
            "Message": "Task deleted successfully..!"}, status=200)
