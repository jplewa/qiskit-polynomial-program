import functools
from typing import List

import sympy
from qiskit.opflow import I, Z
from qiskit.opflow.list_ops import SummedOp


class PolynomialProgram:

    def __init__(self, num_variables: int):
        self.x = sympy.symbols(' '.join([f'x{i}' for i in range(num_variables)]))
        self.objective = sympy.Number(0)

    def add_objective(self, objective: sympy.core.expr.Expr, weight: float = 1.0):
        self.objective += weight * sympy.simplify(sympy.expand(objective))

    def _create_z(self, z_indices: List[int]):
        num_variables = len(self.x)
        return functools.reduce(
            lambda first_gate, second_gate: first_gate ^ second_gate,
            reversed([Z if index in z_indices else I for index in range(num_variables)])
        )

    def _get_summed_ops(self, coefficient_dict):
        ops = []
        offset = 0

        for summand, coefficient in coefficient_dict.items():
            coefficient = float(coefficient)
            if summand.is_Number:
                offset += float(coefficient)
            elif summand.is_Symbol:
                index = int(summand.name[1:])
                ops += [coefficient * self._create_z([index])]
            elif summand.is_Mul:
                indices = [
                    int(factor.base.name[1:])
                    if factor.is_Pow
                    else int(factor.name[1:])
                    for factor
                    in summand.args
                    if not factor.is_Pow or factor.exp % 2 == 1
                ]
                if indices == []:
                    offset += coefficient
                else:
                    ops += [coefficient * self._create_z(indices)]
            elif summand.is_Pow:
                indices = []
                if summand.exp % 2 == 1:
                    indices += [int(summand.base.name[1:])]
                if indices == []:
                    offset += coefficient
                else:
                    ops += [coefficient * self._create_z(indices)]
            else:
                raise RuntimeError(f'Error: unknown type of summand: {summand}')

        return SummedOp(ops).reduce(), offset

    def to_ising(self):
        simplified_objective = sympy.simplify(self.objective)

        for x_i in self.x:
            simplified_objective = simplified_objective.replace(x_i, .5 * (1 - x_i))

        coefficients = sympy.expand(simplified_objective).as_coefficients_dict()
        return self._get_summed_ops(coefficients)

    def evaluate_objective(self, bit_string: str):
        value = self.objective.evalf(subs={
            x_i: int(value) for (x_i, value) in zip(self.x, bit_string)
        })
        return round(value)
