import pandas as pd
from pycaret.regression import setup as pycaret_setup
from pycaret.regression import compare_models, pull, save_model
from django.core.files.base import ContentFile
from .models import Project, MLModel
import os # Importe o 'os' para manipulação de caminhos

def train_model_for_project(project_id: int):
    """
    Serviço principal para treinar um modelo de ML (agora de verdade).
    """
    
    print(f"--- [Iniciando Treinamento Real] ---", flush=True)
    
    try:
        # 1. Busca o projeto
        project = Project.objects.get(id=project_id)
        print(f"Projeto encontrado: {project.name}", flush=True)
        
        # 2. Valida o arquivo
        if not project.data_file:
            print(f"[ERRO] Projeto {project.name} não tem arquivo de dados.", flush=True)
            project.status = 'error'
            project.save()
            return False, "Arquivo de dados não encontrado."

        # 3. Atualiza o status
        print(f"Atualizando status para 'Treinando'...", flush=True)
        project.status = 'training'
        project.save()
        
        # --- Mágica do ML com PyCaret e Pandas ---
        
        # 4. Lê o arquivo .parquet com pandas
        file_path = project.data_file.path  # Pega o caminho do arquivo no disco
        print(f"Lendo o arquivo .parquet de: {file_path}", flush=True)
        df = pd.read_parquet(file_path)
        print(f"Arquivo lido com sucesso. {len(df)} linhas encontradas.", flush=True)
        
        # 5. Configura o PyCaret
        #    Vamos assumir que a coluna alvo é sempre 'sales'
        print("Configurando o PyCaret (setup)...", flush=True)
        pycaret_setup(data=df, target='sales', session_id=123)
        
        # 6. Compara os modelos e encontra o melhor
        print("Comparando modelos para encontrar o melhor...", flush=True)
        best_model = compare_models()
        print(f"Melhor modelo encontrado: {best_model}", flush=True)
        
        # 7. Puxa as métricas do melhor modelo
        metrics_df = pull()
        metrics_json = metrics_df.to_json(orient='records')
        print("Métricas extraídas.", flush=True)

        # 8. Salva o modelo treinado (pipeline + modelo) em um arquivo temporário
        model_filename = f'project_{project.id}_model'
        # O PyCaret salva como .pkl, então não precisamos adicionar a extensão
        save_model(best_model, model_filename) 
        
        # O PyCaret salva o arquivo no diretório de trabalho com a extensão .pkl
        saved_model_path = f"{model_filename}.pkl"
        print(f"Modelo salvo temporariamente em: {saved_model_path}", flush=True)

        # 9. Cria ou atualiza o MLModel no banco de dados
        #    Deleta qualquer modelo antigo que este projeto possa ter
        MLModel.objects.filter(project=project).delete()
        
        # 10. Lê o arquivo .pkl que acabamos de salvar
        with open(saved_model_path, 'rb') as f_model:
            # -------- AQUI ESTÁ A CORREÇÃO (f_model.read()) --------
            model_content = ContentFile(f_model.read())

            # 11. Cria o novo objeto MLModel
            ml_model = MLModel.objects.create(
                project=project,
                metrics=metrics_json, # Salva as métricas como JSON
            )
            
            # 12. Salva o arquivo .pkl no FileField do Django
            ml_model.model_file.save(f"{model_filename}.pkl", model_content, save=True)
            
            print(f"Modelo salvo no banco de dados com ID: {ml_model.id}", flush=True)

        # 13. Limpa o arquivo temporário
        os.remove(saved_model_path)
        print(f"Arquivo temporário {saved_model_path} removido.", flush=True)

        # --- Fim da mágica ---
        
        # 14. Atualiza o status final
        print("Treinamento concluído. Atualizando status para 'Pronto'.", flush=True)
        project.status = 'ready'
        project.save()
        
        print(f"--- [Treinamento Real Finalizado com Sucesso] ---", flush=True)
        return True, "Modelo treinado com sucesso."
        
    except Exception as e:
        # Se algo der errado (ex: erro no pandas ou pycaret)
        print(f"[ERRO GERAL] Falha no treinamento: {e}", flush=True)
        
        # Tenta marcar o projeto com erro
        try:
            project = Project.objects.get(id=project_id)
            project.status = 'error'
            project.save()
        except Project.DoesNotExist:
            pass # Se o projeto nem existia, não há o que marcar
            
        return False, str(e)