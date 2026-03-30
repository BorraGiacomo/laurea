import numpy as np
from utility.AbstractParam import AbstractParam
from utility.SafeArray import SafeArray
class Computator:    
    def __init__(self, param: AbstractParam):
        self.param = param
        
        self.lmbda = 0.5*np.min([1/self.param.n_routes_hat, 1/self.param.n_routes_check])
        
        #Array colonna di 1 con dimensioni n_routes_hat ed n_routes_check
        self.one_n_hat = SafeArray(np.ones((self.param.n_routes_hat, 1)))
        self.one_n_check = SafeArray(np.ones((self.param.n_routes_check, 1)))
    
    
    def getNashEquilibriaVariation(self, theta_hat, theta_check, limit_hat, limit_check, variation):
        """
            Ritorna l'Equilibrio di Nash variando i costi delle strade selezionate in param di un coefficiente variation, usando come
            punto di partenza theta_hat, theta_check e come limite di precisione limit_hat, limit_check
            :param theta_hat, theta_check: array di dimensione [param.n_routes_hat, 1] e [param.n_routes_check, 1]
            :param limit_hat, limit_check, variation: float
        """
        prev_theta_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*np.inf)
        prev_theta_check = SafeArray(np.ones((self.param.n_routes_check, 1))*np.inf)
        
        count = 0
        
        while np.linalg.norm(theta_hat-prev_theta_hat) > limit_hat or np.linalg.norm(theta_check-prev_theta_check) > limit_check:
            prev_theta_hat[:] = theta_hat
            prev_theta_check[:] = theta_check
            
            theta_hat = self.f_hat(theta_hat, theta_check, variation)
            theta_check = self.f_check(theta_hat, theta_check, variation)
            count+=1
        
        if self.param.show_iterations: print("Iterazioni: " + str(count))
        return theta_hat, theta_check
    
    
    def getNashEquilibria(self, theta_hat, theta_check, limit_hat, limit_check):
        """
            Ritorna l'Equilibrio di Nash usando come costi delle strade i tau delle rispettive popolazioni presenti in param (senza variazioni), usando come
            punto di partenza theta_hat, theta_check e come limite di precisione limit_hat, limit_check
            :param theta_hat, theta_check: array di dimensione [param.n_routes_hat, 1] e [param.n_routes_check, 1]
            :param limit_hat, limit_check: float
        """
        return self.getNashEquilibriaVariation(theta_hat, theta_check, limit_hat, limit_check, 0)
    
    
    def phi(self, x):
        x = np.asarray(x)
        res = np.empty_like(x)

        mask = np.isinf(x)
        res[mask] = 1.
        res[~mask] = x[~mask] / (1. - x[~mask])

        return SafeArray(res.reshape(-1, 1))
    
    
    def T_hat(self, theta_hat, theta_check, variation):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_hat.T @ self.param.tau_hat_variated(nu_hat, nu_check, variation)
    
    
    def T_check(self, theta_hat, theta_check, variation):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_check.T @ self.param.tau_check_variated(nu_hat, nu_check, variation)
    
    
    def normalize(self, theta):
        theta_max = np.maximum(theta, 0)
        sum = np.sum(theta_max)
        return theta_max / sum
    
    
    def f_hat(self, theta_hat, theta_check, variation):
        composition = self.phi(self.T_hat(theta_hat, theta_check, variation))
        return self.normalize(theta_hat - self.lmbda*(composition - (theta_hat.T @ composition)[0]*self.one_n_hat))
    
    
    def f_check(self, theta_hat, theta_check, variation):
        composition = self.phi(self.T_check(theta_hat, theta_check, variation))
        return self.normalize(theta_check - self.lmbda*(composition - (theta_check.T @ composition)[0]*self.one_n_check))
    