import unittest

from qiskit.opflow import I, Z
from qiskit.opflow.list_ops import SummedOp

from qiskit_polynomial_program.polynomial_program import PolynomialProgram


class MyTestCase(unittest.TestCase):

    def test_simple_sum(self):
        program = PolynomialProgram(3)
        x = program.x
        program.add_objective(x[0] + x[1] + x[2])
        hamiltonian, offset = program.to_ising()

        expected_hamiltonian = SummedOp([
            -.5 * Z ^ I ^ I,
            -.5 * I ^ Z ^ I,
            -.5 * I ^ I ^ Z
        ])

        self.assertAlmostEqual(offset, 1.5)
        self.assertEqual(hamiltonian, expected_hamiltonian)

    def test_simple_sum_with_square(self):
        program = PolynomialProgram(3)
        x = program.x
        program.add_objective(x[0] + x[1] ** 2 + x[2])
        hamiltonian, offset = program.to_ising()

        expected_hamiltonian = SummedOp([
            -.5 * Z ^ I ^ I,
            -.5 * I ^ Z ^ I,
            -.5 * I ^ I ^ Z,
        ])

        self.assertAlmostEqual(offset, 1.5)
        self.assertEqual(hamiltonian, expected_hamiltonian)

    def test_simple_sum_with_third_power(self):
        program = PolynomialProgram(3)
        x = program.x
        program.add_objective(x[0] + x[1] ** 3 + x[2])
        hamiltonian, offset = program.to_ising()

        expected_hamiltonian = SummedOp([
            -.5 * Z ^ I ^ I,
            -.5 * I ^ Z ^ I,
            -.5 * I ^ I ^ Z,
        ])

        self.assertAlmostEqual(offset, 1.5)
        self.assertEqual(hamiltonian, expected_hamiltonian)
