import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DB_NAME = "dados_cripto.db"
OUTPUT_DIR = "infograficos"

def carregar_dados():
    """Lê os dados do banco SQLite e garante a tipagem correta."""
    conn = sqlite3.connect(DB_NAME)
    
    query = """
    SELECT * FROM historico_criptomoedas 
    WHERE data_carga = (SELECT MAX(data_carga) FROM historico_criptomoedas)
    """
    df = pd.read_sql(query, conn)
    conn.close()

    cols_numericas = ['capitalizacao_mercado', 'volume_total', 'preco_atual_usd']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(subset=cols_numericas, inplace=True)
    
    return df

def configurar_estilo():
    """Define o estilo visual dos gráficos."""
    sns.set_theme(style="darkgrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10

def gerar_top_10_market_cap(df):
    """Gráfico de Barras: Top 10 por Capitalização de Mercado"""
    top_10 = df.nlargest(10, 'capitalizacao_mercado')
    
    plt.figure()
    ax = sns.barplot(x='capitalizacao_mercado', y='name', data=top_10, hue='name', palette='viridis', legend=False)
    plt.title('Top 10 Criptomoedas por Capitalização de Mercado (Market Cap)')
    plt.xlabel('Market Cap (USD)')
    plt.ylabel('')
    plt.tight_layout()
    salvar_grafico("01_top_10_market_cap.png")

def gerar_top_10_volume(df):
    """Gráfico de Barras: Top 10 por Volume (Liquidez)"""
    top_10_vol = df.nlargest(10, 'volume_total')
    
    plt.figure()
    sns.barplot(x='volume_total', y='symbol', data=top_10_vol, hue='symbol', palette='magma', legend=False)
    plt.title('Top 10 Criptomoedas por Volume (24h)')
    plt.xlabel('Volume Total (USD)')
    plt.ylabel('Símbolo')
    plt.tight_layout()
    salvar_grafico("02_top_10_volume.png")

def gerar_dispersao_preco_volume(df):
    """Scatter Plot: Relação entre Preço e Volume (excluindo Bitcoin para melhor escala)"""
    df_filtered = df[df['symbol'] != 'btc'].copy()
    
    plt.figure()
    sns.scatterplot(
        data=df_filtered, 
        x='volume_total', 
        y='preco_atual_usd', 
        hue='symbol', 
        size='capitalizacao_mercado',
        sizes=(20, 200), 
        legend=False
    )
    plt.title('Relação Preço vs. Volume (Altcoins)')
    plt.xlabel('Volume Total (USD)')
    plt.ylabel('Preço Atual (USD)')
    
    # Escala logarítmica
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    salvar_grafico("03_dispersao_altcoins.png")

def salvar_grafico(nome_arquivo):
    """Salva o gráfico na pasta de saída."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, nome_arquivo)
    plt.savefig(path)
    print(f"Gráfico salvo: {path}")
    plt.close()

if __name__ == "__main__":
    print("--- INICIANDO GERAÇÃO DE INFOGRÁFICOS ---")
    
    try:
        dados = carregar_dados()
        if not dados.empty:
            print(f"Dados carregados e tratados: {len(dados)} registros.")
            configurar_estilo()
            
            gerar_top_10_market_cap(dados)
            gerar_top_10_volume(dados)
            gerar_dispersao_preco_volume(dados)
            
            print("--- PROCESSO CONCLUÍDO ---")
            print(f"Verifique a pasta '{OUTPUT_DIR}' no seu projeto.")
        else:
            print("O banco de dados está vazio ou os dados não puderam ser convertidos.")
            
    except Exception as e:
        print(f"Erro crítico: {e}")
        print("Dica: Verifique se rodou o 'etl_crypto.py' antes deste script.")