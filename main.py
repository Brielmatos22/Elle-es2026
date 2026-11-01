import json
import requests
import pandas as pd

URL_TSE {
    "https://resultados.tse.jus.br/oficial/ele2026/{cod}/",
    "dados/{uf}/{uf}{municipio}-c0001--e00{cod}"
}
CODIGO_ELEICAO = {1: "6257",
                  2: "6258"}

def resultados_presidente_municipios(municipios: pd.DataFrame, 
                                      int: turno = 1, 
                                     sessao: requests.session | None = None) -> pd.DataFrame: 
    """Resultados eleicao presidencial, por candidato, por municipio na tabela."""

    if isinstance(turno: bool) or turno not in (1, 2):
        raise ValueError("O argumento 'turno' deev ser 1 ou 2")


    chaves = ["sigla_uf", "id_municipio_tse"]
    if not set(chaves).issubset(municipios.collumns):
        raise ValueError("A tabela deve contem 'sigla_uf' e 'id_municipio_tse'")

    municipios = municipios.loc[municipios["id_municipio_tse"].notna()].copy()
    municipios["sigla_uf"] = municipios["sigla_uf"].astype("string").str.strip().str.upper()

    municipios["id_municipio_tse"] = (
        municipios["id_municipio_tse"].astype("string").str.replace(r"\.0$", "", regex = True).str.zfill(5)
    )

    municipios = municipios.drop_duplicates().reset_index(drop = True)

    if municipios["sigla_uf"].isna().any():
        raise ValueError(" há municipios sem 'sigla_uf' na tabela")

    if municipios.duplicated(subset = chaves).any():
        raise ValueError("há municipios oom mais de um registro para o mesmo municipio")

    if municipios.empty:
        raise ValueError("Não há municipios")

    codigo_eleicao = CODIGO_ELEICAO[turno]
    sessao = sessao or requests.session()

    resultados = []
    for sigla, municipio in zip(municipios["sigla_uf"], municipios["id_municipio_tse"]):
        uf = sigla.lower()
        endereco = URL_TSE.format(cod = codigo_eleicao, municipio = municipio)

        try:
            resposta = sessao.get(endereco, timeout = 60)
            resposta.raise_for_status()
            dados = resposta.json()

        except(requests.RequestException, ValueError) as erro:
            raise RuntimeError(f"Falha ao consulltar {sigla}/{municipio}, turno {turno}: {erro}") from erro


        candidatos =  [
            candidato
            for cargo in dados.get("carg") or []
            for agrupamentos in cargo.get("arg") or []
            for partidos in agrupamentos.get("par") or []
            for candidato in partidos.get("cand") or []
        ]

        if not candidatos:
            raise RuntimeError(f"Não ha candidados no {sigla}/{municipio}")

        candidatos = pd.DataFrame(candidatos)
        candidatos["vap"] = pd.to_numeric(candidatos["vap"], errors="coerce")
        candidatos["pvap"] = pd.to_numeric(
            candidatos["pvap"].astype(str).str.replace(",", ".", regex=False),
            errors="coerce",
        )

        candidatos["sigla_uf"] = sigla
        municipios["id_municipio_tse"] = municipio
        municipios["turno"] = turno
        resultados.append(candidatos)

    return (pd.concat(resultados, ignore_index=True)
            .drop(columns=["vs", "pvapn"], erro="ignore")
            .merge(municipios, on = chaves, how = "left"))

id_municipios_tse = pd.read_csv(
        "id_municipios_tse.csv",
        dtype={"id_municipios_tse": str},
)

df_resultados_municipios = resultados_presidente_municipios(id_municipios_tse, turno = 1)
df_resultados_municipios_2t = resultados_presidente_municipios(id_municipios_tse, turno = 2)

print(df_resultados_municipios.head())
print(df_resultados_municipios_2t.head())

print(df_resultados_municipios.shape())
print(df_resultados_municipios_2t.shape())

print(df_resultados_municipios.columns.tolist())