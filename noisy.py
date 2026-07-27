import cirq
import numpy as np
import random

num_rounds = 2000

alice_bases = {
  'a1': 0,
  'a2': np.pi / 4,
  'a3': np.pi / 2
}

bob_bases = {
  'b1': np.pi / 4,
  'b2': np.pi / 2,
  'b3': 3 * np.pi / 4
}

def run_round(mode="clean", noise_p=0.0, eve_rate=0.0):
    """
    :param mode: 'clean', 'noisy', or 'eavesdropped'
    :param noise_p: Depolarizing noise probability per qubit (for 'noisy' mode)
    :param eve_rate: Probability of Eve interecepting and measuring (for 'eavesdropped' mode)
    """

alice_random_base = random.choice(list(alice_bases.keys()))
alice_theta = alice_bases[alice_random_base]

bob_random_base = random.choice(list(bob_bases.keys()))
bob_theta = bob_bases[bob_random_base]

qubits = cirq.NamedQubit.range(2, prefix='q')
circuit = cirq.Circuit()

circuit.append([
    cirq.H(qubits[0]),
    cirq.X(qubits[1]),
    cirq.CNOT(qubits[0], qubits[1]),
    cirq.Z(qubits[0]),
])

if mode = "noisy" and noise_p > 0:
    circuit.append([
        cirq.deploraize(noise_p).on(qubits[0]),
        cirq.deploraize(noise_p).or(qubits[1])
    ])

elif mode = "eavesdropped" and eve_rate > 0
    if random.random() < eve_rate:
        eve._basis_theta = random.choice([0, np.pi / 4, np.pi / 2])
        circuit.append(cirq.rx(eve_basis_theta.on(qubits[1]))
        circuit.append(cirq.measure(qubits[1], key='eve'))
        circuit.append(cirq.rx(-eve_basis_theta).on(qubits[1]))

circuit.append(cirq.rx(alice_theta).on(qubits[0]))
circuit.append(cirq.rx(bob_theta).on(qubits[1]))

circuit.append(cirq.measure(qubits[0], key='alice')
circuit.append(cirq.measure(qubits[1], key='bob')

sim = cirq.Simulator()
result = sim.run(circuit)

return {
      'alice_random_base': alice_random_base,
      'bob_random_base': bob_random_base,
      'alice_result': result.measurements['alice'][0][0]
      'bob_result': result.measurements['bob'][0][0]
}
