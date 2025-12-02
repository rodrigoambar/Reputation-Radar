import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from src.connection_db import get_collection
from src.data_prep import colecao_para_df, normalizar_df
import plotly.express as px
from src.kpis import kpi_sentimento_avancado, kpi_volume_avancado
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

st.title(" Visão Geral – Volume de Comentários")

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
st.markdown("""
    <style>
    div[data-baseweb="tag"] {
        background-color: #4169E1 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

#filtro por origem
filtro = st.multiselect('Escolha as origens que deseja avaliar: ', opcoes_origem, default=opcoes_origem)
if filtro:
     df = df[df["origem"].isin(filtro)]


# gráficos a partir dos KPis
#big numbers
total_avaliacoes = len(df)
total_positivo = df[df["sentimento_nlp"].isin(["positivo", "muito positivo"])].shape[0]
total_negativo = df[df["sentimento_nlp"].isin(["negativo", "muito negativo"])].shape[0]

# --- Layout dos cartões ---
col1, col2, col3 = st.columns(3)

col1.metric("Total de Avaliações", f"{total_avaliacoes:,}".replace(",", "."))
col2.metric("Total Positivo", f"{total_positivo:,}".replace(",", "."))
col3.metric("Total Negativo", f"{total_negativo:,}".replace(",", "."))

# primeiros gráficos:
df_com_data = df[df["data"].notna()].copy()
df_sem_data = df[df["data"].isna()].copy()

kpi_sent = kpi_sentimento_avancado(df_com_data)
sent = kpi_sent["sentimento_periodo"].reset_index()
sent["periodo"] = sent["periodo"].astype(str)

fig_line = px.line(sent, x="periodo", y="sent_score", markers=True,
              title="Sentimento Médio por Período")
# heatmap
kpi_sent_total = kpi_sentimento_avancado(df)
orig = kpi_sent_total["sentimento_por_origem"].reset_index()

fig_heat = px.density_heatmap(
    orig,
    x="origem",
    y="sent_score",
    z="sent_score",
    color_continuous_scale="RdYlGn",
    title="Sentimento Médio por Origem"
)

col1, col2 = st.columns([2, 1])    # 2/3 para o line chart, 1/3 para o heatmap
fig_line.update_layout(height=450)
fig_heat.update_layout(height=450)
fig_line.update_layout(title_x=0.5)
fig_heat.update_layout(title_x=0.2)
fig_line.update_layout(margin=dict(l=10, r=10, t=40, b=10))
fig_heat.update_layout(margin=dict(l=10, r=10, t=40, b=10))
with col1:
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.plotly_chart(fig_heat, use_container_width=True)

