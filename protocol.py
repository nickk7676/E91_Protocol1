import cirq
import numpy as np
import random

#set num_rounds carefully because it can overflow the terminal very quickly
num_rounds = 10
results=[]
keyGeneration = []
chsh_calculation=[]

for _ in range(num_rounds):
    qubits = cirq.NamedQubit.range(2, prefix='q')
    circuit = cirq.Circuit()

    #Preparing the Bell State of (1/sqrt(2))(|01>-|10>)
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.X(qubits[1]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.Z(qubits[0]))

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

    results.append({
        'alice_random_base' : alice_random_base,
        'bob_random_base' : bob_random_base,
        'alice_result' : alice_result,
        'bob_result': bob_result
    })

    if alice_result[0][0] == [[0]] :
        alice_outcome = 1
    else:
        alice_outcome = -1

    if bob_result[0][0] == [[0]] :
        bob_outcome = 1
    else:
        bob_outcome = -1

    if alice_theta == bob_theta :
        keyGeneration.append(int(alice_result[0][0]))
    else:
        chsh_calculation.append({
            'alice_random_base' : alice_random_base,
            'bob_random_base' : bob_random_base,
            'alice_outcome' : alice_outcome, 
            'bob_outcome' : bob_outcome
        })

for i, r in enumerate(results[:num_rounds]):
    print(f"Round {i+1:4d} | Alice: {r['alice_random_base']} -> {r['alice_result']} | Bob: {r['bob_random_base']} -> {r['bob_result']}")
print("--------------------------------------------------------------")

print("Key Generation: ",  keyGeneration)
print("--------------------------------------------------------------")
print("          CHSH Calculation Angles and the +/- Outcome         ")
for i, r in enumerate(chsh_calculation[:num_rounds]):
    print(f"Outcome {i+1:4d} | Alice: {r['alice_random_base']} -> {r['alice_outcome']} | Bob: {r['bob_random_base']} -> {r['bob_outcome']}")
