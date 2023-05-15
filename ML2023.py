import pandas as pd
import numpy as np
import ipywidgets as widgets

import math

from IPython.display import display


# Primeira implementação do processo de precificação Ornstein-Uhlenbeck discreto: formulação ingênua.

def ou(valor_esperado=110, tempo_saida=20, phi=.5, sigma=.1, p_0=100, cenarios=10):
    '''
    Essa função é um draft; sintam-se livres para torná-la boa.
    :param valor_esperado: E_0(P_{i,T_i})
    :param tempo_saida: T_i
    :param p_0: preço inicial do asset
    :param phi: parâmetro do modelo que queremos estimar via ML
    :param sigma: parâmetro do modelo que queremos estimar via ML
    :param cenarios: define a quantidade de cenários, em construção não utilize por enquanto.
    
    Retorna um DataFrame com os preços: indices são ticks, colunas são cenários.
    '''
    historico_precos = pd.DataFrame(0, index=range(cenarios), columns=range(tempo_saida+1)) # Cria um DataFrame para os precos gerados com todas as entradas 0.
    perturbacao = pd.DataFrame(np.random.normal(loc=0, scale=1, size=(cenarios, tempo_saida+1))) # Cria um DataFrame para os epsilon_{i,t}
    perturbacao[0], historico_precos[0] = 0, p_0 # Adiciona os valores iniciais.
    for t in range(1, tempo_saida+1): # Loop que gera os preços (loops são demorados em python, talvez seria legal rever esta parte do código).
        historico_precos[t] = (1-phi)*valor_esperado + phi*historico_precos[t-1] + sigma*perturbacao[t] # Atualiza os valores t usando a fórmula.
    return historico_precos.transpose() # Retorna um DataFrame do jeito "certo" para ser analisado.

def grafico_ou(valor_esperado=110, tempo_saida=100, phi=.5, sigma=.1, p_0=100, cenarios=100):
    """
    :param valor_esperado: E_0(P_{i,T_i})
    :param tempo_saida: T_i
    :param p_0: preço inicial do asset
    :param phi: parâmetro do modelo que queremos estimar via ML
    :param sigma: parâmetro do modelo que queremos estimar via ML
    :param cenarios: define a quantidade de cenários, em construção não utilize por enquanto.
    
    Retorna um gráfico com os preços gerados via Ornstein-Uhlenbeck.
    """
    precos = ou(valor_esperado, tempo_saida, phi, sigma, p_0, cenarios)
    ax = precos.plot(color="goldenrod", alpha = 0.5, linewidth=2, figsize=(12,5), legend=False) # Desenha os cenários. Alpha é a transparência do traçado.
    ax.axhline(y=p_0, ls=":", color="gray") # Desenha uma linha no valor p_0.
    ax.axhline(y=valor_esperado, ls=":", color="black") # Desenha uma linha no valor esperado.
    ax.set_ylabel('Patrimônio (%)'), ax.set_xlabel('Tempo (ut)'), ax.set_title('Evolução Temporal de Patrimônio com preços gerados por Ornstein-Uhlenbeck')
    
def display_ou():
    '''
    Versão pedagógica do O-U. Em construção, no momento não permite parâmetros fornecidos pelo usuário.
    '''
    controles_ou = widgets.interactive(grafico_ou, 
                                   valor_esperado=widgets.IntSlider(min=90, max=110, step=1, value=105), 
                                   tempo_saida=widgets.IntSlider(min=10, max=1000, step=1, value=50),
                                   phi=(-1.5, 1.5, .01),
                                   sigma=(-.3, .3, .01),
                                   p_0=widgets.IntSlider(min=100, max=100, step=1, value=100),
                                   cenarios=widgets.IntSlider(min=10, max=1000, step=10, value=50))
    display(controles_ou)
    

