from django.db import models
from django.contrib.auth.models import User # 1. Importa o modelo de Usuário padrão

# Modelo para o "Projeto de Previsão"
class Project(models.Model):
    # Status possíveis para o projeto
    STATUS_CHOICES = [
        ('pending', 'Pendente'),   # O usuário criou, mas ainda não enviou dados
        ('training', 'Treinando'),  # O sistema está processando o modelo
        ('ready', 'Pronto'),        # O modelo está treinado e pronto para prever
        ('error', 'Erro'),          # Algo deu errado no treinamento
    ]

    # 2. Relacionamento: Cada projeto pertence a um usuário (Dono)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    # 3. Campos de informação
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # 4. Campo para o arquivo de dados (o .parquet que o usuário vai enviar)
    #    'uploads/parquet/': é a subpasta onde os arquivos serão salvos
    data_file = models.FileField(upload_to='uploads/parquet/', blank=True, null=True)

    # 5. Datas automáticas
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


# Modelo para o "Modelo de Machine Learning Treinado"
class MLModel(models.Model):
    # 6. Relacionamento: Cada modelo treinado pertence a um Projeto
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='model')
    
    # 7. Campo para o arquivo do modelo (o .pkl que o PyCaret vai gerar)
    model_file = models.FileField(upload_to='uploads/models/')
    
    # 8. Campo para guardar as métricas (ex: R², RMSE, etc.)
    #    Usamos JSONField que é perfeito para guardar dados estruturados
    metrics = models.JSONField(blank=True, null=True)
    
    # 9. Datas automáticas
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Modelo do projeto: {self.project.name}"