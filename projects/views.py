from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, MLModel
from .serializers import (
    ProjectSerializer,
    PredictionInputSerializer,
    PredictionOutputSerializer
)
from . import services
import pandas as pd
import os
from pycaret.regression import load_model, predict_model

# Esta é a "View" para o modelo de Projeto
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que projetos sejam vistos ou editados.
    """
    queryset = Project.objects.all()
    # serializer_class = ProjectSerializer # <-- VAMOS REMOVER ESTA LINHA
    permission_classes = [permissions.IsAuthenticated]

    # --- NOVA FUNÇÃO "GPS" DE SERIALIZER ---
    def get_serializer_class(self):
        """
        Diz ao DRF qual "tradutor" (serializer) usar
        dependendo da ação que está sendo chamada.
        """
        # Se a ação for 'predict', use o formulário de INPUT da previsão
        if self.action == 'predict':
            return PredictionInputSerializer
        
        # Para todas as outras ações ('list', 'create', 'train', etc.)
        # use o serializer padrão do Projeto.
        return ProjectSerializer
    # --- FIM DA NOVA FUNÇÃO ---

    def get_queryset(self):
        user_projects = Project.objects.filter(owner=self.request.user)
        return user_projects

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        try:
            project = self.get_object()
            print(f"Recebida requisição de treino para o projeto: {project.name}", flush=True)
            success, message = services.train_model_for_project(project.id)
            if success:
                return Response(
                    {'status': 'Treinamento iniciado', 'message': message},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Falha ao iniciar treinamento', 'message': message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': 'Erro interno do servidor', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        """
        Ação personalizada para fazer uma previsão usando o modelo treinado.
        Responde a: POST /api/v1/projects/{id}/predict/
        """
        try:
            project = self.get_object()

            if project.status != 'ready':
                return Response(
                    {'error': 'O modelo deste projeto não está pronto para prever.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Usamos o 'get_serializer' que agora aponta para o serializer correto
            input_serializer = self.get_serializer(data=request.data)
            if not input_serializer.is_valid():
                return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            model_path_com_extensao = project.model.model_file.path
            model_path_sem_extensao = os.path.splitext(model_path_com_extensao)[0]
            modelo_carregado = load_model(model_path_sem_extensao)
            
            input_data = pd.DataFrame([input_serializer.validated_data])

            previsao = predict_model(modelo_carregado, data=input_data)
            
            resultado_final = previsao.iloc[0]

            output_serializer = PredictionOutputSerializer(resultado_final)

            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except MLModel.DoesNotExist:
            return Response(
                {'error': 'Modelo de ML não encontrado para este projeto.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"[ERRO PREDICT] {e}", flush=True)
            return Response(
                {'error': 'Erro interno do servidor durante a previsão.', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )