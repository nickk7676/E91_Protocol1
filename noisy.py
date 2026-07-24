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
