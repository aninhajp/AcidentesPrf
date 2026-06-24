import pandas as pd
import numpy as np

arquivos = [
    "Dados/datatran2023.csv",
    "Dados/datatran2024.csv",
    "Dados/datatran2025.csv"
]

dfs = []

for arquivo in arquivos:
    temp = pd.read_csv(arquivo, sep=";", encoding="latin1")
    dfs.append(temp)

df = pd.concat(dfs, ignore_index=True)

# Remoção de colunas
df = df.drop(columns=["latitude", "longitude", "regional", "uop", "id", "delegacia"])

# Remoção de duplicadas
antes = len(df)
df = df.drop_duplicates()
depois = len(df)
print(f"Duplicatas removidas: {antes - depois} registros")

# Tratamento dos nulos
colunas_categoricas = [
    "causa_acidente", "tipo_acidente", "condicao_metereologica",
    "tipo_pista", "tracado_via", "uso_solo", "fase_dia"
]
for coluna in colunas_categoricas:
    df[coluna] = df[coluna].fillna("Não Informado")

colunas_numericas = ["mortos", "feridos", "feridos_graves", "feridos_leves",
                  "ilesos", "ignorados", "veiculos"]
for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce").fillna(0).astype(int)

# Alterando tipos de dados
df["data_inversa"] = pd.to_datetime(df["data_inversa"], errors="coerce")

df["ano_acidente"] = df["data_inversa"].dt.year

# Mês do acidente
df["mes_acidente"] = df["data_inversa"].dt.month

df["ano_mes"] = df["data_inversa"].dt.to_period("M").astype(str)

# Adiconando BR- e alterando o tipo dos dados
df["br"] = "BR-" + df["br"].astype(str).str.replace(".0", "", regex=False)

# Hora do acidente (inteiro 0–23)
df["hora_acidente"] = pd.to_datetime(
    df["horario"], format="%H:%M:%S", errors="coerce"
).dt.hour

# Período do dia
df["periodo_dia"] = np.select(
    [df["hora_acidente"] < 6, df["hora_acidente"] < 12, df["hora_acidente"] < 18],
    ["Madrugada", "Manhã", "Tarde"],
    default="Noite"
)

# Classificando gravidade
df["acidente_grave"] = np.where(
    (df["mortos"] > 0) | (df["feridos_graves"] > 0),
    "Grave",
    "Não Grave"
)

# Indicador de fim de semana
df["fim_de_semana"] = np.where(
    df["dia_semana"].str.lower().isin(["sábado", "domingo"]),
    "Sim",
    "Não"
)

# Verificações finais
print("\nShape final")
print(f"Linhas: {df.shape[0]:,} | Colunas: {df.shape[1]}")

print("\nDistribuição de Gravidade")
print(df["acidente_grave"].value_counts())

print("\nDistribuição por Período do Dia")
print(df["periodo_dia"].value_counts())

print("\nNulos remanescentes (top 10)")
nulos = df.isnull().sum()
print(nulos[nulos > 0].sort_values(ascending=False).head(10))
print("\nInformações do DataFrame:")
print(df.info())

# Exportando dados tratados
df.to_csv("Dados/dados_tratados.csv", index=False)
print("\nArquivo Salvo")