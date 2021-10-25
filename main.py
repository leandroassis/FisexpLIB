'''
# Universidade Federal do Rio de Janeiro
# Escola Politécnica
# Engenharia Eletrônica e da Computação
# 
# Author: Leandro Assis dos Santos
# Date: 07/04/2021
# 
# Description: Python library to simplify the work while doing an expirement analysis.
#
'''

import getopt
import sys

from utils import *

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["save=", "fit=", "axis_x=", "axisy=", "file=", "name_x=", "name_y=", "unit_x=", "unit_y=", "minimum_x_uncertainty=", "minimum_y_uncertainty=", "plot", "codification=", "separator="])
    except getopt.GetoptError as e:
        print(e)
        print("Usage:")
        print("python3 main.py [options]")
        print("See --help to all option.")
        sys.exit(InvalidOption)
    
    try:
        handleOptions()
    except Exception as e:
        print(e)

    if input_file == 0:
        print("No input file given.")
        sys.exit(NoInputFile)
    if Xaxis == 0 or Yaxis == 0:
        print("No axis content data given.")
        sys.exit(NoAxis)
    
    object = DataAnalysis(input_file, Xaxis, Yaxis, separator, codification)
    average, stdDeviation, nonprop_uncertainty = object.FindParameters()

    print(f"Avarage: {average}\nStandard Deviation: {stdDeviation}\nNon-Propagate Uncertainty: {nonprop_uncertainty}")
    calculate_propuncer = input("Do you would like to calculate the propagated uncertainty? [Y/N]")
    if calculate_propuncer.upper() in ["YES", "Y", "SIM", "S"]:
        print("Sorry, yet we can't do this procediment. Please calculate the propagated uncertainty manually and insert here")
        prop_uncertainty = float(input("Calculated uncertainty: "))
    else:
        print("Proceeding with the Non-Propagated Uncertainty")
        prop_uncertainty = nonprop_uncertainty
    
    if fit_type == "linear":
        coef = object.LinearFit()
        object.Plot(prop_uncertainty, linear_coef=coef)
    else:
        coef = object.ExponentialFit()
        object.Plot(prop_uncertainty, expo_coef=coef)

    if output_file:
        object.Save(prop_uncertainty, average)

if __name__ == '__main__':
    main()