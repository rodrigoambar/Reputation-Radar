import pandas as pd

# Função para converter coleção em DataFrame com tag de origem
def colecao_para_df(colecao):
    dados = list(colecao.find())  # Busca todos os documentos
    df = pd.DataFrame(dados) 
    return df

def normalizar_df(df, origem, rename_map):
    df = df.copy()
    
    # Renomeia colunas
    df = df.rename(columns=rename_map)

    # Adiciona a origem
    df["origem"] = origem

    # Garante que todas as colunas principais existam
    colunas_finais = [
        "comentario", "data", "origem","sentimento_nlp", 
        "_id", "nome_usuario"
    ]

    for col in colunas_finais:
        if col not in df.columns:
            df[col] = None


    return df[colunas_finais]




