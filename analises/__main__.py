import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from analises.analise_escolaridade import analisa_escolaridade, plotar_escolaridade_uf


df = pd.read_csv('pefil-eleito/perfil_eleitorado_transferencia_2026.csv', sep=';', header=0, encoding='latin1')
df_instrucao = pd.read_csv('pefil-eleito/perfil_eleitorado_transferencia_2026.csv', sep=';', header=0, encoding='latin1')

print(df.head(2))
print(df.info())
print(df.columns)

fi = df["CD_GENERO"].value_counts().sort_index()

Fi = df["CD_GENERO"].value_counts(normalize=True).sort_index()

tabela_sexo = pd.DataFrame({
    'fi':fi,
    'Fi': Fi.round(4),
    'Fi%': (Fi * 100).round(2) 
})

tabela_sexo = tabela_sexo.rename(index={2: 'Masculino' , 4: 'Feminino'})

tabela_sexo.loc['Total'] = [tabela_sexo['fi'].sum(),
                            tabela_sexo['Fi'].sum().round(4),
                            tabela_sexo['Fi%'].sum().round(2)
                            ]
tabela_sexo['fi'] = tabela_sexo['fi'].astype(int)

print(tabela_sexo)


fi_instrucao = df_instrucao["CD_GRAU_INSTRUCAO"].value_counts().sort_index()
Fi_instrucao = df_instrucao["CD_GRAU_INSTRUCAO"].value_counts(normalize=True).sort_index()

tabela_grau_intrucao = pd.DataFrame({
    'fi': fi_instrucao,
    'Fi': Fi_instrucao.round(4),
    'Fi%': (Fi_instrucao * 100).round(2)
})

tabela_grau_intrucao = tabela_grau_intrucao.rename(index={
    1: 'Analfabeto',
    2: 'Ler e escrever',
    3: 'Ensino fundamental incompleto',
    4: 'Ensino fundamental completo',
    5: 'Ensino médio incompleto',
    6: 'Ensino médio completo',
    7: 'Ensino superior incompleto',
    8: 'Ensino superior completo'
})

tabela_grau_intrucao.loc['Total'] = [
    tabela_grau_intrucao['fi'].sum(),
    tabela_grau_intrucao['Fi'].sum().round(4),
    tabela_grau_intrucao['Fi%'].sum().round(2)
]

tabela_grau_intrucao['fi'] = tabela_grau_intrucao['fi'].astype(int)

print(tabela_grau_intrucao)

#plotar a tabela sexo
fig, ax = plt.subplots(figsize=(8, 4))

ax.axis('off')

ax.table(
    cellText=tabela_sexo.values,
    rowLabels=tabela_sexo.index,
    colLabels=tabela_sexo.columns,
    loc='center',
    cellLoc='center'
)

plt.title('Distribuição do eleitorado por sexo')
plt.show()


fig, ax = plt.subplots(figsize=(12, 6))

ax.axis('off')

ax.table(
    cellText=tabela_grau_intrucao.values,
    rowLabels=tabela_grau_intrucao.index,
    colLabels=tabela_grau_intrucao.columns,
    loc='center',
    cellLoc='center'
)

plt.title('Distribuição do eleitorado por formaçao academica')
plt.show()

tabela, percentual = analisa_escolaridade(df_instrucao)
print('Frequencia absoluta')
print(tabela)

print('Frequencia percentual')
print(tabela.round(2))

plotar_escolaridade_uf(percentual)