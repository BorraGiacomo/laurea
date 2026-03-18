import numpy as np
from utility.SafeArray import SafeArray
import importlib
from pathlib import Path

def main():
    Param = importlib.import_module(f"{getParam()}.Parameters")
    
    param = Param.Parameters()
    
    #Given theta (distribution of the hat and check population on the routes):
    theta_hat = SafeArray([[1/2],
                          [1/2]])
    
    theta_check = SafeArray([[0],
                            [1]])
    
    #Population on each road:
    nu_hat = param.Gamma_hat @ theta_hat
    
    nu_check = param.Gamma_check @ theta_check
    
    #Travel times for every route
    T_hat = param.Gamma_hat.T @ param.tau_hat(nu_hat, nu_check)
    T_check = param.Gamma_check.T @ param.tau_check(nu_hat, nu_check)
    
    print(T_hat)
    print(T_check)
    
def getParam():
    cartella = Path(__file__).parent
    parametri = [f.name for f in cartella.iterdir() if f.is_dir and f.name.startswith("parameters")]
    print(parametri)
    
    scelta = None
    while scelta is None:
        try:
            indice = int(input("Scegli un pacchetto (numero): ")) - 1
            if 0 <= indice < len(parametri):
                scelta = parametri[indice]
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")
    return scelta

if __name__ == "__main__":
    main()