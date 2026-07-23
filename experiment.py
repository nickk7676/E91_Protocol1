#last bit that can be the code where we actually run experiments regardless of the circuit being used. 
from analysis import chshValue
from analysis import split_in_groups
from protocol import run_clean

def run_experiment(num_rounds):
    chsh_calculation = []
    keyGeneration = []
    for _ in range(num_rounds):
        result = run_clean()
        split_in_groups(result, chsh_calculation, keyGeneration)

    s = abs(chshValue(chsh_calculation))
    return s, keyGeneration