import numpy as np
import importlib
from pathlib import Path

def main():
    Param = importlib.import_module(f"{getParam()}.Parameters")
    
    param = Param.Parameters()
    
    #Given theta (distribution of the hat and check population on the routes):
    theta_hat = np.array([1/2, 1/2])
    
    theta_check = np.array([1/2, 1/2])
    
    #Population on each road:
    pop_hat = param.Gamma_hat @ theta_hat.T
    
    pop_check = param.Gamma_check @ theta_check.T
    
    #Travel times for every route
    T_hat = param.tau_hat(pop_hat, pop_check) @ param.Gamma_hat
    T_check = param.tau_check(pop_hat, pop_check) @ param.Gamma_check
    
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