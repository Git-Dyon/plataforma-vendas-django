from rest_framework import viewsets, permissions, status # 1. Importe o 'status'
from rest_framework.decorators import action             # 2. Importe o 'action'
from rest_framework.response import Response             # 3. Importe o 'Response'
from .models import Project
from .serializers import ProjectSerializer
from . import services                                 # 4. Importe nossos serviços

# Esta é a "View" para o modelo de Projeto
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que projetos sejam vistos ou editados.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Esta função garante que um usuário só possa ver os *seus próprios* projetos.
        """
        user_projects = Project.objects.filter(owner=self.request.user)
        return user_projects

    def perform_create(self, serializer):
        """
        Esta função é chamada quando um novo projeto é CRIADO (via POST).
        """
        serializer.save(owner=self.request.user)
        
    # --- NOSSA NOVA AÇÃO DE TREINAMENTO ---
    
    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        """
        Ação personalizada para disparar o treinamento de ML para um projeto.
        Responde a: POST /api/v1/projects/{id}/train/
        """
        try:
            # 1. Pega o objeto do projeto (o DRF nos dá o 'pk', ou primary key)
            project = self.get_object()
            
            print(f"Recebida requisição de treino para o projeto: {project.name}")

            # 2. Chama nosso serviço de "trabalho pesado"
            #    (Estamos fazendo isso de forma simples por enquanto)
            success, message = services.train_model_for_project(project.id)
            
            # 3. Responde à API
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
    # --- FIM DA NOVA AÇÃO ---