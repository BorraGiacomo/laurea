from typing import override

from utility.SafeArray import SafeArray
from utility.Operations import Operations
from utility.AbstractParam import AbstractParam

class Parameters(AbstractParam):

    @property
    def operation(self):
        return Operations.NASH_EQ_POP_VARIATIONS
    
    @property
    def output_directory(self):
        return "esempi\\Es1"
    
    @property
    def MIN(self) -> float:
        return 0.
    
    @property
    def MAX(self) -> float:
        return 2.
    
    @property
    def step(self) -> float:
        return 0.01

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
                0
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
                0
            ])
        )