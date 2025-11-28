import pandas as pd

def kpi_volume(df):
    return {
        "total_avaliacoes": len(df),
        "total_por_origem": df["origem"].value_counts(),
        "total_por_sentimento": df["sentimento_nlp"].value_counts(dropna=True)
    }


def kpi_sentimento(df):
    df = df.copy()

    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    mapa = {
        "muito positivo": 5,
        "positivo": 4,
        "neutro": 3,
        "negativo": 2,
        "muito negativo": 1
    }
    df["sent_numerico"] = df["sentimento_nlp"].map(mapa).fillna(3)

    return {
        "percentual_sentimentos": df["sentimento_nlp"].value_counts(normalize=True) * 100,
        "sentimento_medio_geral": df["sent_numerico"].mean(),
        "sentimento_por_origem": df.groupby("origem")["sent_numerico"].mean(),
        "sentimento_medio_por_periodo": df.groupby(df["data"].dt.to_period("M"))["sent_numerico"].mean()
    }