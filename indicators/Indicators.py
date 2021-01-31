import numpy as np
#Calculando alguns dos indicadores para alteração de parâmetros
class Indicators():
    def __init__(self,data,name='indicators'):
        self.data = data
        self.name = name
        self.regras_medias= [{'tipo':['simples','exponecial'],
                            'valor_usado':['close','open','high','low']}]
        self.regras_mm_longa = [{'tipo':['simples','exponecial'],
                            'periodo':[i for i in range(100)],
                            'valor_usado':['close','open','high','low']}]
        self.regras_macd = [{'valor_usado':['close','open','high','low']}]
        self.regras_ifr = [{'valor_usado':['close','open','high','low']}]
        self.regras_bands = [{'valor_usado':['close','open','high','low']}]
    def mmv(self,tipo,period,column):
        tipo = self.regras_medias[0]['tipo'][tipo]
        columns = self.regras_medias[0]['valor_usado'][column]
        if tipo == 'simples':
            self.data.insert(len(self.data.columns),'SMA'+str(period),self.data[columns].rolling(period).mean(),True)
        else:
            self.data.insert(len(self.data.columns),
                             'EMA'+str(period),self.data[columns].ewm(ignore_na=False,min_periods=period,com=period,adjust=True).mean(),True)
        return self.data,tipo,period,columns
    def macd(self,period_short=26,period_long=12,period_signal=int,column=int):
        remove_cols = []
        columns = self.regras_macd[0]['valor_usado'][column]
        if not 'EMA'+str(period_long) in self.data.columns:
            self.data,_,_,_ = self.mmv(1,period_long,column)
            remove_cols.append('EMA'+str(period_long))
        if not 'EMA'+str(period_short) in self.data.columns:
            self.data,_,_,_ = self.mmv(1,period_short,column)
            remove_cols.append('EMA' + str(period_short))
        self.data.insert(len(self.data.columns),'macd_val',self.data['EMA' + str(period_short)] - self.data['EMA' + str(period_long)],True)
        # self.data.loc[:,'macd_val'] = self.data['EMA' + str(period_short)] - self.data['EMA' + str(period_long)]
        self.data.insert(len(self.data.columns),'macd_signal_line',self.data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_signal, adjust=True).mean(),True)
        # self.data.loc[:,'macd_signal_line'] = self.data['macd_val'].ewm(ignore_na=False, min_periods=0, com=period_signal, adjust=True).mean()
        self.data = self.data.drop(remove_cols, axis=1)
        return self.data,period_short,period_long,period_signal,columns
    def bands(self,trend_periods=20, deviation=2, column=int):
        columns = self.regras_bands[0]['valor_usado'][column]
        self.data['bol_bands_middle'] = self.data[columns].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()
        for index, row in self.data.iterrows():
            s = self.data[columns].iloc[index - trend_periods: index]
            sums = 0
            middle_band = self.data.at[index, 'bol_bands_middle']
            for e in s:
                sums += np.square(e - middle_band)
            std = np.sqrt(sums / trend_periods)
            upper_band = middle_band + (deviation * std)
            lower_band = middle_band - (deviation * std)
            self.data.at[index,'bol_bands_upper']= upper_band
            self.data.at[index,'bol_bands_lower']= lower_band
        return self.data,trend_periods,columns
    def ifr(self,period=14,column=int):
        columns = self.regras_ifr [0]['valor_usado'][column]
        delta = self.data[columns].diff().dropna()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u = u.ewm(span=period,min_periods=0,adjust=False).mean() #first value is sum of avg gains
        d = d.ewm(span=period,min_periods=0,adjust=False).mean() #first value is sum of avg losses
        self.data['IFR'+str(period)]=1 - 1 / (1 + u/d)
        return self.data,period,columns
    def vwap(self):
        vol = self.data.VOL.values
        price = self.data.close.values
        self.data['VWAP'] = (vol*price).cumsum()/vol.cumsum()
        return self.data