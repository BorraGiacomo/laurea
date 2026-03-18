from utility.SafeArray import SafeArray
import numpy as np
class Parameters:
    
    
    n_roads = 7
    n_routes_hat = 2
    n_routes_check = 2

    #Percorsi per la popolazione hat
    Gamma_hat = SafeArray([ [0., 1.],
                            [1., 0.],
                            [0., 0.],
                            [0., 0.],
                            [1., 0.],
                            [0., 0.],
                            [1., 0.]])
    
    #Percorsi per la popolazione check
    Gamma_check = SafeArray([   [0., 0.],
                                [0., 0.],
                                [1., 0.],
                                [0., 1.],
                                [1., 0.],
                                [1., 0.],
                                [0., 0.]])  
    
    
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
        return SafeArray([5/2+eta_hat_t[0], 1, np.inf, np.inf, (eta_hat_t[4]+eta_check_t[4])/(1-(eta_hat_t[4]+eta_check_t[4])), np.inf, 1])
    
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
        return SafeArray([np.inf, np.inf, 1, 2+eta_check_t[3], (eta_hat_t[4]+eta_check_t[4])/(1-(eta_hat_t[4]+eta_check_t[4])), 1, np.inf])