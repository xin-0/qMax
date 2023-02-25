from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate
# from qiskit.circuit.quantumcircuit import QubitSpecifier

import numpy as np

from typing import List

def ry_QFT(
    num_qubit: int,
    inverse: bool = False
) -> Gate:
    """
        Do fourier transform with ry rotations.

        Args:            
            num_qubit: `int`
                define the number of qubit that will be applied qft

            inverse: `bool`
                if `true`, will return the inverse qft. defualt is `false`
    """

    qc = QuantumCircuit(num_qubit, name="yQFT")

    for ctl_q in reversed(range(num_qubit - 1)):
        for target in reversed(range(ctl_q + 1, num_qubit)):
            angle_exp = target - ctl_q
            theta = np.pi/(2**angle_exp)
            qc.cry(theta=theta, target_qubit=target, control_qubit=ctl_q)

    yQFT_gate = qc.to_gate()

    if inverse:
        return yQFT_gate.inverse()

    return yQFT_gate


def yQft_adder(
    X: int,
    num_qubit: int
) -> Gate:

    """
        Add a classical data `X`, an integer, into targeted quantum register.
        The addant should be already in fourier basis. Output is also in fourier basis.
    
        Args:
            X: `int`
                An classically given integer. Can be positive or negative.

            num_qubit: `int`
                the number of qubit of the target register representing the addant(in fourier basis). 
    """

    qc = QuantumCircuit(num_qubit, name= "qft_add(" + str(X) + ")")

    for k in range(num_qubit):
        theta = np.pi*X/(2**(k))
        qc.ry(theta=theta, qubit=k)

    qft_add_gate = qc.to_gate()

    return qft_add_gate



def qAdder(
    X: int,
    num_qubit: int    
) -> Gate:
    """
        given an input register in basic encoding, add classically given integer `X`
        to the quantum register and the result will also be in basic encoding

        Args:
            X: `int`
                An classically given integer. Can be positive or negative.

            num_qubit: `int`
                the number of qubit of the target register representing the addant. 
    """

    qc = QuantumCircuit(num_qubit, name="add(" + str(X) + ")") 

    # if X is 0 the gate is identity
    if 0 == X:
        qc.id(range(qc.num_qubits))
        return qc.to_gate()

    # transform the addant into fourier basis
    qc.append(
        ry_QFT(num_qubit=num_qubit),
        range(num_qubit)
    )

    # use the adder in fourier basis to add `X`
    qc.append(
        yQft_adder(X=X, num_qubit=num_qubit),
        range(num_qubit)
    )

    # transform back into basic encoding
    qc.append(
        ry_QFT(num_qubit=num_qubit, inverse=True),
        range(num_qubit)
    )

    return qc.to_gate()