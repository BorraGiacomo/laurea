from pathlib import Path
import importlib
import numpy as np
from fractions import Fraction
from Initializer import Initializer
from utility.SafeArray import SafeArray

def main():
    
    Param = importlib.import_module(f"{getParam()}.Parameters")
    param = Param.Parameters()
    
    init = Initializer(param)
    init.printNashEq(*init.start())

def getParam():
    cartella = Path(__file__).parent.joinpath("parameters")
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
    return "parameters." + scelta

if __name__ == "__main__":
    main()