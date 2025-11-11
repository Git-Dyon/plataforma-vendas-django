from rest_framework import serializers
from .models import Project, MLModel
from django.contrib.auth.models import User

# Serializer para o modelo de Usuário (para vermos o dono do projeto)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# Serializer para o modelo de Projeto
class ProjectSerializer(serializers.ModelSerializer):
    # 1. Usamos o UserSerializer para mostrar os detalhes do dono, e não só o ID
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        # 2. Lista os campos que queremos "traduzir" para JSON
        fields = [
            'id',
            'name',
            'description',
            'status',
            'owner',
            'created_at',
            'data_file', # O campo de upload
        ]
        # 3. 'owner' e 'status' não podem ser editados diretamente pela API
        read_only_fields = ['owner', 'status']


# Serializer para o modelo de ML
class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ['id', 'project', 'metrics', 'model_file', 'created_at']