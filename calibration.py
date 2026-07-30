#runs experiments until there is a matching S value between the noise and then attack
from analysis import run_experiment
import matplotlib.pyplot as plt

def calibration(comparison:str, tolerance:float, num_rounds:int, noise_strength:float, eve_strength:float):
    s, keyGeneration, fig, error_a2b1, error_a3b2 = run_experiment(circuit ="noisy", num_rounds=num_rounds, noise_strength=noise_strength, eve_strength=eve_strength)
    targetS = s
    eavesdroppingS=0
    if comparison == "naive_eve":
        while abs(targetS - eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, fig1, eveError_a2b1, eveError_a3b2 = run_experiment(circuit=comparison, num_rounds=num_rounds, noise_strength=0, eve_strength=eve_strength)
            if abs(targetS - eavesdroppingS) > tolerance:
                plt.close(fig1)
    if comparison == "ancilla_eve":
        while abs(targetS - eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, fig1, eveError_a2b1, eveError_a3b2 = run_experiment(circuit=comparison, num_rounds=num_rounds, noise_strength=0, eve_strength=eve_strength)
            if abs(targetS - eavesdroppingS) > tolerance:
                plt.close(fig1)
    if comparison == "fixed_naive_eve":
        while abs(targetS-eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, fig1, eveError_a2b1, eveError_a3b2 = run_experiment(circuit=comparison, num_rounds=num_rounds, noise_strength=0, eve_strength=eve_strength)
            if abs(targetS - eavesdroppingS) > tolerance:
                plt.close(fig1)
    if comparison == "fixed_ancilla_eve":
        while abs(targetS-eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, fig1, eveError_a2b1, eveError_a3b2 = run_experiment(circuit=comparison, num_rounds=num_rounds, noise_strength=0, eve_strength=eve_strength)
            if abs(targetS - eavesdroppingS) > tolerance:
                plt.close(fig1)
    return s, keyGeneration, fig, error_a2b1, error_a3b2, eavesdroppingS, keyGeneration1, fig1, eveError_a2b1, eveError_a3b2
