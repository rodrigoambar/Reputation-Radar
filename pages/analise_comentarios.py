import streamlit as st
import pandas as pd
from src.connection_db import get_collection
from src.data_prep import colecao_para_df, normalizar_df
from src.kpis import kpi_sentimento_avancado


rename_ra = {
    "texto": "comentario",
    "sentimento": "sentimento_regra",
    "sentimento_comentario": "sentimento_nlp",
    "titulo": "titulo",
    "data": "data",
    "id": "id_review",
}
rename_play = {
    "content": "comentario",
    "score": "score",
    "sentimento": "sentimento_regra",
    "sentimento_comentario": "sentimento_nlp",
    "userName": "nome_usuario",
    "at": "data",
    "reviewId": "id_review",
    "reviewCreatedVersion": "versao",
    "replyContent": "resposta",
}
rename_maps = {
    "comentario": "comentario",
    "nota": "score",
    "sentimento": "sentimento_regra",
    "sentimento_comentario": "sentimento_nlp",
    "nome": "nome_usuario",
    "endereco": "endereco",
    "bairro": "bairro",
}

st.title(" Análise de comentários")

# -------------------------
# CARREGAMENTO
# -------------------------

@st.cache_data
def load_data():
    col_gmaps = get_collection("google_maps_com_nlp")
    col_play  = get_collection("google_play_com_nlp")
    col_ra    = get_collection("reclame_aqui_com_nlp")

    df_gmaps = normalizar_df(colecao_para_df(col_gmaps), "Google Maps", rename_maps)
    df_play  = normalizar_df(colecao_para_df(col_play),  "Google Play", rename_play)
    df_ra    = normalizar_df(colecao_para_df(col_ra),    "Reclame Aqui", rename_ra)

    df_total = pd.concat([df_gmaps, df_play, df_ra], ignore_index=True)

    return df_total

df = load_data()
print(df.columns)
opcoes_origem = sorted(df["origem"].dropna().unique())
#filtro por origem
filtro = st.multiselect('Escolha as origens que deseja avaliar: ', opcoes_origem, default=opcoes_origem)
if filtro:
     df = df[df["origem"].isin(filtro)]

df_com_data = df[df["data"].notna()].copy()
texto_col = "comentario"
    # KPIs avançados
kpis = kpi_sentimento_avancado(df_com_data)

    # ---- Big Numbers ----
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Sentimento Médio Geral", f"{kpis['sentimento_periodo'].mean():.2f}")

with col2:
    crescimento = kpis['crescimento_sentimento'].iloc[-1]
    st.metric("Crescimento do Sentimento", f"{crescimento*100:.1f}%", 
    delta=f"{crescimento*100:.1f}%")

with col3:
    melhor_origem = kpis["sentimento_por_origem"].idxmax()
    st.metric("Origem com Melhor Sentimento", melhor_origem)

    # fazer gráficos
    # ranking de palavras
    # juntar todo o texto limpo

top_positivo = kpis["top_positivo"]
top_negativo = kpis["top_negativo"]
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌟 Top 10 Comentários Positivos")
    for _, row in top_positivo.iterrows():
        st.success(f" 😁 nota: {row['sent_score']} — {row['comentario']}")

with col2:
    st.subheader("⚠️ Top 10 Comentários Negativos")
    for _, row in top_negativo.iterrows():
        st.error(f" 😞 nota: {row['sent_score']} — {row['comentario']}")