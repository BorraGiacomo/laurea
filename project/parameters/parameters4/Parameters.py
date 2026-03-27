from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation

class Parameters:
    
    def __init__(self):
        self.n_roads = 6
        self.n_routes_hat = 3
        self.n_routes_check = 2
        
        self.operation = Operation.NASH_EQ
        
        self.show_result = False
        self.print_as_fraction = True
        
        self.MIN = 0
        self.MAX = 0.5
        self.step = 0.01

    #Percorsi per la popolazione hat
    Gamma_hat = SafeArray([ [1., 0., 0.],
                            [0., 1., 0.],
                            [0., 0., 0.],
                            [0., 0., 1.],
                            [0., 1., 0.],
                            [0., 0., 1.]])
    
    #Percorsi per la popolazione check
    Gamma_check = SafeArray([   [0., 0.],
                                [0., 0.],
                                [1., 0.],
                                [0., 1.],
                                [1., 0.],
                                [0., 0.]])
    
    variation_hat = SafeArray([0., 0., 0., 0., 0., 1.])
    
    variation_check = SafeArray([0., 0., 0., 0., 0., 0.])
    
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
        return SafeArray([4., 1.+eta_hat_t[1], np.inf, 5.*eta_hat_t[3]+5.*eta_check_t[3], 1.+eta_hat_t[4]+eta_check_t[4], 1])
    
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
        return SafeArray([np.inf, np.inf, eta_check_t[2], 5.*eta_hat_t[3]+5.*eta_check_t[3], 1.+eta_hat_t[4]+eta_check_t[4], np.inf])
    
    def tau_hat_variated(self, eta_hat, eta_check, variation):
        return self.tau_hat(eta_hat, eta_check) + self.variation_hat*variation
    
    def tau_check_variated(self, eta_hat, eta_check, variation):
        return self.tau_check(eta_hat, eta_check) + self.variation_check*variation