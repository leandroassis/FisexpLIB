'''
# Universidade Federal do Rio de Janeiro
# Escola Politécnica
# Engenharia Eletrônica e da Computação
# 
# Autor: Leandro Assis dos Santos
# DRE: 120032476
# Data: 07/04/2021
# 
# Descrição: Script para fazer a análise de dados dos experimentos de Fisexp II
#
'''

import matplotlib.pyplot as plt
from math import log10, floor, pi
import scipy.optimize as spopt

incerteza_minima_tempo = 0.01
incerteza_minima_tamanho = 0.1

def FuncaodeAjuste(L, a, b):
    if type(L) == list:
        y = []
        for x in L:
            y.append(a*x + b)
        return y
    return a*L+b

class AnalisedeDados():
    def __init__(self, dadosmedidos):
        self.medicao = dadosmedidos

    def ArredondarAlgaritmosSignificativos(self, numero): 
        return round(numero, -int(floor(log10(abs(numero)))))

    def TempoMediodaMedicao(self):
        self.tempomedio = round((sum(self.medicao)- self.medicao[0])/(len(self.medicao)-1),2)

    def IncertezaDaMedida(self):
        desviopadrao = 0
        for indice in range(len(self.medicao)):
            if indice == 0:
                continue
            desviopadrao += (self.medicao[indice] - self.tempomedio)**2
        desviopadrao = (desviopadrao/(len(self.medicao)-2))**0.5
        incertezadamedida = desviopadrao/(len(self.medicao)-1)**0.5
        self.incerteza = self.ArredondarAlgaritmosSignificativos(incertezadamedida)
        self.CompararIncerteza("tempo")

    def CompararIncerteza(self, grandeza):
        if grandeza in ["tamanho", "distancia", "cm", "m", "comprimento"]:
            if self.incerteza <= incerteza_minima_tamanho:
                self.incerteza = incerteza_minima_tamanho
        elif grandeza in ["tempo", "s", "duracao"]:
            if self.incerteza <= incerteza_minima_tempo:
                self.incerteza = incerteza_minima_tempo

    def PropagacaodeIncerteza(self):
        self.incertezapropagada = (self.tempomedio*self.incerteza)/(2*pi**2)
        self.incertezapropagada = self.ArredondarAlgaritmosSignificativos(self.incertezapropagada)

    def AjustarMedidacomIncerteza(self, tempo):
        incertezastr = str(self.incertezapropagada)
        contador = 0
        for caracter in incertezastr:
            if caracter == ".":
                contador+=1
            if contador != 0:
                contador+=1
        casasdecimaisincerteza = contador-2
        tempo = round(tempo, casasdecimaisincerteza)
        return tempo

    def RealizaAjusteLinear(self, dadosX, dadosY):
        popt, pcov = spopt.curve_fit(FuncaodeAjuste, dadosX, dadosY)
        print(popt)
        return popt
    
    def CriaGrafico(self, dadosX, dadosY, incertezadosdados, nomefigura):
        plt.figure(figsize=(8,5))
        plt.errorbar(dadosX, dadosY, yerr = incertezadosdados, fmt='o',
                     mfc='black', markeredgecolor='black', markersize=5, ecolor="black", capsize=8)
        coef = self.RealizaAjusteLinear(dadosX, dadosY)
        plt.plot(dadosX, FuncaodeAjuste(dadosX, coef[0], coef[1]), color="red")
        plt.title("Tempo de Oscilação por Comprimento", fontsize = 20)
        plt.xlabel("Comprimento (L)", fontsize=17)
        plt.ylabel("T²/4π²", fontsize=17)
        plt.savefig(nomefigura, dpi=600)
        plt.close()

    def ExecutarProcedimento(self):
        self.TempoMediodaMedicao()
        self.IncertezaDaMedida()
        self.PropagacaodeIncerteza()
        return self.tempomedio, self.incertezapropagada
    
