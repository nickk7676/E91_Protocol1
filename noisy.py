import random
import numpy as np
import cirq

#Declare bases possible for alice and bob
alice_bases = {
    'a1' : 0,
    'a2' : np.radians(45),
    'a3' : np.radians(90)
}

bob_bases = {
    'b1' : np.radians(45),
    'b2' : np.radians(90),
    'b3' : np.radians(135)
}

#Runs a circuit with noise and no eve
def run_noisy(noise_strength:float):

    #Choosing bases randomly and then setting its theta to the respective base
    alice_random_base = random.choice(list(alice_bases.keys()))
    alice_theta = alice_bases[alice_random_base] 
    bob_random_base = random.choice(list(bob_bases.keys()))
    bob_theta = bob_bases[bob_random_base]

    #Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
    qubits = cirq.NamedQubit.range(2, prefix='q')
    circuit = cirq.Circuit()

    #Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.Z(qubits[0]))  

    #Add Noise
    circuit.append(cirq.depolarize(noise_strength).on(qubits[0]))
    circuit.append(cirq.depolarize(noise_strength).on(qubits[1]))

    #Use the random angle to rotate the qubit and then measure
    circuit.append(cirq.rx(alice_theta).on(qubits[0]))
    circuit.append(cirq.rx(bob_theta).on(qubits[1]))
    circuit.append(cirq.measure(qubits[0], key='alice'))
    circuit.append(cirq.measure(qubits[1], key='bob'))

    #Simulate the circuit and get the results for each qubit. 
    sim = cirq.Simulator()
    result = sim.run(circuit)
    alice_result = result.measurements['alice']
    bob_result = result.measurements['bob']

    #Return a dictionary containing the necessary values to be used in the future. 
    return {
        'alice_random_base' : alice_random_base,
        'bob_random_base' : bob_random_base,
        'alice_result' : alice_result,
        'bob_result': bob_result
    }