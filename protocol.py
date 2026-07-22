import cirq
import numpy as np
import random

def chshValue(chsh_calculation):
    a1b1 = []
    a1b3 = []
    a3b1 = []
    a3b3 = []

    for i in range(len(chsh_calculation)):
        entry = chsh_calculation[i]
        alice_base = entry['alice_random_base']
        bob_base = entry['bob_random_base']
        if (alice_base == "a1" and bob_base == "b1") :
            a1b1.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome'],
            })
        elif (alice_base == "a1" and bob_base == "b3"):
            a1b3.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })
        elif (alice_base == "a3" and bob_base == "b1"):
            a3b1.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })
        elif (alice_base == "a3" and bob_base == "b3"):
            a3b3.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })

    total = 0
    for i in range(len(a1b1)):
        entry = a1b1[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a1b1_E = total/len(a1b1)

    total = 0
    for i in range(len(a1b3)):
        entry = a1b3[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a1b3_E = total/len(a1b3)

    total = 0
    for i in range(len(a3b1)):
        entry = a3b1[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a3b1_E = total/len(a3b1)

    total = 0
    for i in range(len(a3b3)):
        entry = a3b3[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a3b3_E = total/len(a3b3)

    s = a1b1_E - a1b3_E + a3b1_E + a3b3_E 
    return s




#set num_rounds carefully because it can overflow the terminal very quickly

num_rounds = 1000
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
        'a2' : np.pi/4,
        'a3' : np.pi/2
    }

    bob_bases = {
        'b1' : np.pi/4,
        'b2' : np.pi/2,
        'b3' : 3*np.pi/4
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

    if alice_result[0][0] == 0 :
        alice_outcome = 1
    else:
        alice_outcome = -1

    if bob_result[0][0] == 0 :
        bob_outcome = 1
    else:
        bob_outcome = -1

    if (alice_random_base == 'a2' and bob_random_base == 'b1') or (alice_random_base == 'a3' and bob_random_base == 'b2') :
        keyGeneration.append(int(alice_result[0][0]))
    else:
        chsh_calculation.append({
            'alice_random_base' : alice_random_base,
            'bob_random_base' : bob_random_base,
            'alice_outcome' : alice_outcome, 
            'bob_outcome' : bob_outcome
        })

s = abs(chshValue(chsh_calculation))
print(s)
