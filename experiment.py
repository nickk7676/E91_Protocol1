#what actually gets called in the terminal with arguments to run the experiment changing the number of rounds and the type of circuit as desired
if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    from analysis import run_experiment
    from distinguish import run_distinguish

    #Use arguments and assign them values
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuit", type=str, default="clean")
    parser.add_argument("--rounds", type=int, default=1000)
    parser.add_argument("--comparison", type=str, default=None)
    parser.add_argument("--tolerance", type=float, default=0)
    parser.add_argument("--distinguish_rounds", type=int, default=0)
    parser.add_argument("--noise_strength", type=float, default=0)
    args = parser.parse_args()
    circuit = args.circuit
    num_rounds = args.rounds
    comparison = args.comparison
    tolerance = args.tolerance
    distinguishRounds = args.distinguish_rounds
    noise_strength = args.noise_strength

    #Use arguments to run the experiment and show the values.
    if (comparison == None) or (tolerance == 0) or (distinguishRounds == 0):
        s, keyGeneration, hist, fidelity = run_experiment(num_rounds, circuit, noise_strength)
        print("CHSH S Value: ", s)
        print("Fidelty: ", fidelity)
        #Can become long depending on the number of rounds. Remove hashtag if want to see the key. 
        #print("Key: ", keyGeneration)
        plt.show()
    else:
        something = run_distinguish(num_rounds, comparison, tolerance, distinguishRounds)
