from utility.SafeArray import SafeArray
from Computer import Computer
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam

class Initializer:
    
    def __init__(self, param: AbstractParam):
        np.seterr(divide='ignore')
        
        if not isinstance(param, AbstractParam):
            raise TypeError("param deve essere un'istanza di BaseParameters")
        
        self.param = param
        self.computer = Computer(self.param)
        self.initial_theta_hat = SafeArray(np.ones((self.param.n_routes_hat, 1))*(1/self.param.n_routes_hat))
        self.initial_theta_check = SafeArray(np.ones((self.param.n_routes_check, 1))*(1/self.param.n_routes_check))
        self.limit_hat = 1e-11
        self.limit_check = 1e-11
        
        
    def start(self):
        """
            In base a operation in param, decide se calcolare l'equilibrio di Nash (senza variazioni) o costruire il grafico
            variando i costi delle strade
        """
        if self.param.operation == Operation.NASH_EQ:
            return self.getNashEquilibria()
        elif self.param.operation == Operation.NASH_EQ_VARIATIONS:
            return self.graphVariations()


    def getNashEquilibria(self):
        """
            Calcola l'Equilibrio di Nash e ritorna la distribuzione della popolazione hat e check sulla rete, insieme ai tempi di percorrenza della stessa.
            Se show_result==True, stampa tali risultati
        """     
        #Equilibrio di Nash:
        theta_hat, theta_check = self.computer.getNashEquilibria(self.initial_theta_hat, self.initial_theta_check, self.limit_hat, self.limit_check)
        
        #Tempi di viaggio su ogni strada:
        T_hat = self.computer.T_hat(theta_hat, theta_check, 0)
        T_check = self.computer.T_check(theta_hat, theta_check, 0)
        
        if self.param.show_result: self.printNashEq(theta_hat, theta_check, T_hat, T_check)
        
        return theta_hat, theta_check, T_hat, T_check
    
        
    def graphVariations(self):
        """
            Calcola gli array per costruire il grafico dei tempi di percorrenza della rete per le due popolazioni, che dipende dalla
            variazione nei costi delle strade. In ogni caso ritorna tali array. Se show_result==True, mostra il grafico
        """
        MIN = self.param.MIN
        MAX = self.param.MAX
        step = self.param.step
        
        variation_values = np.arange(MIN, MAX+step, step)
        N = len(variation_values)

        time_of_travel_hat = np.zeros(N)
        time_of_travel_check = np.zeros(N)
        
        thetas_hat = np.zeros((self.param.n_routes_hat, N))
        thetas_check = np.zeros((self.param.n_routes_check, N))
        
        theta_hat = self.initial_theta_hat
        theta_check = self.initial_theta_check
        
        for idx, i in enumerate(variation_values):
            if self.param.show_iterations: print("Current step: " + str(idx+1)+"/"+str(N))
            
            theta_hat, theta_check = self.computer.getNashEquilibriaVariation(theta_hat,
                                                                                theta_check, 
                                                                                self.limit_hat, 
                                                                                self.limit_check,
                                                                                i)
            T_hat = self.computer.T_hat(theta_hat, theta_check, i)
            T_check = self.computer.T_check(theta_hat, theta_check, i)
            
            index_hat = np.argmax(theta_hat > 0)
            index_check = np.argmax(theta_check > 0)
            
            time_of_travel_hat[idx] = T_hat[index_hat]
            time_of_travel_check[idx] = T_check[index_check]
            
            thetas_hat[:, idx] = theta_hat[:, 0]
            thetas_check[:, idx] = theta_check[:, 0]
            
        if self.param.show_result: self.showResultTimeVariation(variation_values, time_of_travel_hat, time_of_travel_check)
        if self.param.show_result: 
            self.showResultEqVariation(variation_values, thetas_hat, "hat")
            self.showResultEqVariation(variation_values, thetas_check, "check")
        
        return variation_values, time_of_travel_hat, time_of_travel_check
    
    
    def showResultTimeVariation(self, variation_values, time_of_travel_hat, time_of_travel_check):
        plt.plot(variation_values, time_of_travel_hat, label='Hat', color='blue')
        plt.plot(variation_values, time_of_travel_check, label='Check', color='red')
        plt.xlabel('Variazione del costo delle strade')
        plt.ylabel('Tempo di attraversamento della rete')
        plt.title('Tempo di attraversamento della rete\nin funzione della variazione dei costi')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def showResultEqVariation(self, variation_values, thetas, pop):
        import matplotlib.pyplot as plt
        import numpy as np

        n = thetas.shape[0]
        # determinare dimensioni griglia
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))

        # calcolo minimo e massimo di tutti i dati
        y_min = np.min(thetas)
        y_max = np.max(thetas)

        fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
        axes = axes.flatten()

        for i in range(n):
            ax = axes[i]
            ax.plot(variation_values, thetas[i, :], linewidth=1.8)

            ax.set_title(f'Theta_{pop}_{i}')
            ax.set_xlabel('Variazione del costo delle strade')
            ax.set_ylabel('Distribuzione popolazione')

            # usa la stessa scala su tutti i subplot
            ax.set_ylim(y_min, y_max)

            ax.grid(True)

        # rimuovere eventuali subplot vuoti
        for j in range(n, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
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
        
        