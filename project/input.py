import numpy as np
import importlib
from pathlib import Path
from Computator import Computator

def main():
    Param = importlib.import_module(f"{getParam()}.Parameters")
    
    param = Param.Parameters()
    
    computator = Computator(param)
    
    theta_hat = np.array([[0.25],
                          [0.75]])
    theta_check = np.array([[0.4],
                            [0.6]])
    limit = np.array([[1e-100],
                      [1e-100]])
    
    theta_hat, theta_check = computator.compute(theta_hat, theta_check, limit)
    
    print(theta_hat)
    print(theta_check)
    
    
    
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