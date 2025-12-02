import pandas as pd

def kpi_volume_avancado(df):
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    df["periodo"] = df["data"].dt.to_period("M")

    volume_periodo = df.groupby("periodo").size()

    crescimento = volume_periodo.pct_change().fillna(0)

    origem_mais_crescimento = (
        df.groupby("origem")["data"]
          .count()
          .sort_values(ascending=False)
          .idxmax()
    )

    return {
        "volume_periodo": volume_periodo,
        "crescimento_periodo": crescimento,
        "origem_top": origem_mais_crescimento
    }

def kpi_sentimento_avancado(df):
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    mapa = {
        "muito positivo": 5,
        "positivo": 4,
        "neutro": 3,
        "negativo": 2,
        "muito negativo": 1
    }
    df["sent_score"] = df["sentimento_nlp"].map(mapa).fillna(3)

    df["periodo"] = df["data"].dt.to_period("M")
    sentimento_periodo = df.groupby("periodo")["sent_score"].mean()

    crescimento_sentimento = sentimento_periodo.pct_change().fillna(0)

    return {
        "sentimento_periodo": sentimento_periodo,
        "crescimento_sentimento": crescimento_sentimento,
        "sentimento_por_origem": df.groupby("origem")["sent_score"].mean(),
        "top_positivo": df.sort_values("sent_score", ascending=False).head(5),
        "top_negativo": df.sort_values("sent_score", ascending=True).head(5)
    }
