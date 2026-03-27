from utility.SafeArray import SafeArray
from Computator import Computator
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from utility.Operation import Operation

class Initializer:
    def __init__(self, param):
        np.seterr(divide='ignore')
        
        self.param = param
        self.computator = Computator(self.param)
        self.initial_theta_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*(1/self.param.n_routes_hat))
        self.initial_theta_check = SafeArray(np.ones((self.param.n_routes_check, 1))*(1/self.param.n_routes_check))
        self.limit_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*1e-11)
        self.limit_check = SafeArray(np.ones((self.param.n_routes_check, 1))*1e-11)
        
    def start(self):
        if self.param.operation == Operation.NASH_EQ:
            return self.getNashEquilibria()
        elif self.param.operation == Operation.NASH_EQ_VARIATIONS:
            return self.graphVariations()

    def getNashEquilibria(self):        
        #Equilibrio di Nash:
        theta_hat, theta_check = self.computator.getNashEquilibria(self.initial_theta_hat, self.initial_theta_check, self.limit_hat, self.limit_check)
        
        #Tempi di viaggio su ogni strada:
        T_hat = self.computator.T_hat(theta_hat, theta_check, 0)
        T_check = self.computator.T_check(theta_hat, theta_check, 0)
        
        if self.param.show_result: self.printNashEq(theta_hat, theta_check, T_hat, T_check)
        
        return theta_hat, theta_check, T_hat, T_check
    
        
    def graphVariations(self):
        MIN = self.param.MIN
        MAX = self.param.MAX
        step = self.param.step
        
        variation_values = np.arange(MIN, MAX+step, step)
        N = len(variation_values)

        time_of_travel_hat = np.zeros(N)
        time_of_travel_check = np.zeros(N)
        
        for idx, i in enumerate(variation_values):
            print("Current step: " + str(idx+1)+"/"+str(N))
            
            theta_hat, theta_check = self.computator.getNashEquilibriaVariation(self.initial_theta_hat,
                                                                                                self.initial_theta_check, 
                                                                                                self.limit_hat, 
                                                                                                self.limit_check,
                                                                                                i)
            T_hat = self.computator.T_hat(theta_hat, theta_check, i)
            T_check = self.computator.T_check(theta_hat, theta_check, i)
            
            index_hat = np.argmax(theta_hat > 0)
            index_check = np.argmax(theta_check > 0)
            
            time_of_travel_hat[idx] = T_hat[index_hat]
            time_of_travel_check[idx] = T_check[index_check]
            
        if self.param.show_result: self.showResultPlot(variation_values, time_of_travel_hat, time_of_travel_check)
        
        return variation_values, time_of_travel_hat, time_of_travel_check
    
    def showResultPlot(self, variation_values, time_of_travel_hat, time_of_travel_check):
        plt.plot(variation_values, time_of_travel_hat, label='Hat', color='blue')
        plt.plot(variation_values, time_of_travel_check, label='Check', color='red')
        plt.xlabel('Variazione del tempo di viaggio')
        plt.ylabel('Tempo di viaggio')
        plt.title('Tempo di viaggio in funzione della variazione')
        plt.legend()
        plt.grid(True)
        plt.show()
 
    def printNashEq(self, theta_hat, theta_check, T_hat, T_check):
        vec_frac = np.vectorize(
            lambda x: str(x) if np.isinf(x) or not self.param.print_as_fraction else str(Fraction(x).limit_denominator(1000000))
        )
    
        print("Equilibrio di Nash:")
        print("theta_hat:\n", vec_frac(theta_hat))
        print("theta_check:\n", vec_frac(theta_check))
        
        print()
        
        print("Tempi di attraversamento dei percorsi:")
        print("T_hat:\n", vec_frac(T_hat))
        print("T_check:\n", vec_frac(T_check))
        
        