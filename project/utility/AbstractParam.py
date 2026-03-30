from abc import ABC, abstractmethod
from utility.SafeArray import SafeArray
from utility.Operation import Operation

class AbstractParam(ABC):
    """
    Contratto obbligatorio per i Parametri
    """

    # ===== PARAMETRI BASE =====
    
    @property
    @abstractmethod
    def n_roads(self) -> int:
        pass

    @property
    @abstractmethod
    def n_routes_hat(self) -> int:
        pass

    @property
    @abstractmethod
    def n_routes_check(self) -> int:
        pass

    @property
    @abstractmethod
    def operation(self) -> Operation:
        pass

    @property
    def show_result(self) -> bool:
        return False
    
    @property
    def show_iterations(self) -> bool:
        return True

    @property
    def print_as_fraction(self) -> bool:
        return False

    #Valore minimo della variazione mostrato nel grafico
    @property
    def MIN(self) -> float:
        return 0

    #Valore massimo della variazione mostrato nel grafico
    @property
    def MAX(self) -> float:
        return 1

    #Step della variazione usato nel grafico
    @property
    def step(self) -> float:
        return 0.01



    # ===== MATRICI =====
    
    #Percorsi per la popolazione hat
    @property
    @abstractmethod
    def Gamma_hat(self) -> SafeArray:
        pass

    #Percorsi per la popolazione check
    @property
    @abstractmethod
    def Gamma_check(self) -> SafeArray:
        pass

    #Strade i cui costi variano per la popolazione hat
    @property
    @abstractmethod
    def variation_hat(self) -> SafeArray:
        pass

    #Strade i cui costi variano per la popolazione check
    @property
    @abstractmethod
    def variation_check(self) -> SafeArray:
        pass



    # ===== COSTI =====
    
    @abstractmethod
    def tau_hat(self, eta_hat, eta_check) -> SafeArray:
        """
        Ritorna il costo (tempo di viaggio) delle strade per la popolazione hat

        :param eta_hat: array dove 'eta_hat[i, 0]' è il numero di viaggiatori della popolazione hat sulla strada 'i+1'
        :param eta_check: array dove 'eta_check[i, 0]' è il numero di viaggiatori della popolazione check sulla strada 'i+1'
        :return: array di dimensione 'n_roads' con il costo (tempo di viaggio) delle strade per la popolazione hat. 
                Se la strada 'i+1' non è in widehat{mathcal{N}}, 'return[i]' è impostato di base a +infty
        """
        pass

    @abstractmethod
    def tau_check(self, eta_hat, eta_check) -> SafeArray:
        """
        Ritorna il costo (tempo di viaggio) delle strade per la popolazione check

        :param eta_hat: array dove 'eta_hat[i, 0]' è il numero di viaggiatori della popolazione hat sulla strada 'i+1'
        :param eta_check: array dove 'eta_check[i, 0]' è il numero di viaggiatori della popolazione check sulla strada 'i+1'
        :return: array di dimensione 'n_roads' con il costo (tempo di viaggio) delle strade per la popolazione check. 
                Se la strada 'i+1' non è in widecheck{mathcal{N}}, 'return[i]' è impostato di base a +infty
        """
        pass
    
    
    def tau_hat_variated(self, eta_hat, eta_check, variation) -> SafeArray:
        """
            Ritorna il costo (tempo di viaggio) delle strade per la popolazione hat sommandovi la variazione per le strade indicate in variation_hat
            
            :param eta_hat: array dove 'eta_hat[i, 0]' è il numero di viaggiatori della popolazione hat sulla strada 'i+1'
            :param eta_check: array dove 'eta_check[i, 0]' è il numero di viaggiatori della popolazione check sulla strada 'i+1'
            :param variation: float che rappresenta il coefficiente di variazione della strada
            :return: array di dimensione 'n_roads' con il costo (tempo di viaggio) delle strade per la popolazione hat a cui è stato
                    sommato variation_hat*variation
                    Se la strada 'i+1' non è in widehat{mathcal{N}}, 'return[i]' è impostato di base a +infty
        """
        return self.tau_hat(eta_hat, eta_check) + self.variation_hat * variation

    def tau_check_variated(self, eta_hat, eta_check, variation) -> SafeArray:
        """
            Ritorna il costo (tempo di viaggio) delle strade per la popolazione check sommandovi la variazione per le strade indicate in variation_check
            
            :param eta_hat: array dove 'eta_hat[i, 0]' è il numero di viaggiatori della popolazione hat sulla strada 'i+1'
            :param eta_check: array dove 'eta_check[i, 0]' è il numero di viaggiatori della popolazione check sulla strada 'i+1'
            :param variation: float che rappresenta il coefficiente di variazione della strada
            :return: array di dimensione 'n_roads' con il costo (tempo di viaggio) delle strade per la popolazione check a cui è stato
                    sommato variation_check*variation
                    Se la strada 'i+1' non è in widecheck{mathcal{N}}, 'return[i]' è impostato di base a +infty
        """
        return self.tau_check(eta_hat, eta_check) + self.variation_check * variation