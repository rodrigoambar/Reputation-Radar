import streamlit as st
from PIL import Image
import base64
from io import BytesIO
# ----------- CONFIGURAÇÃO GERAL DA PÁGINA -----------
st.set_page_config(
    page_title="Reputation Radar",
    page_icon="📊",
    layout="wide"
)

# ----------- LOGO ------
def imagem_base64(path):
    img = Image.open(path)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# ----------- TÍTULO DA HOME -----------
logo = imagem_base64(r"assests\rep_logo.png")
st.markdown(
    f"""
    <div style='text-align:center; padding: 10px;'>
        <img src='data:image/png;base64,{logo}' 
             style='width:120px; margin-bottom:10px;' />
        <h1 style='margin-bottom:0;'>Reputation Radar</h1>
        <h3 style='color:#666; margin-top:5px;'>
            Sua reputação monitorada em tempo real. Feedbacks transformados em vantagem competitiva.
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)


# ----------- DESCRIÇÃO PRINCIPAL -----------
st.markdown(
    """
    O **Reputation Radar** consolida comentários coletados automaticamente das plataformas:

    - ⭐ **Google Maps**  
    - 📱 **Google Play**  
    - 🛎️ **Reclame Aqui**

    Nossa plataforma utiliza técnicas de Big Data e Processamento de Linguagem Natural (NLP)  
    para gerar insights acionáveis sobre a percepção dos consumidores.
    """,
    unsafe_allow_html=False
)


st.markdown("---")


# ----------- CARDS DAS PÁGINAS PRINCIPAIS -----------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="
            border-radius: 12px;
            padding: 25px;
            background-color: #708090;
            border: 1px solid #ddd;
        ">
            <h2> Aba Geral</h2>
            <p style="color:#F5FFFA;">
                Visão consolidada da reputação da marca:
                <br> • KPIs de sentimento
                <br> • Evolução temporal
                <br> • Distribuição por origem
            </p>
            <a href="/analise_geral" target="_self">
                <button style="
                    background-color:#4CAF50;
                    padding:10px 20px;
                    border:none;
                    border-radius:8px;
                    color:white;
                    cursor:pointer;
                    font-size:16px;
                ">
                    Acessar Página
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="
            border-radius: 12px;
            padding: 25px;
            background-color: #708090;
            border: 1px solid #ddd;
        ">
            <h2> Análise de Comentários</h2>
            <p style="color:#F5FFFA;">
                Explore profundamente o conteúdo textual:
                <br> • Nuvem de palavras
                <br> • Ranking de termos
                <br> • Busca por palavras-chave
            </p>
            <a href="/analise_comentarios" target="_self">
                <button style="
                    background-color:#4CAF50;
                    padding:10px 20px;
                    border:none;
                    border-radius:8px;
                    color:white;
                    cursor:pointer;
                    font-size:16px;
                ">
                    Acessar Página
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------- FOOTER -----------
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; color:#999; padding-top:10px;'>
        Desenvolvido por <b>Reputation Radar</b> • Big Data & NLP para Reputação Corporativa
    </div>
    """,
    unsafe_allow_html=True
)