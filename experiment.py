#what actually gets called in the terminal with arguments to run the experiment changing the number of rounds and the type of circuit as desired
if __name__ == "__main__":
    import argparse
    import matplotlib.pyplot as plt
    from analysis import run_experiment

    #Use arguments and assign them values
    parser = argparse.ArgumentParser()
    parser.add_argument("--circuit", type=str, default="clean")
    parser.add_argument("--rounds", type=int, default=1000)
    args = parser.parse_args()
    circuit = args.circuit
    num_rounds = args.rounds

    #Use arguments to run the experiment and show the values.
    s, keyGeneration, hist, fidelity = run_experiment(num_rounds, circuit)
    print("CHSH S Value: ", s)
    print("Fidelty: ", fidelity)

    #Can become long depending on the number of rounds. Remove hashtag if want to see the key. 
    #print("Key: ", keyGeneration)

    plt.show()
