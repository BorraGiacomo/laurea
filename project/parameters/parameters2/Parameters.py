from typing import override

from utility.SafeArray import SafeArray
import numpy as np
from utility.Operation import Operation
from utility.AbstractParam import AbstractParam


class Parameters(AbstractParam):

    @property
    def n_roads(self):
        return 7

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
            [0., 1.],
            [1., 0.],
            [0., 0.],
            [0., 0.],
            [1., 0.],
            [0., 0.],
            [1., 0.]
        ])

    @property
    def Gamma_check(self):
        return SafeArray([
            [0., 0.],
            [0., 0.],
            [1., 0.],
            [0., 1.],
            [1., 0.],
            [1., 0.],
            [0., 0.]
        ])

    @property
    def variation_hat(self):
        return SafeArray(np.zeros(self.n_roads))

    @property
    def variation_check(self):
        return SafeArray(np.zeros(self.n_roads))

    @override
    def tau_hat(self, eta_hat, eta_check):
        temp = eta_hat[4, 0] + eta_check[4, 0]

        return (
            SafeArray([
                5/2 + eta_hat[0, 0],
                1,
                np.inf,
                np.inf,
                temp / (1 - temp),
                np.inf,
                1
            ]) + self.variation_hat
        )

    @override
    def tau_check(self, eta_hat, eta_check):
        temp = eta_hat[4, 0] + eta_check[4, 0]

        return (
            SafeArray([
                np.inf,
                np.inf,
                1,
                2 + eta_check[3, 0],
                temp / (1 - temp),
                1,
                np.inf
            ]) + self.variation_check
        )