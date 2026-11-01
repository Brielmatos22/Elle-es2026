import pandas as pd
import matplotlib.pyplot as plt


def analisa_escolaridade(df):
    escolaridade = {
        1: 'Analfabeto',
        2: 'Ler e escrever',
        3: 'Ensino fundamental incompleto',
        4: 'Ensino fundamental completo',
        5: 'Ensino médio incompleto',
        6: 'Ensino médio completo',
        7: 'Ensino superior incompleto',
        8: 'Ensino superior completo'
    }

    # Tabela de frequencia absoluta
    tabela = pd.crosstab(df['SG_UF_ORIGEM'],
                         df['CD_GRAU_INSTRUCAO'])

    tabela = tabela.rename(columns=escolaridade)

    #Tabela de frequencia relativa
    percentual = pd.crosstab(df['SG_UF_ORIGEM'],
                        df['CD_GRAU_INSTRUCAO'],
                        normalize = 'index') * 100
    
    percentual = percentual.rename(columns=escolaridade) 

    return tabela, percentual

def plotar_escolaridade_uf(percentual):
    percentual.plot(
        kind = 'bar',
        stacked = True,
        figsize = (15, 7)
    )

    plt.title('Nivel de escolaridade dos eleitores por UF')
    plt.xlabel('Unidade federativa')
    plt.ylabel('Percentual (%)')
    plt.legend(
        title = 'Grau de instrução',
        bbox_to_anchor = (1.02, 1)
    )

    plt.tight_layout()
    plt.show()

