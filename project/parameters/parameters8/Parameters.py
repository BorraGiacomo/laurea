from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operations import Operations
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operations.NASH_EQ_TIME_VARIATIONS

    @property
    def MIN(self):
        return 0.

    @property
    def MAX(self):
        return 70.

    @property
    def step(self):
        return 1.
    
    @property
    def entity_number_hat(self) -> float:
        return 30.
    
    @property
    def entity_number_check(self) -> float:
        return 30.
    
    @property
    def variation_hat(self) -> SafeArray:
        return SafeArray([0., 0., 0., 1., 1.])
    
    @property
    def output_directory(self):
        return "parameters\\parameters8"

    @property
    def Gamma_hat(self):
        return SafeArray([[1., 0., 1.],
                          [1., 0., 0.],
                          [1., 1., 0.],
                          [0., 1., 0.],
                          [0., 0., 1.]])
    
    @property
    def Gamma_check(self) -> SafeArray:
        return SafeArray([[1.],
                          [1.],
                          [1.],
                          [0.],
                          [0.]])
    
    @override
    def tau_hat(self, eta_hat, eta_check):        
        return (
            SafeArray([
                30. + eta_hat[0, 0] + eta_check[0, 0] + eta_hat[3, 0] + eta_hat[4, 0],
                30. + eta_hat[1, 0] + eta_check[1, 0] + eta_hat[3, 0] + eta_hat[4, 0],
                5. + eta_hat[2, 0] + eta_check[2, 0] + eta_hat[4, 0],
                135. + eta_hat[3, 0],
                105. + eta_hat[4, 0]
            ])
        )
    
    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                30. + eta_hat[0, 0] + eta_check[0, 0] + eta_hat[3, 0] + eta_hat[4, 0],
                30. + eta_hat[1, 0] + eta_check[1, 0] + eta_hat[3, 0] + eta_hat[4, 0],
                5. + eta_hat[2, 0] + eta_check[2, 0] + eta_hat[4, 0],
                np.inf,
                np.inf
            ])
        )