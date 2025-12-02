import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from src.connection_db import get_collection
from src.data_prep import colecao_para_df, normalizar_df

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

st.title("📊 Análise de comentários")

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

