from pathlib import Path
import importlib
import numpy as np
from fractions import Fraction
from Initializer import Initializer
from utility.SafeArray import SafeArray
import matplotlib.pyplot as plt

def main():
    np.seterr(divide='ignore')
    Param = importlib.import_module(f"{getParam()}.Parameters")
    param = Param.Parameters()
    
    indice = None
    while True:
        try:
            indice = int(input("Scegli operazione:\n1)Calcolo equilibrio di Nash\n2)Grafico con variazione delle strade\n>"))
            if 1 <= indice <= 2:
                break
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")
    
    match indice:
        case 1:
            eqNash(param)
        case 2:
            graphVariations(param)
        case _:
            return
       
def eqNash(param):
    init = Initializer(param)
    theta_hat, theta_check, T_hat, T_check = init.getNashEquilibria()
    
    vec_frac = np.vectorize(lambda x: str(Fraction(x).limit_denominator(1000000)))
    
    print("Equilibrio di Nash:")
    print("theta_hat:\n", str(vec_frac(theta_hat)).replace("'", ""))
    print("theta_check:\n", str(vec_frac(theta_check)).replace("'", ""))
    
    print()
    
    print("Tempi di attraversamento dei percorsi:")
    print("T_hat:\n", str(vec_frac(T_hat)).replace("'", ""))
    print("T_check:\n", str(vec_frac(T_check)).replace("'", ""))
    
def graphVariations(param):
    MAX = getMaxVariation()
    step = getDeltaVariation()
    variation_values = np.arange(0, MAX+step, step)
    N = len(variation_values)

    time_of_travel_hat = np.zeros(N)
    time_of_travel_check = np.zeros(N)

    variation_hat, variation_check = getVariationFormat(param)
    init = Initializer(param)
    
    for idx, i in enumerate(variation_values):
        theta_hat, theta_check, T_hat, T_check = init.getNashEquilibria()
        index_hat = np.argmax(theta_hat > 0)
        index_check = np.argmax(theta_check > 0)
        
        time_of_travel_hat[idx] = T_hat[index_hat]
        time_of_travel_check[idx] = T_check[index_check]
        
        param.variation_hat = variation_hat*i
        param.variation_check = variation_check*i
        init.setParameters(param)
    
    plt.plot(variation_values, time_of_travel_hat, label='Hat', color='blue')
    plt.plot(variation_values, time_of_travel_check, label='Check', color='red')
    plt.xlabel('Variazione del tempo di viaggio')
    plt.ylabel('Tempo di viaggio')
    plt.title('Tempo di viaggio in funzione della variazione')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def getMaxVariation():
    scelta = None
    while scelta is None:
        try:
            scelta = float(input("Scegli variazione massima del tempo di viaggio della strada\n>"))
        except ValueError:
            print("Inserisci un numero valido.")
    return scelta

def getDeltaVariation():
    scelta = None
    while scelta is None:
        try:
            scelta = float(input("Scegli passo di variazione del tempo di viaggio della strada\n>"))
        except ValueError:
            print("Inserisci un numero valido.")
    return scelta
    
def getVariationFormat(param):
    indice = None
    while indice is None:
        try:
            scelta = int(input("Scegli la strada che varierà (numero da 1 a "+ str(param.n_roads) +")\n>"))
            if 1 <= scelta <= param.n_roads:
                indice = scelta-1
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")

    scelta = None
    while True:
        try:
            scelta = int(input("Scegli opzione:\n1)Varia solo per hat\n2)Varia solo per check\n3)Varia per entrambi\n>"))
            if 1 <= scelta <= 3:
                break
            else:
                print("Numero non valido. Riprova.")
        except ValueError:
            print("Inserisci un numero valido.")
    
    variation_hat = SafeArray(np.zeros(param.n_roads))
    variation_check = SafeArray(np.zeros(param.n_roads))
    
    match scelta:
        case 1:
            variation_hat[indice] = 1
            return variation_hat, variation_check
        case 2:
            variation_check[indice] = 1
            return variation_hat, variation_check
        case 3:
            variation_hat[indice] = 1
            variation_check[indice] = 1
            return variation_hat, variation_check
        case _:
            return variation_hat, variation_check


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