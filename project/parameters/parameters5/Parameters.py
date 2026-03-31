from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operation.NASH_EQ
    
    @property
    def show_result(self):
        return True

    @property
    def print_as_fraction(self):
        return True

    @property
    def show_iterations(self):
        return True

    @property
    def MIN(self):
        return 0

    @property
    def MAX(self):
        return 6

    @property
    def step(self):
        return 0.2

    @property
    def Gamma_hat(self):
        return SafeArray([[1., 1., 1., 1., 0., 0., 0., 0.],
                          [1., 1., 0., 0., 0., 0., 1., 1.],
                          [1., 0., 1., 0., 1., 0., 1., 0.],
                          [0., 0., 0., 0., 1., 1., 1., 1.],
                          [0., 0., 1., 1., 1., 1., 0., 0.],
                          [0., 1., 0., 1., 0., 1., 0., 1.],
                          [0., 0., 1., 1., 0., 0., 0., 0.],
                          [0., 0., 0., 0., 0., 0., 1., 1.]])
    
    @property
    def Gamma_check(self) -> SafeArray:
        return SafeArray([[1., 1.],
                          [1., 1.],
                          [1., 0.],
                          [0., 0.],
                          [0., 0.],
                          [0., 1.],
                          [0., 0.],
                          [0., 0.]])
    
    @property
    def variation_hat(self):
        return SafeArray([0., 0., -1., 0., 0., 0., 0., 0.])
    
    @property
    def variation_check(self):
        return SafeArray([0., 0., -1., 0., 0., 1., 0., 0.])
    
    @override
    def tau_hat(self, eta_hat, eta_check):
        return (
            SafeArray([
                3.+eta_hat[0, 0]+eta_check[0, 0],
                3.+eta_hat[1, 0]+eta_check[1, 0],
                3.+eta_hat[2, 0]+eta_check[2, 0] + self.MAX,
                4.+eta_hat[3, 0],
                5.+eta_hat[4, 0],
                4.+eta_hat[5, 0]+2*eta_check[5, 0],
                0,
                0
            ])
        )
    
    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                4,
                4,
                4 + self.MAX,
                np.inf,
                np.inf,
                4.+eta_hat[5, 0]+2*eta_check[5, 0],
                np.inf,
                np.inf
            ])
        )