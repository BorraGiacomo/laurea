import numpy as np

class Parameters:
    
    n_roads = 5
    n_routes_hat = 2
    n_routes_check = 2

    #routes for the hat population
    Gamma_hat = np.array([[1, 0],
                          [0, 1],
                          [1, 0],
                          [0, 0],
                          [0, 0]])
    
    #routes for the check population
    Gamma_check = np.array([[0, 0],
                            [0, 0],
                            [1, 0],
                            [1, 0],
                            [0, 1]])
    
    
    def tau_hat(self, nu_hat, nu_check):
        """
        Return the costs (travel time) of the roads for the hat population

        :param nu_hat: array where `nu_hat[i]` is the number of travelers of the hat population on road `i+1`
        :param nu_check: array where `nu_check[i]` is the number of travelers of the check population on road `i+1`
        :return: array with dimension `n_roads` with the costs (travel time) of the roads for the hat population. If no hat travelers use the road `i+1` then `return[i]` is set to 0 (since defining such a function is unnecessary)
        """
        return np.array([1+nu_hat[0], 3+nu_hat[1], 1+nu_hat[2]+nu_check[2], 0, 0])
    
    def tau_check(self, nu_hat, nu_check):
        """
        Return the costs (travel time) of the roads for the check population

        :param nu_hat: array where `nu_hat[i]` is the number of travelers of the hat population on road `i+1`
        :param nu_check: array where `nu_check[i]` is the number of travelers of the check population on road `i+1`
        :return: array with dimension `n_roads` with the costs (travel time) of the roads for the check population. If no check travelers use the road `i+1` then `return[i]` is set to 0 (since defining such a function is unnecessary)
        """
        return np.array([0, 0, 1+nu_hat[2]+nu_check[2], 1+nu_check[3], 3+nu_check[4]])