import numpy as np

class Computator:    
    def __init__(self, parameters):
        self.param = parameters
        self.lmbda = 0.5*np.min([1/self.param.n_routes_hat, 1/self.param.n_routes_check])
        self.one_n_hat = np.ones((self.param.n_routes_hat, 1))
        self.one_n_check = np.ones((self.param.n_routes_check, 1))
    
    def compute(self, theta_hat, theta_check, limit):
        prev_hat = np.ones((self.param.n_routes_hat, 1))*np.inf
        prev_check = np.ones((self.param.n_routes_check, 1))*np.inf
        
        count = 0
        
        while np.any(np.abs(theta_hat-prev_hat) > limit) or np.any(np.abs(theta_check-prev_check) > limit):
            prev_hat = theta_hat
            prev_check = theta_check
            
            theta_hat = self.f_hat(theta_hat, theta_check)
            theta_check = self.f_check(theta_hat, theta_check)
            count+=1
        print(count)
        return theta_hat, theta_check
    
    def phi(self, x):
        """
        Funzione φ applicata elemento per elemento:
        - xi = inf → 1
        - altrimenti → xi / (1 - xi)
        Restituisce sempre un array colonna (n,1)
        """
        vectorized = np.vectorize(lambda xi: 1 if xi == np.inf else xi / (1 - xi))
        return vectorized(x).reshape(-1, 1)
    
    def T_hat(self, theta_hat, theta_check):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_hat.T @ self.param.tau_hat(nu_hat, nu_check)
    
    def T_check(self, theta_hat, theta_check):
        nu_hat = self.param.Gamma_hat @ theta_hat

        nu_check = self.param.Gamma_check @ theta_check

        return self.param.Gamma_check.T @ self.param.tau_check(nu_hat, nu_check)
    
    def normalize(self, theta):
        """
        Funzione definita per `theta` appartenente a R^n talte che esiste almeno un `theta[i]>0`

        if not np.any(theta != 0):
            raise ValueError("normalize non definita per vettori nulli")
        """
        theta_max = np.maximum(theta, 0)
        sum = np.sum(theta_max)
        return theta_max / sum
    
    def f_hat(self, theta_hat, theta_check):
        composition = self.phi(self.T_hat(theta_hat, theta_check))
        return self.normalize(theta_hat - self.lmbda*(composition - (theta_hat.T @ composition)[0]*self.one_n_hat))
    
    def f_check(self, theta_hat, theta_check):
        composition = self.phi(self.T_check(theta_hat, theta_check))
        return self.normalize(theta_check - self.lmbda*(composition - (theta_check.T @ composition)[0]*self.one_n_check))