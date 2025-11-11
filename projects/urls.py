from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

# 1. Cria um Roteador padrão do DRF
router = DefaultRouter()

# 2. Registra nossa ViewSet (ProjectViewSet) com o roteador
#    Isso diz ao roteador para criar URLs para 'projects'
#    baseado na view 'ProjectViewSet'
router.register(r'projects', ProjectViewSet, basename='project')

# 3. As URLs da API agora são geradas automaticamente pelo roteador.
urlpatterns = [
    # Inclui todas as URLs geradas pelo roteador
    path('', include(router.urls)),
]