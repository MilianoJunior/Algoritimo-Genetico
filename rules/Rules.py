import numpy as np
#class regras
class Rules():
    def __init__(self,name='regras'):
        self.name = name
        self.aux_venda =  True
        self.aux_compra = True
        self.macd_venda =  True
        self.macd_compra = True
        self.vwap_venda =  True
        self.vwap_compra = True
        self.ifr_venda =  False
        self.ifr_compra = False
        self.bands_venda =  False
        self.bands_compra = False
        self.regras_medias_a = ['cruz_mma','mediacurta_abaixolonga']
        self.regras_macd_a = ['cruz_macd','macdacima_linhasinal']
        self.regra_vwap = ['rompimento','compra_acima','venda_acima']
        self.regra_ifr = ['cruzamento_ifr','ifr_acima']
        self.regra_bands = ['cruzamento_bands','bands_acima']
    def filtros(self,curta,longa):
        if curta > longa:
            longa_ = curta
            curta_ = longa
            return curta_,longa_
        elif curta == longa:
            curta = curta -1
            return curta,longa
        else:
            return curta,longa
    def medias(self,ma_curta,ma_longa,regra):
        regra_ = self.regras_medias_a[regra]
        if np.isnan(ma_curta) or np.isnan(ma_longa):
            return 0
        ma_curta = float(ma_curta)
        ma_longa = float(ma_longa)
        r1 = True if regra_ =='cruz_mma'else False
        r2 = 'nada'
        if ma_curta > ma_longa and self.aux_compra:
            self.aux_compra = False
            self.aux_venda = True
            r2 = 'compra'
        if ma_curta < ma_longa and self.aux_venda:
            self.aux_compra = True
            self.aux_venda = False
            r2 = 'venda'
        if r1:
            # print('regra:',regra_,'ma_curta:',round(ma_curta,2),
            #       'ma_longa:',round(ma_longa,2),'maior:',ma_curta > ma_longa,
            #       'compra:',self.aux_compra,'venda:',self.aux_venda,'resultado:',r2)
            if r2 =='compra':
                return 1
            if r2 == 'venda':
                return 2
            else:
                return 0
        else:
            # print('regra:',regra_,'ma_curta:',round(ma_curta,2),
            #       'ma_longa:',round(ma_longa,2),'maior:',ma_curta > ma_longa)
            if ma_curta > ma_longa:
                # print('compra')
                return 1
            else:
                # print('venda')
                return 2
            
    def macd(self,macd,sinal,regra):
        regra_  = self.regras_macd_a[regra] 
        if np.isnan(macd) or np.isnan(sinal):
            return 0
        macd = float(macd)
        sinal = float(sinal)
        r1 = True if regra_=='cruz_macd'else False
        r2 = 'nada'
        if macd > sinal and self.macd_compra:
            self.macd_compra = False
            self.macd_venda = True
            r2 = 'compra'
        if macd < sinal and self.macd_venda:
            self.macd_compra = True
            self.macd_venda = False
            r2 = 'venda'
        if r1:
            if r2 =='compra':
                return 1
            if r2 == 'venda':
                return 2
            else:
                return 0
        else:
            if macd > sinal:
                return 1
            else:
                return 2
    def vwap(self,preco,vwap,regra):
#       rompimento da vwap, compra quando rompe para cima, venda quando rompe para baixo.
#       compra acima da vwap/vende abaixo do vwap
#       vende acima da vwap/compra abaixo da vwap
        regra_ = self.regra_vwap[regra]
        if np.isnan(vwap) and np.isnan(preco):
            return 0
        r1 = True if regra_=='rompimento'else False
        r2 = True if regra_=='compra_acima'else False
        r3 = True if regra_=='venda_acima'else False
        r4 = 'nada'
        preco = float(preco)
        vwap=float(vwap)
        if preco > vwap and self.vwap_compra:
            self.vwap_compra = False
            self.vwap_venda = True
            r4 = 'compra'
        if preco < vwap and self.vwap_venda:
            self.vwap_compra = True
            self.vwap_venda = False
            r4 = 'venda'
        if r1:
            if r4 =='compra':
                return 1
            if r4 == 'venda':
                return 2
            else:
                return 0
        if r2:
            if preco > vwap:
                return 1
            else:
                return 2
        if r3:
            if preco < vwap:
                return 1
            else:
                return 2
        return 0
    def ifr(self,IFR,scompra,svenda,regra):
