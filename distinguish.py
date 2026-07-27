from calibration import calibration
import scipy

def run_distinguish(num_rounds:int, comparison:str, tolerance:float, distinguish_rounds:int):
    fidelityDifferences = []

    for i in range(distinguish_rounds):
        noisyS, noisyKeyGeneration, noisyHist, noisyFidelity, eveS, eveKeyGeneration, eveHist, eveFidelity = calibration(comparison, tolerance, num_rounds)
        fidelityDifference = (noisyFidelity - eveFidelity)
        fidelityDifferences.append(fidelityDifference)

    fidelityWilcoxon = scipy.stats.wilcoxon(fidelityDifferences)
    return fidelityWilcoxon