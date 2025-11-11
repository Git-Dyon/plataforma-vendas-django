from django.contrib import admin
from .models import Project, MLModel # 1. Importa nossos novos modelos

# 2. Registra o modelo Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista de projetos
    list_display = ('name', 'owner', 'status', 'created_at')
    # Campos que são links clicáveis
    list_display_links = ('name', 'owner')
    # Filtros que aparecerão na barra lateral
    list_filter = ('status', 'owner__username')
    # Campos de busca
    search_fields = ('name', 'description')


# 3. Registra o modelo MLModel
@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista de modelos
    list_display = ('project', 'created_at')
    # Campos de busca
    search_fields = ('project__name',)