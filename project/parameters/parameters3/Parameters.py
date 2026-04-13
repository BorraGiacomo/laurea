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
    def output_directory(self):
        return "parameters\\parameters3"
    
    @property
    def entity_number_hat(self) -> float:
        return 1.
    
    @property
    def entity_number_check(self) -> float:
        return 1.

    @property
    def Gamma_hat(self):
        return SafeArray([
            [0., 1., 0.],
            [1., 0., 1.],
            [1., 0., 0.],
            [0., 1., 1.],
            [0., 0., 1.]
        ])

    @property
    def Gamma_check(self):
        return SafeArray([
            [0., 1., 0.],
            [1., 0., 1.],
            [1., 0., 0.],
            [0., 1., 1.],
            [0., 0., 1.]
        ])

    @override
    def tau_hat(self, eta_hat, eta_check):
        return (
            SafeArray([
                45.,
                40. * eta_hat[1, 0],
                45.,
                40. * eta_hat[3, 0],
                np.inf
            ])
        )

    @override
    def tau_check(self, eta_hat, eta_check):
        return (
            SafeArray([
                30.,
                20. * eta_check[1, 0] + 8. * eta_hat[1, 0],
                30.,
                20. * eta_check[1, 0] + 8. * eta_hat[1, 0],
                np.inf
            ])
        )