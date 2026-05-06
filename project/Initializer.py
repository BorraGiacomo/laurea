from pathlib import Path

from utility.SafeArray import SafeArray
from Computer import Computer
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from utility.Operations import Operations
from utility.AbstractParam import AbstractParam

class Initializer:
    
    def __init__(self, param: AbstractParam):
        np.seterr(divide='ignore')
        
        if not isinstance(param, AbstractParam):
            raise TypeError("param deve essere un'istanza di AbstractParameters")
        
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
        if self.param.operation == Operations.NASH_EQ:
            return self.getNashEquilibria()
        else:
            return self.graphVariations()


    def getNashEquilibria(self):
        """
            Calcola l'Equilibrio di Nash e ritorna la distribuzione della popolazione hat e check sulla rete, insieme ai tempi di percorrenza della stessa.
            Se save_result==True, stampa tali risultati
        """     
        #Equilibrio di Nash:
        theta_hat, theta_check = self.computer.getNashEquilibria(self.initial_theta_hat, self.initial_theta_check, self.limit_hat, self.limit_check)
        
        #Tempi di viaggio su ogni strada:
        T_hat = self.computer.T_hat(theta_hat, theta_check, self.param.entity_number_hat, self.param.entity_number_check, 0)
        T_check = self.computer.T_check(theta_hat, theta_check, self.param.entity_number_hat, self.param.entity_number_check, 0)
        
        if self.param.save_result: self.saveNashEq(theta_hat, theta_check, T_hat, T_check)
        
        return theta_hat, theta_check, T_hat, T_check
    
        
    def graphVariations(self):
        """
        Calcola gli array per costruire il grafico dei tempi di percorrenza della rete
        per le due popolazioni in funzione della variazione (costi o popolazione).
        Restituisce gli array per costruire i grafici e opzionalmente salva i risultati.
        """
        p = self.param
        variation_values = np.arange(p.MIN, p.MAX + p.step, p.step)
        N = len(variation_values)

        time_hat = np.zeros(N)
        time_check = np.zeros(N)
        thetas_hat = np.zeros((p.n_routes_hat, N))
        thetas_check = np.zeros((p.n_routes_check, N))

        theta_hat, theta_check = self.initial_theta_hat, self.initial_theta_check

        for idx, v in enumerate(variation_values):
            if p.show_iterations:
                print(f"Current step: {idx+1}/{N}")

            theta_hat, theta_check, T_hat, T_check = self._compute_step(
                theta_hat, theta_check, v
            )

            i_hat = np.argmax(theta_hat > 0)
            i_check = np.argmax(theta_check > 0)

            time_hat[idx] = T_hat[i_hat]
            time_check[idx] = T_check[i_check]
            thetas_hat[:, idx] = theta_hat[:, 0]
            thetas_check[:, idx] = theta_check[:, 0]

        if p.save_result:
            label = ('Variazione del costo delle strade'
                    if p.operation == Operations.NASH_EQ_TIME_VARIATIONS
                    else 'Variazione del numero di individui nella popolazione')

            self.saveResultVariation(variation_values, time_hat, time_check, label)
            self.saveResultThetaVariation(variation_values, thetas_hat, 'hat', label)
            self.saveResultThetaVariation(variation_values, thetas_check, 'check', label)

        return variation_values, time_hat, time_check, thetas_hat, thetas_check
    
    def _compute_step(self, theta_hat, theta_check, v):
        p = self.param
        c = self.computer

        if p.operation == Operations.NASH_EQ_TIME_VARIATIONS:
            theta_hat, theta_check = c.getNashEquilibriaCostVariation(
                theta_hat, theta_check, self.limit_hat, self.limit_check, v
            )
            pop_hat, pop_check, var = p.entity_number_hat, p.entity_number_check, v

        else:
            pop_hat = p.entity_number_hat + (v*p.variation_coefficient_pop_hat)
            pop_check = p.entity_number_check + (v*p.variation_coefficient_pop_check)

            theta_hat, theta_check = c.getNashEquilibriaPopVariation(
                theta_hat, theta_check, self.limit_hat, self.limit_check, pop_hat, pop_check
            )
            var = 0

        T_hat = c.T_hat(theta_hat, theta_check, pop_hat, pop_check, var)
        T_check = c.T_check(theta_hat, theta_check, pop_hat, pop_check, var)

        return theta_hat, theta_check, T_hat, T_check
    
    def saveResultVariation(self, variation_values, time_of_travel_hat, time_of_travel_check, xLabel):
        plt.plot(variation_values, time_of_travel_hat, label=f'Hat', color='blue')
        plt.plot(variation_values, time_of_travel_check, label='Check', color='red')
        plt.xlabel(xLabel)
        plt.ylabel('Tempo di attraversamento della rete')
        plt.title(f'Tempo di attraversamento della rete\nin funzione di: {xLabel}')
        plt.legend()
        plt.grid(True)
        self.saveGraph(f'main_{xLabel}')
        
    def saveResultThetaVariation(self, variation_values, thetas, pop, xLabel):
        n = thetas.shape[0]

        subfolder = "hat" if pop == "hat" else "check"

        for i in range(n):
            plt.figure(figsize=(6, 4))

            plt.plot(variation_values, thetas[i, :], linewidth=1.8, color='red')

            plt.title(f'Theta_{pop}_{i+1}')
            plt.xlabel(xLabel)
            plt.ylabel('Distribuzione popolazione')
            plt.ylim(0, 1)
            plt.grid(True)

            file_label = f"{pop}/{subfolder}_theta_{i+1}_{xLabel}"

            self.saveGraph(file_label)

            plt.close() 
 
 
    def saveGraph(self, xLabel):
        file_name = f"grafico_{xLabel}.png".replace(" ", "_")

        file_path = Path(self.param.output_directory) / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        plt.savefig(file_path, dpi=300, bbox_inches='tight', pad_inches=0.5)
 
 
    def _format_nash_eq(self, theta_hat, theta_check, T_hat, T_check):
        vec_frac = np.vectorize(
            lambda x: str(x) if np.isinf(x) or not self.param.save_as_fraction 
            else str(Fraction(x).limit_denominator(1000000))
        )

        lines = []
        lines.append("Equilibrio di Nash:")
        lines.append(f"theta_hat:\n{vec_frac(theta_hat)}")
        lines.append(f"theta_check:\n{vec_frac(theta_check)}")
        lines.append("")
        lines.append("Tempi di attraversamento dei percorsi:")
        lines.append(f"T_hat:\n{vec_frac(T_hat)}")
        lines.append(f"T_check:\n{vec_frac(T_check)}")

        return "\n".join(lines)
        
    def saveNashEq(self, theta_hat, theta_check, T_hat, T_check, file_name="nash_eq.txt"):
        content = self._format_nash_eq(theta_hat, theta_check, T_hat, T_check)

        file_path = Path(self.param.output_directory) / file_name

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        