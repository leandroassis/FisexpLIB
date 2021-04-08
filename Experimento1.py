import fisexplib
from math import pi

medicoescomlimao = [[103, 8.08, 8.06, 8, 8.06, 8.11, 8, 8.06, 7.95, 7.86, 8], [96, 7.8, 7.85, 7.92, 7.73, 7.74, 7.46, 7.87, 7.68, 7.68, 7.8],\
           [71, 6.56, 6.69, 6.57, 6.67, 6.75, 6.62, 6.55, 6.75, 6.7, 6.7], [66.5, 6.37, 6.43, 6.5, 6.37, 6.51, 6.36, 6.36, 6.58, 6.63, 6.5],\
           [54, 5.9, 5.78, 5.84, 5.9, 5.84, 5.83, 6.17, 5.91, 5.89, 5.9]]

medicoescompingpong = [[62, 6.46, 6.24, 6.29, 6.29, 6.43, 6.49, 6.54, 6.35, 6.42, 6.2], [55.5, 5.98, 5.77,5.84, 5.65, 5.59, 5.65, 5.9, 5.85, 5.72, 5.78],\
                      [47, 5.15, 5.36, 5.2, 4.38, 5.24, 5.31, 5.31, 5.18, 5.45, 5.19], [30, 4.89, 4.67, 5.06, 4.33, 4.6, 4.66, 4.27, 4.75, 4.6, 4.32],\
                      [20, 3.49, 3.49, 3.48, 4.15, 3.50, 3.85, 3.48, 3.36, 3.48, 3.65]]

medicaoextra = [[38.3, 5, 4.92, 5.06, 5, 5, 5.13, 5, 5, 5.06, 5.06]]

def recolheDados(conjuntodemedicoes, nomefigura):
    tempos, incertezas, comprimentos = [],[],[]
    for medicao in conjuntodemedicoes:
        func = fisexplib.AnalisedeDados(medicao)
        tempomedio, incerteza = func.ExecutarProcedimento()
        tempomedio = (tempomedio**2)/(4*pi**2)
        tempomedio = func.AjustarMedidacomIncerteza(tempomedio)
        tempos.append(tempomedio)
        incertezas.append(incerteza)
        comprimentos.append(medicao[0])
    func.CriaGrafico(comprimentos, tempos, incertezas, nomefigura)
    print(tempos, incertezas, comprimentos)

recolheDados(medicoescomlimao, "Figura1")


recolheDados(medicoescompingpong, "Figura2")





