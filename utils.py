import matplotlib.pyplot as plt
from math import log10, floor, pi
import pandas as pd
import scipy.optimize as spopt
import numpy as np
#import statsmodels.api as sm https://stackoverflow.com/questions/26050855/getting-uncertainty-values-in-linear-regression-with-python

fit_type, output_file, export_plot, Xaxis, Yaxis, input_file, Xlabel, Ylabel, Xunit, Yunit, minimum_x_uncertainty, minimum_y_uncertainty = "linear", "saida.csv", True, 0, 0, 0, 0, 0, 0, 0, 0.01, 0.01
separator = ";"
codification = "utf-8"

valid_units = ["s", "ms", "h", "V", "F", "m", "m/s", "m/s²", "km/h", "N/m", "kgf", "Ohms", "uF", "mF", "nF", "dB"]
valid_fits = ["linear", "exponencial"]

#   Definição de erros
InvalidOption = 2
InvalidUnit = 3
InvalidFit = 4
InvalidUncertainty = 5
NoInputFile = 6
NoAxis = 7


def handleOptions(opts):
    global fit_type, output_file, export_plot, Xaxis, Yaxis, input_file, Xlabel, Ylabel, Xunit, Yunit, minimum_x_uncertainty, minimum_y_uncertainty, separator, codification

    for o, a in opts:
        if o == "--fit":
            if a in valid_fits:
                fit_type = a
            else:
                raise InvalidFit
        elif o == "--save":
            output_file = a
        elif o == "--plot":
            export_plot = True
        elif o == "--axis_x":
            Xaxis = a
        elif o == "--axis_y":
            Yaxis = a
        elif o == "--file":
            input_file = a
        elif o == "--name_x":
            Xlabel = a
        elif o == "--name_y":
            Ylabel = a
        elif o == "--unit_x":
            if a in valid_units:
                Xunit = a
            else:
                raise InvalidUnit
        elif o == "--unit_y":
            if a in valid_units:
                Yunit = a
            else:
                raise InvalidUnit
        elif o == "--minimum_x_uncertainty":
            if type(a) == float:
                minimum_x_uncertainty = a
            else: 
                raise InvalidUncertainty
        elif o == "--minimum_y_uncertainty":
            if type(a) == float:
                minimum_y_uncertainty = a
            else:
                raise InvalidUncertainty
        elif o == "--separator":
            separator = a
        elif o == "--codification":
            codification = a

def LinearFit(L, a, b):
    return a*L+b

def ExponentialFit(x, a, b, c , d):
    return a*np.exp(b-c*x)+d

class DataAnalysis():
    def __init__(self, file, X, Y, separator, codification):
        self.data = pd.read_csv(file, separator=separator, encoding=codification)
        self.Xmeasure = self.data[X]
        self.Ymeasure = self.data[Y]

    def FindParameters(self):
        average = self.Xmeasure.mean()
        standardDeviation = self.Xmeasure.std()
        return average, standardDeviation, standardDeviation/len(self.data.index)
    
    '''
        def PropagacaodeIncerteza(self):
        self.incertezapropagada = (self.tempomedio*self.incerteza)/(2*pi**2)
        self.incertezapropagada = self.ArredondarAlgaritmosSignificativos(self.incertezapropagada)
    '''
    
    def LinearFit(self):
        popt, pcov = spopt.curve_fit(LinearFit, self.Xmeasure, self.Ymeasure)
        return popt
    
    def ExponentialFit(self):
        popt, pcov = spopt.curve_fit(ExponentialFit, self.Xmeasure, self.Ymeasure)
        return popt
    
    def Plot(self, uncertainty, expo_coef, linear_coef):
        plt.figure(figsize=(8,5))
        plt.xlabel(Xlabel, fontsize=17)
        plt.ylabel(Ylabel, fontsize=17)
        
        plt.errorbar(self.Xmeasure, self.Ymeasure, yerr = uncertainty, fmt='o',
                    mfc='black', markeredgecolor='black', markersize=5, ecolor="black", capsize=8)
        if linear_coef:
            Y = [linear_coef[0]*L+linear_coef[1] for L in self.Xmeasure]
        elif expo_coef:
            Y = [expo_coef[0]*np.exp(expo_coef[1]-expo_coef[2]*x)+expo_coef[3] for x in self.Xmeasure]
        plt.plot(self.Xmeasure, Y, color="red")
        if export_plot:
            plt.savefig("GRAFICO.jpeg", dpi=600)
            print("Close the open plot to continue...")
            plt.show()
        plt.close()
    
    def Save(self, uncertainty, average):
        self.data["Incerteza"] = uncertainty
        self.data["Media"] = average

        self.data.to_csv(output_file)

    