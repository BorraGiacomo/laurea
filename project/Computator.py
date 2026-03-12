import numpy as np

class Computator:    
    def __init__(self, parameters):
        self.param = parameters
        self.lmbda = 0.5*np.min(1/self.param.n_routes_hat, 1/self.param.n_routes_check)
        self.one_n_hat = np.ones((self.param.n_routes_hat, 1))
        self.one_n_check = np.ones((self.param.n_routes_check, 1))
    
    
    def T_hat(self, theta_hat, theta_check):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_hat.T @ self.param.tau_hat(nu_hat, nu_check)
    
    def T_check(self, theta_hat, theta_check):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_check.T @ self.param.tau_check(nu_hat, nu_check)
    
    def phi_bar(self, xi):
        """
        Funzione definita per xi appartenente ai reali positivi o per xi=+infinito
        """
        if xi <= 0:
            raise ValueError("phi_bar non definita per valori minori o uguali di 0")
        
        return 1 if xi == float('inf') else xi/(1-xi)
    
    
    """
    Funzione definita per xi appartenente a (R+ U +inf)^n
    Restituisce un array di dimensione n tale che `return[i]==phi_bar(xi[i])`
    """ 
    phi = np.vectorize(phi_bar)
    
    
    def normalize(self, theta):
        """
        Funzione definita per `theta` appartenente a R^n talte che esiste almeno un `theta[i]>0`
        """
        if not np.any(theta != 0):
            raise ValueError("normalize non definita per vettori nulli")
        
        theta_max = np.maximum(theta, 0)
        sum = sum(theta_max)
        return theta_max / sum
    
    def f_hat(self, theta_hat, theta_check):
        composition = self.phi(self.T_hat(theta_hat, theta_check))
        return self.normalize(theta_hat - self.lmbda*(composition - theta_hat.T @ composition @ self.one_n_hat))
    
    def f_check(self, theta_hat, theta_check):
        composition = self.phi(self.T_check(theta_hat, theta_check))
        return self.normalize(theta_check - self.lmbda*(composition - theta_check.T @ composition @ self.one_n_check))