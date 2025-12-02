import streamlit as st
import pandas as pd

from src.connection_db import get_collection
from src.data_prep import colecao_para_df, normalizar_df, separar_por_data
from src.kpis import kpi_volume

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
st.title("📊 Visão Geral – Volume de Comentários")

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

# -------------------------
# KPIs PRINCIPAIS
# -------------------------
kpi = kpi_volume(df)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total de Comentários", kpi["total_avaliacoes"])

with col2:
    st.write("Volume por Origem")
    st.table(kpi["total_por_origem"])

st.subheader("Volume por Sentimento")
st.table(kpi["total_por_sentimento"])
