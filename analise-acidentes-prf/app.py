import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


# Configuração da página
st.set_page_config(
    page_title="Acidentes PRF 2025",
    layout="wide",
)

plt.rcParams.update({
    "figure.facecolor": "#0E1117",
    "axes.facecolor": "#0E1117",
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
})

COR_PRINCIPAL  = "#1E3A5F"
COR_SECUNDARIA = "#4F86C6"
COR_DESTAQUE   = "#E9C46A"
COR_GRAVE      = "#264653"
COR_NAO_GRAVE  = "#6C8EBF"


# Funções para geração dos gráficos
def plot_barras_vertical(series: pd.Series, titulo: str,
                          ylabel: str, cor: str,
                          rotacao: int = 0) -> plt.Figure:
    """Gráfico de barras vertical com rótulos de valor."""
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(series.index, series.values, color=cor, edgecolor="white")
    ax.set_title(titulo, fontweight="bold", pad=10)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotacao, ha="right" if rotacao else "center")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h * 1.01,
                f"{h:,.0f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    return fig


def plot_barras_horizontal(series: pd.Series, titulo: str,
                            xlabel: str, cor: str) -> plt.Figure:
    """Gráfico de barras horizontal com rótulos de valor."""
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(series.index[::-1], series.values[::-1],
                   color=cor, edgecolor="white")
    ax.set_title(titulo, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel)
    for bar in bars:
        w = bar.get_width()
        ax.text(w * 1.01, bar.get_y() + bar.get_height() / 2,
                f"{w:,.0f}", va="center", fontsize=9)
    fig.tight_layout()
    return fig

def plot_linha_mensal(df: pd.DataFrame) -> plt.Figure:
    """Evolução mensal: acidentes (eixo esq.) e mortos (eixo dir.)."""
    mensal = (
        df.groupby("mes_acidente")
          .agg(acidentes=("mes_acidente", "count"), mortos=("mortos", "sum"))
          .reset_index()
    )
    fig, ax1 = plt.subplots(figsize=(9, 4))
    ax2 = ax1.twinx()

    ax1.plot(mensal["mes_acidente"], mensal["acidentes"],
             color=COR_SECUNDARIA, marker="o", linewidth=2, label="Acidentes")
    ax2.plot(mensal["mes_acidente"], mensal["mortos"],
             color=COR_PRINCIPAL, marker="s", linewidth=2,
             linestyle="--", label="Mortos")

    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Nº de Acidentes", color=COR_SECUNDARIA)
    ax2.set_ylabel("Nº de Mortos",    color=COR_PRINCIPAL)
    meses_abrev = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}
    ax1.set_xticks(mensal["mes_acidente"])
    ax1.set_xticklabels(
    [meses_abrev[m] for m in mensal["mes_acidente"]]
)
    ax1.set_title("Distribuição de Acidentes por Mês",
                  fontweight="bold", pad=10)

    linhas_acidentes, labels_acidentes = ax1.get_legend_handles_labels()
    linhas_mortos, labels_mortos = ax2.get_legend_handles_labels()
    ax1.legend(linhas_acidentes + linhas_mortos, labels_acidentes + labels_mortos, loc="upper right")
    fig.tight_layout()
    return fig

# Carregamento dos dados
@st.cache_data
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv("Dados/dados_tratados.csv")


