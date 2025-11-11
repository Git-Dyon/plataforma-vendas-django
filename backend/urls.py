from django.contrib import admin 
from django.urls import path, include # a função dessa biblioteca é incluir outras urls
from django.conf import settings             # esse importa a biblioteca settings
from django.conf.urls.static import static   # esse importa a biblioteca static

urlpatterns = [
    path('admin/', admin.site.urls), # essa linha é a url do admin que ja vem por padrao no django
    path('api/v1/', include('projects.urls')), # aqui estamos incluindo as urls do app projects
]

# Adiciona as URLs de mídia apenas em modo de desenvolvimento
if settings.DEBUG: #essa linha serve para verificar se estamos em modo de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # esses comandos são para servir arquivos de mídia durante o desenvolvimento
    