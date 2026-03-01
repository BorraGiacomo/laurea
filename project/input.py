import numpy as np

import parameters.Parameters as Param

def main():
    param = Param.Parameters()
    
    #Given theta (distribution of the hat and check population on the routes):
    theta_hat = np.array([1/2, 1/2])
    
    theta_check = np.array([1/2, 1/2])
    
    #Population on each road:
    pop_hat = param.Gamma_hat @ theta_hat.T
    
    pop_check = param.Gamma_check @ theta_check.T
    
    #Travel times for every route
    T_hat = param.tau_hat(pop_hat, pop_check) @ param.Gamma_hat
    T_check = param.tau_check(pop_hat, pop_check) @ param.Gamma_check
    
    print(T_hat)
    print(T_check)

if __name__ == "__main__":
    main()