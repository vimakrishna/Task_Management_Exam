from django.contrib.auth.models import User
from rest_framework import serializers
from task_exam.models import TaskDb

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDb
        fields = "__all__"

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at"
        ]