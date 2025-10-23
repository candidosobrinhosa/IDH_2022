import numpy as np
import pandas as pd

"""
Tábua de vida abreviada a partir das taxas nMx.
    nMx: Taxas de mortalidade por grupo etário.
    age: Etiquetas dos grupos etários (ex: ["0","1-4","5-9",...,"80+"])
    sex: 'M', 'F' ou 't' (total).
    open_age: Se True, último grupo é aberto (q=1).
"""
def life_table_abridged(nMx, age, sex='t', open_age=True):


    nMx = np.array(nMx, dtype=float)
    nMx[np.isnan(nMx)] = 0

    # intervalos de idade
    n = np.array([1, 4] + [5]*(len(nMx)-3) + [np.inf])
    n = n[:len(nMx)]

    # valores de a(x)
    nAx = np.array([0.07, 1.5] + [2.5]*(len(nMx)-3) + [5])
    nAx = nAx[:len(nMx)]

    # probabilidade de morte
    nqx = (n * nMx) / (1 + (n - nAx) * nMx)
    nqx[-1] = 1.0 if open_age else nqx[-1]

    # sobreviventes
    lx = [100000.0]
    for q in nqx[:-1]:
        lx.append(lx[-1] * (1 - q))
    lx = np.array(lx)

    ndx = lx[:-1] - lx[1:]
    Lx = n * lx[1:] + nAx[:-1] * ndx
    Lx = np.append(Lx, lx[-1] / nMx[-1] if nMx[-1] > 0 else 0)

    Tx = np.cumsum(Lx[::-1])[::-1]
    ex = Tx / lx[:-1]

    return pd.DataFrame({
        "Age": age[:len(lx)-1],
        "nMx": nMx[:len(lx)-1],
        "nqx": nqx[:len(lx)-1],
        "lx": lx[:-1],
        "ndx": ndx,
        "Lx": Lx[:-1],
        "Tx": Tx[:-1],
        "ex": ex
    })

    """
    Calcula e₀ (esperança de vida ao nascer) a partir de um DataFrame com colunas ['agegrp','nMx'].
    """
def calc_e0(df):

    age_order = ["0","1-4"] + [f"{i}-{i+4}" for i in range(5,80,5)] + ["80+"]
    df = df.set_index("agegrp").reindex(age_order).reset_index()
    nMx = df["nMx"].to_numpy(dtype=float)
    if not np.any(np.isfinite(nMx)):
        return np.nan
    lt = life_table_abridged(nMx, age=df["agegrp"].tolist())
    return lt["ex"].iloc[0]