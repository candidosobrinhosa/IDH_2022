import pandas as pd
import requests

url = "https://apisidra.ibge.gov.br/values/t/9514/n6/all/v/allxp/p/all/c2/allxt/c287/6653,49108,49109,60040,60041,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098/c286/113635"

# Lê e converte em DataFrame
resp = requests.get(url)
data = resp.json()
pop = pd.DataFrame(data[1:])

# Renomeia colunas
pop = pop.rename(columns={
    "D1C": "cod_municipio",
    "D2C": "sexo",
    "D3C": "grupo_idade",
    "V": "pop"
})

pop["pop"] = pd.to_numeric(pop["pop"], errors="coerce")

# Mapear sexo
pop["sexo"] = pop["sexo"].replace({
    "2": "Masculino",
    "4": "Feminino"
})

# Passar classificação etária
pop["grupo_idade"] = pop["grupo_idade"].replace({
    "6653": "0-4", "49108": "5-9", "49109": "10-14", "60040": "15-19",
    "60041": "20-24", "93070": "25-29", "93084": "30-34", "93085": "35-39",
    "93086": "40-44", "93087": "45-49", "93088": "50-54", "93089": "55-59",
    "93090": "60-64", "93091": "65-69", "93092": "70-74", "93093": "75-79",
    "93094": "80-84", "93095": "85-89", "93096": "90-94", "93097": "95-99",
    "93098": "100+"
})

# Agrupar 80+
pop["grupo_idade"] = pop["grupo_idade"].replace({
    "80-84": "80+",
    "85-89": "80+",
    "90-94": "80+",
    "95-99": "80+",
    "100+": "80+"
})

# Unificar
def tab_9514_proc():
    return pop.groupby(["cod_municipio","sexo","grupo_idade"], as_index=False)["pop"].sum()