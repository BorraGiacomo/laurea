from utility.SafeArray import SafeArray
import importlib
from pathlib import Path
from Computator import Computator
import numpy as np



def main():
    np.seterr(divide='ignore')
    Param = importlib.import_module(f"{getParam()}.Parameters")
    
    param = Param.Parameters()
    
    computator = Computator(param)
    
    theta_hat = SafeArray([[0.5],
                          [0.5]])
    theta_check = SafeArray([[0.5],
                            [0.5]])
    limit = SafeArray([[1.e-20],
                      [1.e-20]])
    
    theta_hat, theta_check = computator.compute(theta_hat, theta_check, limit)
    
    print("Equilibrio di Nash:")
    print("theta_hat:\n", theta_hat)
    print("theta_check:\n", theta_check)
    
    #Popolazione su ogni strada:
    nu_hat = param.Gamma_hat @ theta_hat
    
    nu_check = param.Gamma_check @ theta_check
    
    #Tempi di viaggio su ogni strada:
    T_hat = param.Gamma_hat.T @ param.tau_hat(nu_hat, nu_check)
    T_check = param.Gamma_check.T @ param.tau_check(nu_hat, nu_check)
    
    print("Tempi di attraversamento dei percorsi:")
    print("T_hat:\n", T_hat)
    print("T_check:\n", T_check)
    
    
def getParam():
    cartella = Path(__file__).parent
    parametri = [f.name for f in cartella.iterdir() if f.is_dir() and f.name.startswith("parameters")]
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