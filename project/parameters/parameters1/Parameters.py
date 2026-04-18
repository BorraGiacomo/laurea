from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operations import Operations
from utility.AbstractParam import AbstractParam


class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operations.NASH_EQ
    
    @property
    def output_directory(self):
        return "parameters\\parameters1"
    
    @property
    def entity_number_hat(self) -> float:
        return 2.
    
    @property
    def entity_number_check(self) -> float:
        return 2.

    @property
    def Gamma_hat(self):
        return SafeArray([
            [1., 0.],
            [0., 1.],
            [1., 0.],
            [0., 0.],
            [0., 0.]
        ])

    @property
    def Gamma_check(self):
        return SafeArray([
            [0., 0.],
            [0., 0.],
            [1., 0.],
            [1., 0.],
            [0., 1.]
        ])

    @override
    def tau_hat(self, eta_hat, eta_check):
        return (
            SafeArray([
                1. + eta_hat[0, 0],
                3. + eta_hat[1, 0],
                1. + eta_hat[2, 0] + eta_check[2, 0],
                np.inf,
                np.inf
            ])
        )

    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                np.inf,
                np.inf,
                1. + eta_hat[2, 0] + eta_check[2, 0],
                1. + eta_check[3, 0],
                3. + eta_check[4, 0]
            ])
        )