from pathlib import Path
import importlib
from Initializer import Initializer
import re

def main():
    
    Param = importlib.import_module(f"{getParam()}.Parameters")
    param = Param.Parameters()
    
    init = Initializer(param)
    init.start()

def getParam():
    cartella = Path(__file__).parent / "parameters"

    def extract_number(name):
        match = re.search(r'\d+', name)
        return int(match.group()) if match else -1

    parametri = sorted(
        [f.name for f in cartella.iterdir() if f.is_dir() and f.name.startswith("parameters")],
        key=extract_number
    )

    print("\nPacchetti disponibili:")
    for i, nome in enumerate(parametri, 1):
        print(f"{i}) {nome}")

    while True:
        try:
            indice = int(input("\nScegli un pacchetto (numero): ")) - 1
            if 0 <= indice < len(parametri):
                return "parameters." + parametri[indice]
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")

if __name__ == "__main__":
    main()