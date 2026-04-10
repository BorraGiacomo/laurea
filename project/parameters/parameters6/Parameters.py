from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operation.NASH_EQ_POP_VARIATIONS
    
    @property
    def show_result(self):
        return True

    @property
    def show_iterations(self):
        return True

    @property
    def MIN(self):
        return 1

    @property
    def MAX(self):
        return 60

    @property
    def step(self):
        return 0.5

    @property
    def Gamma_hat(self):
        return SafeArray([[1., 1., 1., 0., 0., 0.],
                          [1., 1., 0., 1., 1., 0.],
                          [1., 0., 0., 1., 0., 0.],
                          [0., 0., 0., 1., 1., 1.],
                          [0., 0., 1., 0., 0., 1.],
                          [0., 1., 1., 0., 1., 1.],
                          [0., 0., 1., 0., 0., 0.],
                          [0., 0., 0., 1., 1., 0.],
                          [0., 1., 0., 0., 1., 0.]])
    
    @property
    def Gamma_check(self) -> SafeArray:
        return SafeArray([[1., 1.],
                          [1., 1.],
                          [1., 0.],
                          [0., 0.],
                          [0., 0.],
                          [0., 1.],
                          [0., 0.],
                          [0., 0.],
                          [0., 1.]])
    
    @override
    def tau_hat(self, eta_hat, eta_check):        
        return (
            SafeArray([
                60./(1.-(eta_hat[0, 0]+4.*eta_check[0, 0])/325.),
                120./(1.-(eta_hat[1, 0]+4.*eta_check[1, 0])/700.),
                180./(1.-(eta_hat[2, 0]+4.*eta_check[2, 0])/800.),
                180./(1.-(eta_hat[3, 0])/500.),
                180./(1.-(eta_hat[4, 0])/575.),
                300./(1.-(eta_hat[5, 0]+4.*eta_check[5, 0])/1175.),
                0.,
                0.,
                0.
            ])
        )
    
    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                60./(1.-(eta_hat[0, 0]+4.*eta_check[0, 0])/325.),
                120./(1.-(eta_hat[1, 0]+4.*eta_check[1, 0])/700.),
                180./(1.-(eta_hat[2, 0]+4.*eta_check[2, 0])/800.),
                np.inf,
                np.inf,
                np.inf,
                np.inf,
                np.inf,
                np.inf
            ])
        )