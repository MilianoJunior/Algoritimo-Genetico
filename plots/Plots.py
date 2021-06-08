import pandas as pd
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *

class Plots():
    def __init__(self,name='plots_candlestick'):
        self.name = name
        
    def candlestick(self,Index,Open,High,Low,Close,result,title='candlestick'):
        trace1 = {
                    'x': Index,
                    'open': Open,
                    'close': Close,
                    'high': High,
                    'low': Low,
                    'type': 'candlestick',
                    'name': title,
                    'showlegend': True
                  }
        data = [trace1]
        for i in range(len(result)):
             
            if result.tipo[i] == 'compra':
                trace1 = {
                    'x':[result.inicio[i],result.fim[i]] ,
                    'y':[result.entrada[i],result.saida[i]],
                    'type': 'scatter',
                    'mode': 'lines',
                    'line': {
                        'width': 1,
                        'color': 'blue'
                    },
                    'name': 'Média (30 dias)'
                }
            else:
                trace1 = {
                    'x': [result.inicio[i],result.fim[i]],
                    'y': [result.entrada[i],result.saida[i]],
                    'type': 'scatter',
                    'mode': 'lines',
                    'line': {
                        'width': 1,
                        'color': 'red'
                    },
                    'name': 'Média (30 dias)'
                }
            data.append(trace1)
        
        # Config graph layout
        layout = go.Layout({
            'title': {
                'text': 'ganho final{}'.format(sum(result.ganhofinal)),
                'font': {
                    'size': 15
                }
            }
        })
        fig = dict(data=data,layout=layout)
        plot(fig)
        # fig = go.Figure(data=data, layout=layout)
        # fig.show()