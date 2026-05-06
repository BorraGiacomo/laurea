from abc import ABC, abstractmethod
from utility.SafeArray import SafeArray
from utility.Operations import Operations
import numpy as np
from typing import final


class AbstractParam(ABC):
    """
    Contratto obbligatorio per i Parametri.
    Definisce struttura, matrici e funzioni di costo per modelli di traffico.
    """
    
    

    # ===== PARAMETRI BASE =====
    
    @property
    @final
    def n_roads(self) -> int:
        """
        Numero totale di strade del grafo.
        
        Returns:
            int: numero di righe di Gamma_hat (una per ogni strada)
        """
        return self.Gamma_hat.shape[0]

    @property
    @final
    def n_routes_hat(self) -> int:
        """
        Numero di percorsi disponibili per la popolazione hat.
        
        Returns:
            int: numero di colonne di Gamma_hat
        """
        return self.Gamma_hat.shape[1]

    @property
    @final
    def n_routes_check(self) -> int:
        """
        Numero di percorsi disponibili per la popolazione check.
        
        Returns:
            int: numero di colonne di Gamma_check
        """
        return self.Gamma_check.shape[1]

    @property
    @abstractmethod
    def operation(self) -> Operations:
        """
        Tipo di operazione da eseguire (es. Nash equilibrium).
        
        Returns:
            Operation: tipo di operazione
        """
        pass

    @property
    @abstractmethod
    def output_directory(self) -> str:
        """
        Directory dove salvare i risultati.
        
        Returns:
            str: percorso della directory di output
        """
        pass

    @property
    def save_result(self) -> bool:
        """
        Indica se salvare i risultati su file.
        
        Returns:
            bool: True se i risultati devono essere salvati
        """
        return True
    
    @property
    def show_iterations(self) -> bool:
        """
        Indica se mostrare le iterazioni durante il calcolo.
        
        Returns:
            bool: True se si vogliono stampare a terminale le iterazioni
        """
        return True

    @property
    def save_as_fraction(self) -> bool:
        """
        Indica se salvare i valori come frazioni.
        Utilizzato solo nel caso in cui self.operation==Operation.NASH_EQ
        
        Returns:
            bool: True se i numeri devono essere convertiti in frazioni
        """
        return True

    @property
    def MIN(self) -> float:
        """
        Valore minimo della variazione nei grafici.
        
        Returns:
            float: limite inferiore
        """
        return 0.

    @property
    def MAX(self) -> float:
        """
        Valore massimo della variazione nei grafici.
        
        Returns:
            float: limite superiore
        """
        return 1.

    @property
    def step(self) -> float:
        """
        Passo della variazione nei grafici.
        
        Returns:
            float: incremento della variazione
        """
        return 0.01
    
    @property
    def entity_number_hat(self) -> float:
        """
        Numero totale di entità nella popolazione hat.
        Nel caso in cui self.operation==Operation.NASH_EQ_POP_VARIATIONS, viene
        utilizzato solo se self.variate_pop_hat==False
        
        Returns:
            float: numero di entità hat
        """
        return 1.
    
    @property
    def entity_number_check(self) -> float:
        """
        Numero totale di entità nella popolazione check. 
        Nel caso in cui self.operation==Operation.NASH_EQ_POP_VARIATIONS, viene
        utilizzato solo se self.variate_pop_check==False
                
        Returns:
            float: numero di entità check
        """
        return 1.
    
    @property
    def variation_coefficient_pop_hat(self) -> float:
        """
        Indica il coefficiente di variazione del numero di entità della popolazione hat durante il calcolo,
        nel caso in cui self.operation==Operation.NASH_EQ_POP_VARIATIONS
        
        Returns:
            float: coefficiente di variazione della popolazione hat
        """
        return 1.
    
    @property
    def variation_coefficient_pop_check(self) -> float:
        """
        Indica il coefficiente di variazione del numero di entità della popolazione check durante il calcolo,
        nel caso in cui self.operation==Operation.NASH_EQ_POP_VARIATIONS
        
        Returns:
            float: coefficiente di variazione della popolazione check
        """
        return 1.
    
    

    # ===== MATRICI =====
    
    @property
    @abstractmethod
    def Gamma_hat(self) -> SafeArray:
        """
        Matrice dei percorsi per la popolazione hat.
        
        Returns:
            SafeArray: matrice (n_roads x n_routes_hat)
        """
        pass

    @property
    @abstractmethod
    def Gamma_check(self) -> SafeArray:
        """
        Matrice dei percorsi per la popolazione check.
        
        Returns:
            SafeArray: matrice (n_roads x n_routes_check)
        """
        pass

    @property
    def variation_hat(self) -> SafeArray:
        """
            Ritorna array di dimensione (*@$N$@*), i cui elementi sono 1 o 0:
                - 'return[i]'!=0: se viene utilizzata una variazione, i costi della strada 'i' variano per la popolazione (*@$\textit{check}$@*) di un coefficiente 'return[i]', maggiore o minore di 0
                - 'return[i]'==0: se viene utilizzata una variazione, i costi della strada 'i' non variano per la popolazione (*@$\textit{hat}$@*)
        """
        return SafeArray(np.zeros(self.n_roads))

    @property
    def variation_check(self) -> SafeArray:
        """
            Ritorna array di dimensione (*@$N$@*), i cui elementi sono:
                - 'return[i]'!=0: se viene utilizzata una variazione, i costi della strada 'i' variano per la popolazione (*@$\textit{check}$@*) di un coefficiente 'return[i]', maggiore o minore di 0
                - 'return[i]'==0: se viene utilizzata una variazione, i costi della strada 'i' non variano per la popolazione (*@$\textit{check}$@*)
        """
        return SafeArray(np.zeros(self.n_roads))



    # ===== COSTI =====
    
    @abstractmethod
    def tau_hat(self, eta_hat, eta_check) -> SafeArray:
        """
        Calcola il costo (tempo di viaggio) per la popolazione hat.
        
        Args:
            eta_hat: entità hat presenti su ogni strada
            eta_check: entità check presenti su ogni strada
        
        Returns:
            SafeArray: costo per ogni strada (dimensione n_roads)
        """
        pass

    @abstractmethod
    def tau_check(self, eta_hat, eta_check) -> SafeArray:
        """
        Calcola il costo (tempo di viaggio) per la popolazione check.
        
        Args:
            eta_hat: entità hat presenti su ogni strada
            eta_check: entità check presenti su ogni strada
        
        Returns:
            SafeArray: costo per ogni strada (dimensione n_roads)
        """
        pass
    
    @final
    def tau_hat_variated(self, eta_hat, eta_check, variation) -> SafeArray:
        """
        Calcola il costo per la popolazione hat includendo una variazione lineare.
        
        Il costo restituito è:
            tau_hat + variation_hat * variation
        
        Args:
            eta_hat: entità hat presenti su ogni strada
            eta_check: entità check presenti su ogni strada
            variation: coefficiente scalare di variazione
        
        Returns:
            SafeArray: costo modificato per ogni strada
        """
        return self.tau_hat(eta_hat, eta_check) + self.variation_hat * variation

    @final
    def tau_check_variated(self, eta_hat, eta_check, variation) -> SafeArray:
        """
        Calcola il costo per la popolazione check includendo una variazione lineare.
        
        Il costo restituito è:
            tau_check + variation_check * variation
        
        Args:
            eta_hat: entità hat presenti su ogni strada
            eta_check: entità check presenti su ogni strada
            variation: coefficiente scalare di variazione
        
        Returns:
            SafeArray: costo modificato per ogni strada
        """
        return self.tau_check(eta_hat, eta_check) + self.variation_check * variation