# Construção do dashboard
def main() -> None:
    df_original = carregar_dados()

    # Cabeçalho
    st.title("Análise de Acidentes Rodoviários — PRF 2025")
    st.markdown(
        "Exploração dos registros de acidentes nas rodovias federais brasileiras. "
        "Utilize os filtros na barra lateral para segmentar a análise."
    )
    st.divider()

    # Filtros laterais
    st.sidebar.header("Filtros")

    # Estado
    ufs = sorted(df_original["uf"].dropna().unique())
    ufs_selecionadas = st.sidebar.selectbox(
        "Estado (UF)",
        ["Todos"] + ufs
    )

    # Período
    periodos = sorted(df_original["periodo_dia"].dropna().unique())
    periodos_selecionados = st.sidebar.selectbox(
        "Período do Dia",
        ["Todos"] + periodos
    )

    # Gravidade
    gravidades = sorted(df_original["acidente_grave"].dropna().unique())
    gravidades_selecionadas = st.sidebar.selectbox(
        "Gravidade",
        ["Todos"] + gravidades
    )

    anos = sorted(df_original["ano_acidente"].unique())
    ano_selecionado= st.sidebar.selectbox("Ano", ["Todos"] + anos)

    # Mês
    meses_nomes = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    meses_disponiveis = sorted(df_original["mes_acidente"].dropna().unique().astype(int))
    meses_selecionados = st.sidebar.selectbox(
        "Mês",
        ["Todos"] + meses_disponiveis,
        format_func=lambda m: "Todos" if m == "Todos" else meses_nomes[m]
    )

    # Aplicação dos filtros

    if ufs_selecionadas == "Todos":
        filtro_uf = df_original["uf"].notna()
    else:
        filtro_uf = df_original["uf"] == ufs_selecionadas

    if periodos_selecionados == "Todos":
        filtro_periodo = df_original["periodo_dia"].notna()
    else:
        filtro_periodo = df_original["periodo_dia"] == periodos_selecionados

    if gravidades_selecionadas == "Todos":
        filtro_gravidade = df_original["acidente_grave"].notna()
    else:
        filtro_gravidade = df_original["acidente_grave"] == gravidades_selecionadas

    if meses_selecionados == "Todos":
        filtro_mes = df_original["mes_acidente"].notna()
    else:
        filtro_mes = df_original["mes_acidente"] == meses_selecionados

    if ano_selecionado == "Todos":
        filtro_ano = df_original["ano_acidente"].notna()
    else:
        filtro_ano = df_original["ano_acidente"] == ano_selecionado

    df = df_original[
        filtro_uf &
        filtro_periodo &
        filtro_gravidade &
        filtro_mes &
        filtro_ano
    ].copy()

    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return

    # Métricas gerais
    st.subheader("Resumo Geral")
    coluna_acidentes, coluna_mortos, coluna_feridos, coluna_graves, coluna_fim_semana = st.columns(5)
    coluna_acidentes.metric("Total de Acidentes",  f"{len(df):,}")
    coluna_mortos.metric("Total de Mortos",     f"{int(df['mortos'].sum()):,}")
    coluna_feridos.metric("Total de Feridos",    f"{int(df['feridos'].sum()):,}")
    coluna_graves.metric("Acidentes Graves",
              f"{(df['acidente_grave'] == 'Grave').sum():,}")
    coluna_fim_semana.metric("Em Fim de Semana",
              f"{(df['fim_de_semana'] == 'Sim').sum():,}")
    st.divider()

    # Distribuição Geográfica
    st.subheader("Distribuição Geográfica")
    coluna_estados, coluna_rodovias = st.columns(2)

    with coluna_estados:
        top_ufs = (
            df.groupby("uf")["acidente_grave"]
              .value_counts()
              .unstack(fill_value=0)
              .assign(Total=lambda x: x.sum(axis=1))
              .sort_values("Total", ascending=False)
              .head(10)
        )
        grave_uf    = top_ufs.get("Grave",    pd.Series(0, index=top_ufs.index))
        nao_grave_uf = top_ufs.get("Não Grave", pd.Series(0, index=top_ufs.index))
        total_uf    = top_ufs["Total"]
        ufs_ordem   = top_ufs.index.tolist()[::-1]

        fig_uf = go.Figure()
        fig_uf.add_trace(go.Bar(
            name="Grave",
            y=ufs_ordem,
            x=grave_uf.reindex(ufs_ordem),
            orientation="h",
            marker_color=COR_GRAVE,
            customdata=[[
                grave_uf.reindex(ufs_ordem)[u],
                round(grave_uf.reindex(ufs_ordem)[u] / total_uf.reindex(ufs_ordem)[u] * 100, 1)
            ] for u in ufs_ordem],
            hovertemplate="<b>%{y}</b><br>Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
        ))
        fig_uf.add_trace(go.Bar(
            name="Não Grave",
            y=ufs_ordem,
            x=nao_grave_uf.reindex(ufs_ordem),
            orientation="h",
            marker_color=COR_NAO_GRAVE,
            customdata=[[
                nao_grave_uf.reindex(ufs_ordem)[u],
                round(nao_grave_uf.reindex(ufs_ordem)[u] / total_uf.reindex(ufs_ordem)[u] * 100, 1)
            ] for u in ufs_ordem],
            hovertemplate="<b>%{y}</b><br>Não Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
        ))
        # Anotações com total no final de cada barra
        for u in ufs_ordem:
            fig_uf.add_annotation(
                x=total_uf.reindex(ufs_ordem)[u],
                y=u,
                text=f"{total_uf.reindex(ufs_ordem)[u]:,}",
                showarrow=False,
                xanchor="left",
                xshift=5,
                font=dict(size=11, color="white"),
            )
        fig_uf.update_layout(
            barmode="stack",
            title="Top 10 Estados com Mais Acidentes",
            xaxis_title="Nº de Acidentes",
            xaxis=dict(range=[0, total_uf.max() * 1.18]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
            margin=dict(l=10, r=10, t=60, b=10),
        )
        st.plotly_chart(fig_uf, use_container_width=True)

    with coluna_rodovias:
        if "br" in df.columns:
            top_brs = (
                df.groupby("br")["acidente_grave"]
                  .value_counts()
                  .unstack(fill_value=0)
                  .assign(Total=lambda x: x.sum(axis=1))
                  .sort_values("Total", ascending=False)
                  .head(10)
            )
            grave_br     = top_brs.get("Grave",     pd.Series(0, index=top_brs.index))
            nao_grave_br = top_brs.get("Não Grave", pd.Series(0, index=top_brs.index))
            total_br     = top_brs["Total"]
            brs_ordem    = top_brs.index.tolist()[::-1]

            fig_br = go.Figure()
            fig_br.add_trace(go.Bar(
                name="Grave",
                y=brs_ordem,
                x=grave_br.reindex(brs_ordem),
                orientation="h",
                marker_color=COR_GRAVE,
                customdata=[[
                    grave_br.reindex(brs_ordem)[b],
                    round(grave_br.reindex(brs_ordem)[b] / total_br.reindex(brs_ordem)[b] * 100, 1)
                ] for b in brs_ordem],
                hovertemplate="<b>%{y}</b><br>Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
            ))
            fig_br.add_trace(go.Bar(
                name="Não Grave",
                y=brs_ordem,
                x=nao_grave_br.reindex(brs_ordem),
                orientation="h",
                marker_color=COR_NAO_GRAVE,
                customdata=[[
                    nao_grave_br.reindex(brs_ordem)[b],
                    round(nao_grave_br.reindex(brs_ordem)[b] / total_br.reindex(brs_ordem)[b] * 100, 1)
                ] for b in brs_ordem],
                hovertemplate="<b>%{y}</b><br>Não Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
            ))
            # Anotações com total no final de cada barra
            for b in brs_ordem:
                fig_br.add_annotation(
                    x=total_br[b],
                    y=b,
                    text=f"{total_br[b]:,}",
                    showarrow=False,
                    xanchor="left",
                    xshift=5,
                    font=dict(size=11, color="white"),
                )
            fig_br.update_layout(
                barmode="stack",
                title="Top 10 Rodovias com Mais Acidentes",
                xaxis_title="Nº de Acidentes",
                xaxis=dict(range=[0, total_br.max() * 1.18]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=400,
                margin=dict(l=10, r=10, t=60, b=10),
            )
            st.plotly_chart(fig_br, use_container_width=True)

    st.divider()

    # Temporal
    st.subheader("Análise Temporal")
    coluna_dias_semana, coluna_evolucao_mensal = st.columns(2)

    with coluna_dias_semana:
        # Ordena dias da semana corretamente
        ordem_dias = ["segunda-feira", "terça-feira", "quarta-feira",
                      "quinta-feira", "sexta-feira", "sábado", "domingo"]
        resumo_dia = df["dia_semana"].str.lower().value_counts()
        resumo_dia = resumo_dia.reindex(
            [d for d in ordem_dias if d in resumo_dia.index]
        ).dropna()
        resumo_dia.index = [d.capitalize() for d in resumo_dia.index]
        st.pyplot(plot_barras_vertical(
            resumo_dia,
            "Acidentes por Dia da Semana",
            "Nº de Acidentes",
            COR_DESTAQUE,
            rotacao=35,
        ))

    with coluna_evolucao_mensal:
        st.pyplot(plot_linha_mensal(df))

    st.divider()

    # Período e Causas
    st.subheader("Período do Dia e Principais Causas")
    coluna_hora, coluna_causa = st.columns([1, 1])

    with coluna_hora:
        por_hora = (
            df.groupby("hora_acidente")
              .agg(acidentes=("hora_acidente", "count"), mortos=("mortos", "sum"))
              .reset_index()
        )
        fig_hora, ax_hora1 = plt.subplots(figsize=(6, 4))
        ax_hora2 = ax_hora1.twinx()

        ax_hora1.plot(por_hora["hora_acidente"], por_hora["acidentes"],
                      color=COR_SECUNDARIA, marker="o", linewidth=2, label="Acidentes")
        ax_hora2.plot(por_hora["hora_acidente"], por_hora["mortos"],
                      color=COR_PRINCIPAL, marker="s", linewidth=2,
                      linestyle="--", label="Mortos")

        ax_hora1.set_xlabel("Hora do Dia")
        ax_hora1.set_ylabel("Nº de Acidentes", color=COR_SECUNDARIA)
        ax_hora2.set_ylabel("Nº de Mortos", color=COR_PRINCIPAL)
        ax_hora1.set_xticks(range(0, 24, 2))
        ax_hora1.set_title("Acidentes e Mortos por Hora do Dia", fontweight="bold", pad=10)

        l1, lb1 = ax_hora1.get_legend_handles_labels()
        l2, lb2 = ax_hora2.get_legend_handles_labels()
        ax_hora1.legend(l1 + l2, lb1 + lb2, loc="upper left", fontsize=8)
        fig_hora.tight_layout()
        st.pyplot(fig_hora)

    with coluna_causa:
        top_causas = df["causa_acidente"].value_counts().head(10)
        st.pyplot(plot_barras_horizontal(
            top_causas,
            "Top 10 Causas de Acidentes",
            "Nº de Ocorrências",
            COR_PRINCIPAL,
        ))

    st.divider()

    # Gravidade dos acidentes
    st.subheader("Gravidade dos Acidentes")

    if "tipo_pista" in df.columns:
        tabela_pista = (
            df.groupby("tipo_pista")["acidente_grave"]
              .value_counts()
              .unstack(fill_value=0)
              .assign(Total=lambda x: x.sum(axis=1))
        )
        grave_pista    = tabela_pista.get("Grave",    pd.Series(0, index=tabela_pista.index))
        nao_grave_pista = tabela_pista.get("Não Grave", pd.Series(0, index=tabela_pista.index))
        total_pista    = tabela_pista["Total"]

        fig_pista = go.Figure()
        fig_pista.add_trace(go.Bar(
            name="Grave",
            x=tabela_pista.index,
            y=grave_pista,
            marker_color=COR_GRAVE,
            customdata=[
                [grave_pista[p], round(grave_pista[p] / total_pista[p] * 100, 1)]
                for p in tabela_pista.index
            ],
            hovertemplate="<b>%{x}</b><br>Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
        ))
        fig_pista.add_trace(go.Bar(
            name="Não Grave",
            x=tabela_pista.index,
            y=nao_grave_pista,
            marker_color=COR_NAO_GRAVE,
            customdata=[
                [nao_grave_pista[p], round(nao_grave_pista[p] / total_pista[p] * 100, 1)]
                for p in tabela_pista.index
            ],
            hovertemplate="<b>%{x}</b><br>Não Grave: %{customdata[0]:,} (%{customdata[1]}%)<extra></extra>",
        ))
        fig_pista.update_layout(
            barmode="stack",
            title="Gravidade por Tipo de Pista",
            xaxis_title="Tipo de Pista",
            yaxis_title="Nº de Acidentes",
            legend=dict(title="Gravidade", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=420,
            margin=dict(l=10, r=10, t=60, b=10),
        )
        st.plotly_chart(fig_pista, use_container_width=True)

    st.divider()

    # Fim de Semana
    st.subheader("Acidentes em Fim de Semana")

    taxa_fds = (
        df.groupby("fim_de_semana")
          .agg(acidentes=("fim_de_semana", "count"), mortos=("mortos", "sum"))
          .assign(taxa=lambda x: (x["mortos"] / x["acidentes"] * 100).round(2))
          .rename(index={"Sim": "Fim de Semana", "Não": "Dia Útil"})
    )

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])
    with col_centro:
        fig_taxa, ax_taxa = plt.subplots(figsize=(5, 3.5))
        bars = ax_taxa.bar(
            taxa_fds.index,
            taxa_fds["taxa"],
            color=[COR_PRINCIPAL, COR_DESTAQUE],
            edgecolor="white",
            width=0.4,
        )
        ax_taxa.set_title("Taxa de Mortalidade: Dia Útil vs Fim de Semana",
                          fontweight="bold", pad=10)
        ax_taxa.set_ylabel("Mortos por 100 Acidentes")
        for bar in bars:
            h = bar.get_height()
            ax_taxa.text(bar.get_x() + bar.get_width() / 2, h + 0.02,
                         f"{h:.2f}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
        ax_taxa.set_ylim(0, taxa_fds["taxa"].max() * 1.25)
        fig_taxa.tight_layout()
        st.pyplot(fig_taxa)

    st.divider()

    # Análise de Tendência e Sazonalidade
    st.subheader("Análise de Tendência e Sazonalidade")

    evolucao = (
        df_original.groupby(["ano_acidente", "mes_acidente"])
        .size()
        .reset_index(name="acidentes")
    )

    fig_tendencia, ax = plt.subplots(figsize=(10, 4))

    for ano in sorted(evolucao["ano_acidente"].unique()):
        dados_ano = evolucao[evolucao["ano_acidente"] == ano]

        ax.plot(
            dados_ano["mes_acidente"],
            dados_ano["acidentes"],
            marker="o",
            linewidth=2,
            label=str(ano)
        )

    meses_abrev = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([meses_abrev[m] for m in range(1, 13)])

    ax.set_title(
        "Comparação Mensal de Acidentes por Ano",
        fontweight="bold"
    )

    ax.set_xlabel("Mês")
    ax.set_ylabel("Quantidade de Acidentes")
    ax.legend(title="Ano")

    fig_tendencia.tight_layout()

    st.pyplot(fig_tendencia)

    st.info("""
    Esta análise compara a evolução mensal dos acidentes entre 2023, 2024 e 2025.
    O objetivo é verificar se a redução observada entre dezembro e janeiro representa
    um comportamento sazonal recorrente ou um evento específico de determinado ano.
    """)

    st.divider()

    # Tabela Resumo por UF
    st.subheader("Tabela Resumo por Estado")
    resumo_tabela = (
        df.groupby("uf")
          .agg(
              Acidentes=("uf", "count"),
              Mortos=("mortos", "sum"),
              Feridos=("feridos", "sum"),
              Graves=(
                  "acidente_grave",
                  lambda x: (x == "Grave").sum()
              ),
          )
          .sort_values("Acidentes", ascending=False)
          .reset_index()
          .rename(columns={"uf": "UF"})
    )
    resumo_tabela["% Graves"] = (
        resumo_tabela["Graves"] / resumo_tabela["Acidentes"] * 100
    ).round(1)

    st.dataframe(
        resumo_tabela.style
            .format({
                "Acidentes": "{:,}",
                "Mortos":    "{:,}",
                "Feridos":   "{:,}",
                "Graves":    "{:,}",
                "% Graves":  "{:.1f}%",
            })
            .background_gradient(subset=["% Graves"], cmap="Reds"),
        use_container_width=True,
    )

    st.caption(
        "Fonte: Polícia Rodoviária Federal (PRF) — dados públicos 2025. "
        "Projeto acadêmico — Análise de Dados com Python."
    )


if __name__ == "__main__":
    main()