# 🚦 Análise de Acidentes Rodoviários — PRF (2023–2025)

Dashboard interativo para exploração e visualização dos registros de acidentes nas rodovias federais brasileiras, construído com Python e Streamlit a partir dos dados públicos da Polícia Rodoviária Federal.

---

## 📋 Sobre o Projeto

Este projeto realiza o tratamento, análise e visualização dos dados de acidentes registrados pela PRF entre 2023 e 2025. O objetivo é identificar padrões de ocorrência, causas mais frequentes, distribuição geográfica e temporal, além de comparar a gravidade dos acidentes em diferentes contextos (período do dia, tipo de pista, fim de semana vs. dia útil).

---

## 📊 Funcionalidades do Dashboard

- **Resumo geral** — totais de acidentes, mortos, feridos, acidentes graves e ocorrências em fim de semana
- **Distribuição geográfica** — top 10 estados e rodovias federais com mais acidentes, segmentados por gravidade
- **Análise temporal** — acidentes por dia da semana, evolução mensal com comparativo de mortos, e análise de tendência por ano
- **Período do dia** — distribuição de acidentes e mortos hora a hora
- **Principais causas** — top 10 causas de acidentes registradas
- **Gravidade por tipo de pista** — relação entre infraestrutura viária e gravidade dos acidentes
- **Taxa de mortalidade** — comparação entre dias úteis e fins de semana
- **Tabela resumo por estado** — com percentual de acidentes graves e gradiente visual

### Filtros disponíveis

A barra lateral permite segmentar toda a análise por:

| Filtro | Opções |
|---|---|
| Estado (UF) | Todos os estados ou um específico |
| Período do Dia | Madrugada, Manhã, Tarde, Noite |
| Gravidade | Grave / Não Grave |
| Ano | 2023, 2024 ou 2025 |
| Mês | Janeiro a Dezembro |

---

## 🗂️ Estrutura do Repositório

```
analise-acidentes-prf/
├── app.py               # Dashboard Streamlit (visualizações e filtros)
├── Tratamento.py        # Pipeline de limpeza e enriquecimento dos dados
└── Dados/
    ├── datatran2023.csv # Dados brutos PRF 2023
    ├── datatran2024.csv # Dados brutos PRF 2024
    ├── datatran2025.csv # Dados brutos PRF 2025
    └── dados_tratados.csv # Dataset consolidado e tratado (gerado pelo Tratamento.py)
```

---

## ⚙️ Pipeline de Tratamento dos Dados

O script `Tratamento.py` executa as seguintes etapas:

1. **Consolidação** — leitura e concatenação dos três arquivos anuais (encoding `latin1`, separador `;`)
2. **Remoção de colunas** — descarte de `latitude`, `longitude`, `regional`, `uop`, `id` e `delegacia`
3. **Deduplicação** — remoção de registros duplicados
4. **Tratamento de nulos** — categorias preenchidas com `"Não Informado"`; colunas numéricas convertidas e preenchidas com `0`
5. **Engenharia de features** — criação das colunas:
   - `ano_acidente`, `mes_acidente`, `ano_mes`
   - `hora_acidente` (inteiro 0–23)
   - `periodo_dia` (Madrugada / Manhã / Tarde / Noite)
   - `acidente_grave` (Grave se há mortos ou feridos graves)
   - `fim_de_semana` (Sim / Não)
   - `br` formatada como `"BR-XXX"`
6. **Exportação** — geração do arquivo `Dados/dados_tratados.csv`

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+
- pip

### Instalação das dependências

```bash
pip install streamlit pandas numpy plotly matplotlib
```

### 1. Gerar os dados tratados

Execute este passo apenas uma vez (ou sempre que os dados brutos forem atualizados):

```bash
python Tratamento.py
```

### 2. Iniciar o dashboard

```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no navegador em `http://localhost:8501`.

---

## 📦 Dependências

| Biblioteca | Uso |
|---|---|
| `pandas` | Manipulação e análise de dados |
| `numpy` | Operações vetorizadas e classificações |
| `streamlit` | Interface web do dashboard |
| `plotly` | Gráficos interativos (barras empilhadas) |
| `matplotlib` | Gráficos estáticos (linhas, barras, taxa) |

---

## 🗃️ Fonte dos Dados

Os dados brutos são disponibilizados publicamente pela **Polícia Rodoviária Federal (PRF)** no portal de dados abertos do governo federal:

🔗 [https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-acidentes)

---


*Projeto acadêmico — Análise de Dados com Python.*
