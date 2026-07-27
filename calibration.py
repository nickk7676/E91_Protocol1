#runs experiments until there is a matching S value between the noise and then attack
from analysis import run_experiment

def calibration(comparison:str, tolerance:float, num_rounds:int):
    s, keyGeneration, hist, fidelity = run_experiment(circuit ="noisy", )
    targetS = s
    eavesdroppingS=0
    if comparison == "naive_eve":
        while abs(targetS - eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, hist1, fidelity1 = run_experiment(comparison)
    if comparison == "ancilla_eve":
        while (targetS - eavesdroppingS) > tolerance:
            eavesdroppingS, keyGeneration1, hist1, fidelity1 = run_experiment(comparison)
    return s, keyGeneration, hist, fidelity, eavesdroppingS, keyGeneration1, hist1, fidelity1
