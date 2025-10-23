import pandas as pd
import numpy as np

"""
    Calcula o índice de saúde (IDH-Longevidade).
    Fórmula: IDH_Saúde = (e0 - 20) / (85 - 20)
"""
def compute_idh_saude(df_e0: pd.DataFrame) -> pd.DataFrame:
    df = df_e0.copy()
    df["idh_saude"] = np.clip((df["e0_total"] - 20) / 65, 0, 1)
    return df
