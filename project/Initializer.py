from utility.SafeArray import SafeArray
from Computator import Computator
import numpy as np

class Initializer:
    def __init__(self, param):
        self.param = param
        self.computator = Computator(self.param)
        self.initial_theta_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*(1/self.param.n_routes_hat))
        self.initial_theta_check = SafeArray(np.ones((self.param.n_routes_check, 1))*(1/self.param.n_routes_check))
        self.limit_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*1e-11)
        self.limit_check = SafeArray(np.ones((self.param.n_routes_check, 1))*1e-11)

    def getNashEquilibria(self):
        #Equilibrio di Nash:    
        theta_hat, theta_check = self.computator.getNashEquilibria(self.initial_theta_hat, self.initial_theta_check, self.limit_hat, self.limit_check)
        
        #Tempi di viaggio su ogni strada:
        T_hat = self.computator.T_hat(theta_hat, theta_check)
        T_check = self.computator.T_check(theta_hat, theta_check)
        
        return theta_hat, theta_check, T_hat, T_check
    
    def setParameters(self, param):
        self.param = param
        self.computator = Computator(self.param)
        self.initial_theta_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*(1/self.param.n_routes_hat))
        self.initial_theta_check = SafeArray(np.ones((self.param.n_routes_check, 1))*(1/self.param.n_routes_check))
        self.limit_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*1e-11)
        self.limit_check = SafeArray(np.ones((self.param.n_routes_check, 1))*1e-11)
        
        