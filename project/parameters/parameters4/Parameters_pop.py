from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operations import Operations
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operations.NASH_EQ_POP_VARIATIONS
    
    @property
    def output_directory(self) -> str:
        return "esempi\\Es2"

    @property
    def MIN(self):
        return 0.

    @property
    def MAX(self):
        return 5.

    @property
    def step(self):
        return 0.05
    
    @property
    def variation_coefficient_pop_hat(self) -> float:
        return 0.
    
    @property
    def variation_coefficient_pop_check(self) -> float:
        return 1.

    @property
    def Gamma_hat(self):
        return SafeArray([[1., 0., 0.],
                          [0., 1., 0.],
                          [0., 0., 0.],
                          [0., 0., 1.],
                          [0., 1., 0.],
                          [0., 0., 1.]])
    
    @property
    def Gamma_check(self) -> SafeArray:
        return SafeArray([[0., 0.],
                          [0., 0.],
                          [1., 0.],
                          [0., 1.],
                          [1., 0.],
                          [0., 0.]])
    
    @override
    def tau_hat(self, eta_hat, eta_check):
        return (
            SafeArray([
                4.,
                1.+eta_hat[1, 0],
                np.inf,
                5.*eta_hat[3, 0]+5.*eta_check[3, 0],
                1.+eta_hat[4, 0]+eta_check[4, 0],
                1
            ])
        )
    
    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                np.inf,
                np.inf,
                eta_check[2, 0],
                5.*eta_hat[3, 0]+5.*eta_check[3, 0],
                1.+eta_hat[4, 0]+eta_check[4, 0],
                np.inf
            ])
        )