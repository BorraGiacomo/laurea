from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam


class Parameters(AbstractParam):

    @property
    def n_roads(self):
        return 5

    @property
    def n_routes_hat(self):
        return 2

    @property
    def n_routes_check(self):
        return 2

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
        return 0.5

    @property
    def step(self):
        return 0.01

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

    @property
    def variation_hat(self):
        return SafeArray(np.zeros(self.n_roads))

    @property
    def variation_check(self):
        return SafeArray(np.zeros(self.n_roads))

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