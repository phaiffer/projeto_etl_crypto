import requests
import pandas as pd
import sqlite3
import datetime
import os

URL_API = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 100,
    'page': 1,
    'sparkline': 'false'
}
DB_NAME = "dados_cripto.db"
TABLE_NAME = "historico_criptomoedas"

def extract_data():
    """
    Etapa de Extração:
    Conecta à API e retorna os dados em formato JSON.
    """
    print(f"[{datetime.datetime.now()}] Iniciando extração de dados...")
    try:
        response = requests.get(URL_API, params=PARAMS)
        response.raise_for_status()
        data = response.json()
        print(f"[{datetime.datetime.now()}] Dados extraídos com sucesso: {len(data)} registros.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro na extração: {e}")
        return None

def transform_data(data_json):
    """
    Etapa de Transformação:
    Converte JSON para DataFrame, seleciona colunas úteis e adiciona timestamp.
    """
    print(f"[{datetime.datetime.now()}] Iniciando transformação...")
    
    if not data_json:
        return None

    df = pd.DataFrame(data_json)

    colunas_desejadas = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'last_updated']
    df_transformado = df[colunas_desejadas].copy()

    df_transformado['data_carga'] = datetime.datetime.now()

    df_transformado.rename(columns={
        'current_price': 'preco_atual_usd',
        'market_cap': 'capitalizacao_mercado',
        'total_volume': 'volume_total',
        'last_updated': 'ultima_atualizacao_api'
    }, inplace=True)

    df_transformado['ultima_atualizacao_api'] = pd.to_datetime(df_transformado['ultima_atualizacao_api'])

    print(f"[{datetime.datetime.now()}] Transformação concluída.")
    return df_transformado

def load_data(df):
    """
    Etapa de Carga:
    Salva os dados transformados num banco de dados SQLite local.
    """
    print(f"[{datetime.datetime.now()}] Iniciando carga no banco de dados...")
    
    if df is None or df.empty:
        print("Nenhum dado para carregar.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        
        df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        
        conn.close()
        print(f"[{datetime.datetime.now()}] Carga concluída com sucesso no banco '{DB_NAME}'.")
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

if __name__ == "__main__":
    print("--- INICIANDO PIPELINE ETL ---")
    
    dados_brutos = extract_data()
    
    dados_tratados = transform_data(dados_brutos)
    
    load_data(dados_tratados)
    
    print("--- PIPELINE FINALIZADO ---")