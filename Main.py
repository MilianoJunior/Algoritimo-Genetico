#importação das bibliotecas
import random
import pandas as pd
from data.Data import Data
from indicators.Indicators import Indicators
from enviroment.Env_trader import Env_trader
from rules.Rules import Rules
from plots.Plots import Plots

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#Serão constantes
ticket = 'WIN'                                     #papel negociado
direction_operations = 'comprado&vendido'          #operações possiveis: compra e venda a descoberto
amount_orders = 1                                  #quantidade de ordens 
start_time = '09:00'                               #horário inicial
end_time = '17:00'                                 #horário limite de operação
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#Serão variáveis
time_frame = 1                                     #tempo gráfico em min
stop = -200                                        #limite de perda por operação
gain = 200                                         #algo de ganho por operação
nun_days = 910                                   #numero de candles
batch_size = 1                                     #divisao em blocos
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#instanciar dados
data = Data(nun_days,batch_size)
entrada,entrada_trader,base,media,std = data.import_data()
colunas = ['Data','Hora', 'open', 'high', 'low', 'close','VOL']
base1 = base[colunas]
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#instanciar indicadores
indicators = Indicators(base1)
rules = Rules()
trader = Env_trader()
resultados = pd.DataFrame(columns=['mean-short-type','mean-short-period','mean-short-column','mean-long-type','mean-long-period','mean-long-column',
                                   'period-short-macd','period-long-macd','period-signal-macd','column-macd',
                                   'vwap',
                                   'period-IFR','column-IFR',
                                   'period-bands','column-bands',
                                   'rules-mean','rules-macd','rules-vwap',
                                   'ifr-regra','ifr-svenda','ifr-scompra','regra-bands',
                                   'mode','stop','gain',
                                   'qtd-operations','profit'])
#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
#Indicadores
maior = 0
mode_ = 0
result_ = 0
for j in range(1000):
    #Exploração aleatória
    stop = random.randrange(-150,-600,-5)                                    
    gain = random.randrange(150,600,5)    
    colunas = ['Data','Hora', 'open', 'high', 'low', 'close','VOL']
    base1 = base[colunas]
    indicators.data = base1
    parametro_media_curta = [random.randrange(0,2),random.randrange(1,100),random.randrange(0,4)]
    parametro_media_longa = [random.randrange(0,2),random.randrange(1,100),random.randrange(0,4)]
    parametros_macd = [random.randrange(1,100),
                   random.randrange(1,100),
                   random.randrange(1,100),
                   random.randrange(0,4)]
    parametros_ifr = [random.randrange(1,100),random.randrange(0,4)]
    parametros_bands = [random.randrange(1,100),random.randrange(0,4)]
    
    parametro_media_curta[1],parametro_media_longa[1] = rules.filtros(parametro_media_curta[1],parametro_media_longa[1])
    parametros_macd[1],parametros_macd[2] = rules.filtros(parametros_macd[1],parametros_macd[2])
    #¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    base1,tipoc,periodc,columnc = indicators.mmv(parametro_media_curta[0],parametro_media_curta[1],parametro_media_curta[2])
    base1,tipol,periodl,columnl = indicators.mmv(parametro_media_longa[0],parametro_media_longa[1],parametro_media_longa[2])
    base1,period_short_macd,period_long_macd,period_signal_macd,column_macd = indicators.macd(parametros_macd[0],parametros_macd[1],parametros_macd[2],parametros_macd[3])
    base1 = indicators.vwap()
    base1,period_ifr,column_ifr = indicators.ifr(parametros_ifr[0],parametros_ifr[1])
    base1,period_bands,column_band = indicators.bands(parametros_bands[0],2,parametros_bands[1])
    base1 = base1.dropna()
    base1 = base1.reset_index(drop=True)
    media1 = base1.columns[7]
    media2 = base1.columns[8]
    media3 = base1.columns[9]
    media4 = base1.columns[10]
    media5 = base1.columns[11]
    media6 = base1.columns[12]
    media7 = base1.columns[13]
    media8 = base1.columns[14]
    media9 = base1.columns[15]
    # print(media1,media2,media3,media4,media5,media6,media7,media8,media9)
    base2 = base[['Hora','open', 'high', 'low', 'close','VOL']]
    #¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
    # regras-----------------------------------------
    regra_media = random.randrange(0,2)
    regra_macd = random.randrange(0,2)
    regra_vwap= random.randrange(0,3)
    regra_ifr = random.randrange(0,2)
    regra_ifr_svenda = random.randrange(10,50)
    regra_ifr_scompra = random.randrange(50,100)
    regra_bands = random.randrange(0,2)
    mode = random.randrange(0,23)
    #------------------------------------------------
    trader.reset()
    for s in range(len(base1)):
        action1 = rules.medias(base1[media1][s],base1[media2][s],regra_media)
        action2 = rules.macd(base1[media3][s],base1[media4][s],regra_macd)
        action3 = rules.vwap(base2.values[s][3],base1[media5][s],regra_vwap)
        action4 = rules.ifr(base1[media6][s],regra_ifr_scompra,regra_ifr_svenda,regra_ifr)
        action5 = rules.bands(base2.values[s][3],base1[media8][s],base1[media9][s],regra_bands)
        # print(action1,action2,action3,action4,action5)
        action = rules.central_rules(action1,action2,action3,action4,action5,mode)
        result,buy,shell,reward = trader.agente(base2.values[s],action,stop,gain,0,0)
    ganho = sum(result.ganhofinal)
    if ganho > maior:
        maior = ganho
        mode_ = mode
        result_ = result
    print(j,'ganho final:',ganho,'mode: ',mode,' maior: ',maior,'mode:',mode_)
    #-----------------------------------------------
    resultados = resultados.append({'mean-short-type': tipoc,
                                    'mean-short-period': periodc,
                                    'mean-short-column': columnc,
                                    'mean-long-type': tipol,
                                    'mean-long-period': periodl,
                                    'mean-long-column': columnl,
                                    'period-short-macd':period_short_macd,
                                    'period-long-macd':period_long_macd,
                                    'period-signal-macd':period_signal_macd,
                                    'column-macd':column_macd,
                                    'vwap':True,
                                    'period-IFR':period_ifr,
                                    'column-IFR':column_ifr,
                                    'period-bands':period_bands,
                                    'column-bands':column_band,
                                    'rules-mean':regra_media,
                                    'rules-macd':regra_macd,
                                    'rules-vwap':regra_vwap,
                                    'ifr-regra':regra_ifr,
                                    'ifr-svenda':regra_ifr_svenda,
                                    'ifr-scompra':regra_ifr_scompra,
                                    'regra-bands':regra_bands,
                                    'mode':mode,
                                    'stop':stop,
                                    'gain':gain,
                                    'qtd-operations':len(result.ganhofinal),
                                    'profit':sum(result.ganhofinal)}, ignore_index=True)

#¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
# Plotar gráficos
plotar = Plots()
plotar.candlestick(base.Hora, base.open, base.high, base.low, base.close,result_)
bas,period_bands,column_band = indicators.bands(26,2,3)