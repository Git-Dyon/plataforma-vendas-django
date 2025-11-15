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

#incluindo serializer do modelo MLModel para visualização humana dos modelos treinados
# Serializer para o modelo de ML
class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ['id', 'project', 'metrics', 'model_file', 'created_at']
# --- Adicione o código abaixo no final do arquivo ---

# 1. O "Tradutor" da PERGUNTA do cliente
#    Define como deve ser a pergunta que o cliente vai nos enviar
class PredictionInputSerializer(serializers.Serializer):
    """
    Serializador para validar os dados de entrada para uma nova previsão.
    Ele garante que o cliente enviou os dados no formato correto.
    """
    # Usamos os mesmos nomes de colunas do arquivo .parquet
    produto = serializers.ChoiceField(choices=['Whey Protein', 'Creatina', 'Glutamina', 'BCAA', 'Multivitamínico'])
    preco_venda = serializers.IntegerField(min_value=0)
    promocao_ativa = serializers.ChoiceField(choices=[0, 1]) # 0 = Não, 1 = Sim
    dia_da_semana = serializers.ChoiceField(choices=['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom'])
    
    # Este Serializer não tem um "Meta" e um "model" porque ele não
    # está ligado a uma tabela do banco de dados. Ele é só um "validador"
    # de dados de entrada.


# 2. O "Tradutor" da RESPOSTA do robô
#    Define como vamos formatar a resposta final para o cliente arredondando a previsão
class PredictionOutputSerializer(serializers.Serializer):

    previsao_de_vendas = serializers.SerializerMethodField()

    def get_previsao_de_vendas(self, obj):
        
        return round(obj['prediction_label'])