import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Project

# O "marcador" que diz ao Pytest: "Para estes testes, você vai precisar 
# de acesso ao banco de dados (que será um banco de teste temporário)"
@pytest.mark.django_db
class TestProjectAPI:
    
    def test_unauthenticated_user_cannot_see_projects(self):
        """
        TESTE 1: Garante que um usuário DESLOGADO não pode ver a lista de projetos.
        """
        # 1. Cria um "navegador" falso
        client = APIClient()
        
        # 2. Faz uma requisição GET para a nossa API
        response = client.get('/api/v1/projects/')
        
        # 3. Verifica o resultado
        #    Esperamos um erro 401 (Não Autorizado) ou 403 (Proibido).
        #    O DRF, por padrão, retorna 401.
        assert response.status_code == 403

    def test_authenticated_user_can_see_their_projects(self):
        """
        TESTE 2: Garante que um usuário LOGADO pode ver os SEUS projetos.
        """
        client = APIClient()
        
        # 1. Cria os dados de teste no banco
        user = User.objects.create_user(username='testuser', password='password123')
        Project.objects.create(owner=user, name='Meu Projeto de Teste')
        
        # 2. "Loga" o usuário no nosso "navegador" falso
        client.force_authenticate(user=user)
        
        # 3. Faz a requisição (agora como usuário logado)
        response = client.get('/api/v1/projects/')
        
        # 4. Verifica o resultado
        assert response.status_code == 200     # Deve ser um sucesso
        assert len(response.data) == 1         # Deve retornar 1 projeto
        assert response.data[0]['name'] == 'Meu Projeto de Teste'

    def test_user_cannot_see_other_users_projects(self):
        """
        TESTE 3: Garante que um usuário LOGADO NÃO vê os projetos de OUTROS usuários.
        Este é o teste de segurança mais importante da nossa lógica.
        """
        client = APIClient()
        
        # 1. Cria DOIS usuários e UM projeto
        user1 = User.objects.create_user(username='user1', password='p')
        user2 = User.objects.create_user(username='user2', password='p')
        
        # 2. O projeto pertence ao user2
        Project.objects.create(owner=user2, name='Projeto do Outro Cara')
        
        # 3. Loga como user1
        client.force_authenticate(user=user1)
        
        # 4. Pede a lista de projetos
        response = client.get('/api/v1/projects/')
        
        # 5. Verifica o resultado
        assert response.status_code == 200  # A página carrega...
        assert len(response.data) == 0      # ...mas a lista de projetos vem VAZIA.