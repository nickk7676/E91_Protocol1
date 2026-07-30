#what actually gets called in the terminal with arguments to run the experiment changing the number of rounds and the type of circuit as desired
if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    import numpy as np
    from analysis import run_experiment
    from analysis import chshValue_by_strength
    from distinguish import run_distinguish_fixed_eve
    from distinguish import run_distinguish_random_eve
    from distinguish import run_distinguish_fixed_ancilla

    #Use arguments and assign them values
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuit", type=str, default=None)
    parser.add_argument("--rounds", type=int, default=1000)
    parser.add_argument("--comparison", type=str, default=None)
    parser.add_argument("--tolerance", type=float, default=0)
    parser.add_argument("--noise_strength", type=float, default=0)
    parser.add_argument("--eve_strength", type=float, default=1.0)
    args = parser.parse_args()
    circuit = args.circuit
    num_rounds = args.rounds
    comparison = args.comparison
    tolerance = args.tolerance
    noise_strength = args.noise_strength
    eve_strength = args.eve_strength

    #Use arguments to run the experiment and show the values.
    if (comparison == None) or (tolerance == 0):
        if (circuit == "fixed_ancilla_eve" and eve_strength == 6.7):
            chsh_by_strength = chshValue_by_strength(num_rounds)
            x_values = list(chsh_by_strength.keys())
            y_values = list(chsh_by_strength.values())
            plt.plot(x_values, y_values, marker='o')
            plt.xlabel('Eve Ancilla Strength')
            plt.ylabel('CHSH S Value')
            plt.title('CHSH S vs. Eve Ancilla Attack Strength')
            plt.axhline(y=2, color='r', linestyle='--', label= 'Tsirelson bound (S=2*sqrt(2))')
            plt.axhline(y=2*np.sqrt(2), color='g', linestyle='--', label='Tsirelson bound (S=2*sqrt(2))')
            plt.legend()
            plt.show()
        else:
            s, keyGeneration, fig, error_a2b1, error_a3b2= run_experiment(num_rounds, circuit, noise_strength, eve_strength)
            print("CHSH S Value: ", s)
            print("A2B1 Error: ", error_a2b1)
            print("A3B2 Error: ", error_a3b2)

        #Can become long depending on the number of rounds. Remove hashtag if want to see the key. 
        #print("Key: ", keyGeneration)
        plt.show()
    elif circuit == None:
        if (comparison == "fixed_naive_eve"):
            bothFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2 = run_distinguish_fixed_eve(num_rounds, comparison, tolerance, noise_strength)
            print("----------------------------Noisy Info---------------------")
            print("CHSH S Value: ", noisyS)
            print("A2B1 Error: ", noisyError_a2b1)
            print("A3B2 Error: ", noisyError_a3b2)
            print("---------------------------Eve Info------------------------")
            print("CHSH S Value: ", eveS)
            print("A2B1 Error: ", eveError_a2b1)
            print("A3B2 Error: ", eveError_a3b2)
            plt.show()
        elif (comparison == "naive_eve"):
            bothFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2 = run_distinguish_random_eve(num_rounds, comparison, tolerance, noise_strength)
            print("----------------------------Noisy Info---------------------")
            print("CHSH S Value: ", noisyS)
            print("A2B1 Error: ", noisyError_a2b1)
            print("A3B2 Error: ", noisyError_a3b2)
            print("---------------------------Eve Info------------------------")
            print("CHSH S Valeu: ", eveS)
            print("A2B1 Error: ", eveError_a2b1)
            print("A3B2 Error: ", eveError_a3b2)
            plt.show()  
        elif (comparison == "fixed_ancilla_eve"):
            bothFig, noisyS, noisyError_a2b1, noisyError_a3b2, eveS, eveError_a2b1, eveError_a3b2 = run_distinguish_fixed_ancilla(num_rounds, comparison, tolerance, noise_strength, eve_strength)
            print("----------------------------Noisy Info---------------------")
            print("CHSH S Value: ", noisyS)
            print("A2B1 Error: ", noisyError_a2b1)
            print("A3B2 Error: ", noisyError_a3b2)
            print("---------------------------Eve Info------------------------")
            print("CHSH S Valeu: ", eveS)
            print("A2B1 Error: ", eveError_a2b1)
            print("A3B2 Error: ", eveError_a3b2)
            plt.show()                       

