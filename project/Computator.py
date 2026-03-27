import numpy as np
from utility.SafeArray import SafeArray
class Computator:    
    def __init__(self, param):
        self.param = param
        self.lmbda = 0.5*np.min([1/self.param.n_routes_hat, 1/self.param.n_routes_check])
        self.one_n_hat = SafeArray(np.ones((self.param.n_routes_hat, 1)))
        self.one_n_check = SafeArray(np.ones((self.param.n_routes_check, 1)))
    
    def getNashEquilibriaVariation(self, theta_hat, theta_check, limit_hat, limit_check, variation):
        prev_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*np.inf)
        prev_check = SafeArray(np.ones((self.param.n_routes_check, 1))*np.inf)
        
        count = 0
        
        while np.any(np.abs(theta_hat-prev_hat) > limit_hat) or np.any(np.abs(theta_check-prev_check) > limit_check):
            prev_hat = theta_hat.copy()
            prev_check = theta_check.copy()
            
            theta_hat = self.f_hat(theta_hat, theta_check, variation)
            theta_check = self.f_check(theta_hat, theta_check, variation)
            count+=1
        print("Iterazioni: " + str(count))
        return theta_hat, theta_check
    
    def getNashEquilibria(self, theta_hat, theta_check, limit_hat, limit_check):
        return self.getNashEquilibriaVariation(theta_hat, theta_check, limit_hat, limit_check, 0)
    
    def phi(self, x):
        """
        Funzione bar{varphi} applicata elemento per elemento:
        - xi = inf → 1
        - altrimenti → xi / (1 - xi)
        Restituisce sempre un array colonna (n,1)
        """
        vectorized = np.vectorize(lambda xi: 1. if xi == np.inf else xi / (1. - xi))
        return SafeArray(vectorized(x).reshape(-1, 1))
    
    def T_hat(self, theta_hat, theta_check, variation):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_hat.T @ self.param.tau_hat_variated(nu_hat, nu_check, variation)
    
    def T_check(self, theta_hat, theta_check, variation):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_check.T @ self.param.tau_check_variated(nu_hat, nu_check, variation)
    
    def normalize(self, theta):
        """
        Funzione definita per `theta` appartenente a R^n talte che esiste almeno un `theta[i]>0`

        if not np.any(theta != 0):
            raise ValueError("normalize non definita per vettori nulli")
        """
        theta_max = np.maximum(theta, 0)
        sum = np.sum(theta_max)
        return theta_max / sum
    
    def f_hat(self, theta_hat, theta_check, variation):
        composition = self.phi(self.T_hat(theta_hat, theta_check, variation))
        return self.normalize(theta_hat - self.lmbda*(composition - (theta_hat.T @ composition)[0]*self.one_n_hat))
    
    def f_check(self, theta_hat, theta_check, variation):
        composition = self.phi(self.T_check(theta_hat, theta_check, variation))
        return self.normalize(theta_check - self.lmbda*(composition - (theta_check.T @ composition)[0]*self.one_n_check))
    