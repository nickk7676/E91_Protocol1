import random
import cirq
import numpy as np

#Show the possible base options for alice, bob, and eve in the circuit (assuming that eve has the same base options as bob)
alice_bases = {
    'a1' : 0,
    'a2' : np.pi/4,
     'a3' : np.pi/2
}

bob_bases = {
    'b1' : np.pi/4,
    'b2' : np.pi/2,
    'b3' : 3*np.pi/4
}

eve_bases = {
    'e1' : np.pi/4,
    'e2' : np.pi/2,
    'e3' : 3*np.pi/4    
}

#Runs a simple intercept and resend attack and returns the result of that one singlet state. 
def run_naive():

    #Choosing a random base and then setting the respective theta to that base's value. 
    alice_random_base = random.choice(list(alice_bases.keys()))
    alice_theta = alice_bases[alice_random_base] 
    bob_random_base = random.choice(list(bob_bases.keys()))
    bob_theta = bob_bases[bob_random_base]
    eve_random_base = random.choice(list(eve_bases.keys()))
    eve_theta = eve_bases[eve_random_base]

    #Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
    qubits = cirq.NamedQubit.range(2, prefix='q')
    circuit = cirq.Circuit()

    #Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.Z(qubits[0])) 

    #Eve's Interception part
    circuit.append(cirq.rx(eve_theta).on(qubits[1]))
    circuit.append(cirq.measure(qubits[1], key='eve'))
    circuit.append(cirq.rx(-eve_theta).on(qubits[1]))  

    #Use the random angle to rotate the qubit and then measure
    circuit.append(cirq.rx(alice_theta).on(qubits[0]))
    circuit.append(cirq.rx(bob_theta).on(qubits[1]))
    circuit.append(cirq.measure(qubits[0], key='alice'))
    circuit.append(cirq.measure(qubits[1], key='bob'))

    ##Run the Circuit and get the measurement that alice and bob measured respectively.
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


