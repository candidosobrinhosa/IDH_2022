import pandas as pd
import numpy as np

"""
Idade em anos para grupo etário quinquenal. Exemplos:
    0   -> "0"
    1-4 -> "1-4"
    5-9 -> "5-9"
    80> -> "80+"
    Intervalos entre 10 a 79 são computados com o laço else
"""
def age_to_group(age: float) -> str:

    if pd.isna(age):
        return np.nan
    if age < 1:
        return "0"
    elif age < 5:
        return "1-4"
    elif age >= 80:
        return "80+"
    else:
        lo = int((age // 5) * 5)
        hi = lo + 4
        return f"{lo}-{hi}"

"""
Taxas etárias de mortalidade (nMx) por município, sexo e grupo etário.
"""
def compute_nMx(df_pop: pd.DataFrame, df_obitos: pd.DataFrame) -> pd.DataFrame:

    df_pop = pop_final()
    df_obitos = df_obitos.copy()

    df_pop["agegrp"] = df_pop["idade"].apply(age_to_group)
    df_obitos["agegrp"] = df_obitos["idade"].apply(age_to_group)

    pop_q = df_pop.groupby(["cod_municipio","sexo","agegrp"], as_index=False)["pop"].sum()
    obitos_q = df_obitos.groupby(["cod_municipio","sexo","agegrp"], as_index=False)["obitos"].sum()

    mx = pd.merge(pop_q, obitos_q, on=["cod_municipio","sexo","agegrp"], how="outer").fillna(0)
    mx["nMx"] = np.where(mx["pop"] > 0, mx["obitos"]/mx["pop"], np.nan)

    return mx[["cod_municipio","sexo","agegrp","nMx"]]
