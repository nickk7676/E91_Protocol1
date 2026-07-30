from calibration import calibration
import scipy

def run_distinguish_fixed_eve(num_rounds:int, comparison:str, tolerance:float, noise_strength:float):
    noisyS, noisyKeyGeneration, noisyFig, noisyError_a2b1, noisyError_a3b2, eveS, eveKeyGeneration, eveFig, eveError_a2b1, eveError_a3b2 = calibration(comparison, tolerance, num_rounds, noise_strength)
    return noisyFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2
    

def run_distinguish_random_eve(num_rounds:int, comparison:str, tolerance:float, noise_strength:float):
    noisyS, noisyKeyGeneration, noisyFig, noisyError_a2b1, noisyError_a3b2, eveS, eveKeyGeneration, eveFig, eveError_a2b1, eveError_a3b2 = calibration(comparison, tolerance, num_rounds, noise_strength)
    return noisyFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2

def run_distinguish_fixed_ancilla(num_rounds:int, comparison:str, tolerance:float, noise_strength:float, eve_strength:float):
    noisyS, noisyKeyGeneration, noisyFig, noisyError_a2b1, noisyError_a3b2, eveS, eveKeyGeneration, eveFig, eveError_a2b1, eveError_a3b2 = calibration(comparison, tolerance, num_rounds, noise_strength, eve_strength)
    return noisyFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2    