from setuptools import find_packages, setup

setup(
    name='qiskit_polynomial_program',
    packages=find_packages(include=['qiskit_polynomial_program']),
    version='0.1.0',
    description='Qiskit polynomial program to Hamiltonian util',
    author='Julia Plewa',
    license='MIT',
    install_requires=['qiskit==0.29.0', 'qiskit-optimization==0.2.2', 'sympy==1.8'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.2.4', 'qiskit==0.29.0'],
    test_suite='tests',
)
