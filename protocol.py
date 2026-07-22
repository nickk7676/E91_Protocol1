import cirq
import numpy as np
import random

qubits = cirq.NamedQubit.range(2, prefix='q')
circuit = cirq.Circuit()

#Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
circuit.append(cirq.H(qubits[0]))
circuit.append(cirq.X(qubits[1]))
circuit.append(cirq.CNOT(qubits[0], qubits[1]))
circuit.append(cirq.Z(qubits[0]))

print(circuit)

#Set up a randomizer to get a random angle each time
alice_bases = {
    'a1' : 0,
    'a2' : np.pi/2,
    'a3' : -np.pi/2
}

bob_bases = {
    'b1' : 0,
    'b2' : np.pi/4,
    'b3' : -np.pi/4
}

alice_random_base = random.choice(list(alice_bases.keys()))
alice_theta = alice_bases[alice_random_base]

bob_random_base = random.choice(list(bob_bases.keys()))
bob_theta = bob_bases[bob_random_base]

#use the random angle to rotate the qubit and then measure
circuit.append(cirq.rx(alice_theta).on(qubits[0]))
circuit.append(cirq.rx(bob_theta).on(qubits[1]))

circuit.append(cirq.measure(qubits[0], key='alice'))
circuit.append(cirq.measure(qubits[1], key='bob'))

sim = cirq.Simulator()
result = sim.run(circuit)
alice_result = result.measurements['alice']
bob_result = result.measurements['bob']
print(alice_result, alice_random_base)
print(bob_result, bob_random_base)