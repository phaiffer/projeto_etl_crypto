
---

# 🚀 Pipeline de Engenharia de Dados — Top 100 Criptomoedas

Este projeto consiste em um pipeline de dados **ETL (Extract, Transform, Load)** construído em **Python**.  
O objetivo é **extrair dados de mercado** das principais criptomoedas e gerar **infográficos** com os resultados.

---

## ⚙️ Etapas do Pipeline

1️⃣ **Executar o Pipeline ETL (Extrair dados)**  
```bash
python etl_crypto.py
```

🔹 Isso criará o arquivo `dados_crypto.db`.

2️⃣ **Gerar os Infográficos**  
```bash
python visualizacao.py
```

🔹 Isso criará a pasta `infograficos/` com as imagens geradas.

---

## 📊 Estrutura dos Dados

A tabela `historico_criptomoedas` contém:

| Campo                | Descrição                                 |
|---------------------|--------------------------------------------|
| `symbol`            | Símbolo da criptomoeda (ex: BTC, ETH)      |
| `preco_atual_usd`   | Valor atual em dólares                     |
| `capitalizacao_mercado` | Indicador de capitalização de mercado |

---