#         indica compra quando o IFR cruza de baixo para cima o nivel de sobrevendido/inferior
#         indica venda quando o ifr cruza de cima para baixo o nivel sobrecomprado/superior
#         indica compra quando o ifr está abaixo do nivel sobrevendido
#         indica venda quando o ifr está acima do nivel sobrecomprado/superior
        regra_ = self.regra_ifr[regra]
        r1 = True if regra_ == 'cruzamento_ifr'else False
        r2 = 'nada'
        IFR=float(IFR)
        if IFR < svenda:
            self.ifr_compra = True
        if IFR > scompra:
            self.ifr_venda = True
        if IFR > svenda and self.ifr_compra:
            r2 = 'compra'
        if IFR < scompra and self.ifr_venda:
            r2 = 'venda'
        if r1:
            if r2 =='compra':
                return 1
            if r2 == 'venda':
                return 2
            else:
                return 0
        else:
            if IFR > scompra:
                return 2
            if IFR < svenda:
                return 1
            else:
                return 0
    def bands(self,preco,bands_superior,bands_inferior,regra):
        # compra quando o fechamento do candle cruza de baixo para cima a banda inferior
        # venda quando o fechamento do candle cruza de cima para baixo a banda superior
        # compra quando o fechamento do candle está abaixo da banda inferior
        # venda quando o preco está acima da banda superior
        regra_ = self.regra_ifr[regra]
        r1 = True if regra_ == 'cruzamento_bands' else False
        r2 = 'nada'
        preco=float(preco)
        bands_superior=float(bands_superior)
        bands_inferior=float(bands_inferior)
        
        if preco < bands_inferior:
            self.compra = True
        if preco > bands_inferior and self.bands_compra:
            r2 = 'compra'
        if preco > bands_superior:
            self.bands_venda = True
        if preco < bands_superior and self.bands_venda:
            r2 = 'venda'
        if r1:
            if r2 == 'compra':
                return 1
            if r2 == 'venda':
                return 2
            else:
                return 0
        else:
            if preco < bands_inferior:
                return 1
            if preco > bands_superior:
                return 2
            else:
                return 0
    def central_rules(self,action1,action2,action3,action4,action5,mode):
        if mode == 0:
            return action1
        if mode == 1:
            return action2
        if mode == 2:
            return action3
        if mode == 3:
            return action4
        if mode == 4:
            return action5
        if mode == 5:
            if action1 == action2:
                return action1
            else:
                return 0
        if mode == 6:
            if action1 == action3:
                return action1
            else:
                return 0
        if mode == 7:
            if action1 == action4:
                return action1
            else:
                return 0
        if mode == 8:
            if action1 == action5:
                return action1
            else:
                return 0
        if mode == 9:
            if action2 == action3:
                return action3
            else:
                return 0
        if mode == 10:
            if action2 == action4:
                return action4
            else:
                return 0
        if mode == 11:
            if action2 == action5:
                return action2
            else:
                return 0
        if mode == 12:
            if action3 == action4:
                return action2
            else:
                return 0
        if mode == 13:
            if action3 == action5:
                return action3
            else:
                return 0
        if mode == 14:
            if action4 == action5:
                return action3
            else:
                return 0
        if mode == 15:
            if action1 == action2 == action3:
                return action4
            else:
                return 0   
        if mode == 16:
            if action1 == action2 == action4:
                return action1
            else:
                return 0
        if mode == 17:
            if action1 == action2 == action5:
                return action1
            else:
                return 0
        if mode == 18:
            if action1 == action3 == action4:
                return action1
            else:
                return 0
        if mode == 19:
            if action1 == action3 == action5:
                return action1
            else:
                return 0
        if mode == 20:
            if action1 == action4 == action5:
                return action4
            else:
                return 0   
        if mode == 21:
            if action5 == action2 == action4:
                return action1
            else:
                return 0
        if mode == 22:
            if action5 == action2 == action1 == action3:
                return action1
            else:
                return 0

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            