import pandas as pd
import numpy as np
# Nesse caso o sistema ira randomizar dados de vendas de suplementos alimentares, porém é possivel psoteriormente criar um sistema para inclusão manual de dados
print("Iniciando criação do simulacro de dados de suplementos...")

# Lista dos seus produtos
produtos = ['Whey Protein', 'Creatina', 'Glutamina', 'BCAA', 'Multivitamínico']

# Criar 1000 registros de vendas fictícias
num_registros = 1000

dados = {
    'produto': np.random.choice(produtos, num_registros),
    'preco_venda': np.random.randint(50, 350, num_registros), # Preço de R$50 a R$350
    'promocao_ativa': np.random.choice([0, 1], num_registros), # 0 = Não, 1 = Sim
    'dia_da_semana': np.random.choice(['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom'], num_registros)
}

df = pd.DataFrame(dados)

# --- AQUI ESTÁ A "LÓGICA" QUE O ROBÔ VAI APRENDER ---
# Vamos definir nossa coluna 'sales' (vendas) = unidades vendidas.
# Vamos criar uma "lógica de negócios" para o robô descobrir.

# 1. Preço base de vendas (quanto mais caro, menos vende)
vendas_base = 150 - (df['preco_venda'] / 5)

# 2. Promoção aumenta as vendas
vendas_promo = df['promocao_ativa'] * 100 # Promoção dá um bônus de 100 unidades

# 3. Alguns produtos vendem mais que outros
def bonus_produto(produto):
    if produto == 'Whey Protein':
        return 50
    if produto == 'Creatina':
        return 70
    else:
        return 10
vendas_produto_bonus = df['produto'].apply(bonus_produto)

# 4. Adicionar um pouco de "ruído" (sorte/azar)
ruido = np.random.randint(-10, 10, num_registros)

# 5. Calcular o total de vendas (NOSSA COLUNA "ALVO")
# É CRUCIAL que o nome seja 'sales', pois nosso robô foi programado para prever 'sales'
df['sales'] = vendas_base + vendas_promo + vendas_produto_bonus + ruido

# Garantir que não tenhamos vendas negativas (não faz sentido)
df['sales'] = df['sales'].clip(lower=0).astype(int)

# --- FIM DA LÓGICA ---

# Salvar no formato que o robô entende
nome_arquivo = 'suplementos.parquet'
df.to_parquet(nome_arquivo)

print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
print("Ele contém 1000 registros de vendas de suplementos.")
print("Agora você pode usar este arquivo no seu sistema.")