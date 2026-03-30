from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def n_roads(self):
        return 6

    @property
    def n_routes_hat(self):
        return 8

    @property
    def n_routes_check(self):
        return 2

    @property
    def operation(self):
        return Operation.NASH_EQ_VARIATIONS
    
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
                          [1., 1., 0., 0., 1., 1., 0., 0.],
                          [1., 0., 1., 0., 1., 0., 1., 0.],
                          [0., 0., 0., 0., 1., 1., 1., 1.],
                          [0., 0., 1., 1., 0., 0., 1., 1.],
                          [0., 1., 0., 1., 0., 1., 0., 1.]])
    
    @property
    def Gamma_check(self) -> SafeArray:
        return SafeArray([[1., 1.],
                          [1., 1.],
                          [1., 0.],
                          [0., 0.],
                          [0., 0.],
                          [0., 1.]])
    
    @property
    def variation_hat(self):
        return SafeArray([0., 0., 1., 0., 0., 0.])
    
    @property
    def variation_check(self):
        return SafeArray([0., 0., 1., 0., 0., 0.])
    
    @override
    def tau_hat(self, eta_hat, eta_check):
        return (
            SafeArray([
                2.+eta_hat[0, 0]+2*eta_check[0, 0],
                2.+eta_hat[1, 0]+2*eta_check[1, 0],
                2.+eta_hat[2, 0]+2*eta_check[2, 0],
                4.+eta_hat[3, 0],
                4.+eta_hat[4, 0],
                4.+eta_hat[5, 0]+2*eta_check[5, 0]
            ])
        )
    
    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                5,
                5,
                5,
                np.inf,
                np.inf,
                4.+eta_hat[5, 0]+2*eta_check[5, 0]
            ])
        )