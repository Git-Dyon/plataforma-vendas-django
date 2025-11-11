import pandas as pd
import numpy as np
# Simular criação de um dataset Parquet para testes
# Criar 500 linhas de dados fictícios
data = {
    'data': pd.date_range(start='2023-01-01', periods=500),
    'investimento_marketing': np.random.uniform(50, 500, 500),
    'dia_da_semana': np.random.choice(['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom'], 500),
    'promocao_ativa': np.random.choice([0, 1], 500),
    # Nossa coluna alvo "sales" (vendas)
    'sales': np.random.uniform(1000, 5000, 500) + np.random.normal(0, 300, 500)
}

df = pd.DataFrame(data)

# Adicionar um pouco de "lógica" para o ML encontrar
df['sales'] = df['sales'] + (df['investimento_marketing'] * 1.5) + (df['promocao_ativa'] * 200)

# Salvar como Parquet
filename = 'sample_sales.parquet'
df.to_parquet(filename)

print(f"Arquivo '{filename}' criado com sucesso com {len(df)} linhas.")