from utility.SafeArray import SafeArray
import numpy as np

class Parameters:
    
    def __init__(self):
        self.n_roads = 5
        self.n_routes_hat = 2
        self.n_routes_check = 2
        self.variation_hat = SafeArray(np.zeros(self.n_roads))
        self.variation_check = SafeArray(np.zeros(self.n_roads))

    #Percorsi per la popolazione hat
    Gamma_hat = SafeArray([ [1., 0.],
                            [0., 1.],
                            [1., 0.],
                            [0., 0.],
                            [0., 0.]])
    
    #Percorsi per la popolazione check
    Gamma_check = SafeArray([   [0., 0.],
                                [0., 0.],
                                [1., 0.],
                                [1., 0.],
                                [0., 1.]])
    
    
    def tau_hat(self, eta_hat, eta_check):
        """
        Ritorna il costo (tempo di viaggio) delle strade per la popolazione hat

        :param nu_hat: array dove `nu_hat[i]` è il numero di viaggiatori della popolazione hat sulla strada `i+1`
        :param nu_check: array dove `nu_check[i]` è il numero di viaggiatori della popolazione check sulla strada `i+1`
        :return: array di dimensione `n_roads` con il costo (tempo di viaggio) delle strade per la popolazione hat. 
                Se la strada `i+1` non è in widehat{mathcal{N}}, `return[i]` è impostato di base a +infty
        """
        eta_hat_t = eta_hat.flatten()
        eta_check_t = eta_check.flatten()
        return SafeArray([1.+eta_hat_t[0], 3.+eta_hat_t[1], 1.+eta_hat_t[2]+eta_check_t[2], np.inf, np.inf]) + self.variation_hat
    
    def tau_check(self, eta_hat, eta_check):
        """
        Ritorna il costo (tempo di viaggio) delle strade per la popolazione check

        :param nu_hat: array dove `nu_hat[i]` è il numero di viaggiatori della popolazione hat sulla strada `i+1`
        :param nu_check: array dove `nu_check[i]` è il numero di viaggiatori della popolazione check sulla strada `i+1`
        :return: array di dimensione `n_roads` con il costo (tempo di viaggio) delle strade per la popolazione check. 
                Se la strada `i+1` non è in widecheck{mathcal{N}}, `return[i]` è impostato di base a +infty
        """
        eta_hat_t = eta_hat.flatten()
        eta_check_t = eta_check.flatten()
        return SafeArray([np.inf, np.inf, 1.+eta_hat_t[2]+eta_check_t[2], 1.+eta_check_t[3], 3.+eta_check_t[4]]) + self.variation_check