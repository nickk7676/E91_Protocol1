from protocol import run_clean
from eve_naive import run_naive
from noisy import run_noisy
import matplotlib.pyplot as plt
from eve_fixed_naive import run_fixed_naive
from eve_ancilla import run_fixed_eve_ancilla
from random_eve_ancilla import run_random_eve_ancilla


#Calculate the CHSH S value to determin
def chshValue(chsh_calculation):
    a1b1 = []
    a1b3 = []
    a3b1 = []
    a3b3 = []

    #Goes through all the entries in chsh_calculation list/dictionary
    for i in range(len(chsh_calculation)):

        #Makes an entry as a single dictionary and take store alice_base and bob_base into variables
        entry = chsh_calculation[i]
        alice_base = entry['alice_random_base']
        bob_base = entry['bob_random_base']

        #Find which group/list to append the outcome (+/- 1) based off alice and bob's bases. 
        if (alice_base == "a1" and bob_base == "b1") :
            a1b1.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome'],
            })
        elif (alice_base == "a1" and bob_base == "b3"):
            a1b3.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })
        elif (alice_base == "a3" and bob_base == "b1"):
            a3b1.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })
        elif (alice_base == "a3" and bob_base == "b3"):
            a3b3.append({
                'alice_outcome' : entry['alice_outcome'],
                'bob_outcome' : entry['bob_outcome']
            })

    #Calculate each correlation value for each group from the outcome values (+/- 1) that were grouped and found earlier. 
    total = 0
    for i in range(len(a1b1)):
        entry = a1b1[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a1b1_E = total/len(a1b1)

    total = 0
    for i in range(len(a1b3)):
        entry = a1b3[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a1b3_E = total/len(a1b3)

    total = 0
    for i in range(len(a3b1)):
        entry = a3b1[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a3b1_E = total/len(a3b1)

    total = 0
    for i in range(len(a3b3)):
        entry = a3b3[i]
        alice_outcome = entry['alice_outcome']
        bob_outcome = entry['bob_outcome']
        total = total + (alice_outcome*bob_outcome)
    a3b3_E = total/len(a3b3)

    #Calculate the final CHSH S value with the formula and then return it. 
    s = a1b1_E - a1b3_E + a3b1_E + a3b3_E 
    return s

def chshValue_by_strength(num_rounds):
    chsh_by_strength = {}
    strengths = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for eve_strength in strengths:
        chsh_calculation = []
        keyGeneration = []
        occurrences_a2b1 = {'00': 0, '01': 0, '10': 0, '11': 0}
        occurrences_a3b2 = {'00': 0, '01': 0, '10': 0, '11': 0}
        for _ in range(num_rounds):
            result = run_fixed_eve_ancilla(eve_strength)
            split_in_groups(result, chsh_calculation, keyGeneration, occurrences_a2b1, occurrences_a3b2)
        s = abs(chshValue(chsh_calculation))
        chsh_by_strength[eve_strength] = s
    return chsh_by_strength

def key_round_error(counts):
    total = sum(counts.values())
    if total ==0:
        return 0.0
    errors = counts.get('00', 0) + counts.get('11',0)
    return errors/total

#Takes the result from the circuit measurement and then places it into a group depending whether the bases match or they do not. 
def split_in_groups(result, chsh_calculation, keyGeneration, occurrences_a2b1, occurrences_a3b2):

    #Takes values from the result dictionary and puts them into variables within this method. 
    alice_result = result['alice_result']
    alice_random_base = result['alice_random_base']
    bob_result = result['bob_result']
    bob_random_base = result['bob_random_base']

    #Determines the outcome (+/- 1) depending on whether alice or bob measured 0 or 1. 
    if alice_result[0][0] == 0 :
        alice_outcome = 1
    else:
        alice_outcome = -1

    if bob_result[0][0] == 0 :
        bob_outcome = 1
    else:
        bob_outcome = -1

    #If the bases match, generate the key, and if they do not match, then take the necessary values and append it to the chsh_calculation list/dictionary containing values to be used in the CHSH S calculation.
    if (alice_random_base == 'a2' and bob_random_base =='b1'):
        keyGeneration.append(int(alice_result[0][0]))

        #Counting the number of occurrences that the states |00>, |01>, |10>, and |11> show up.
        if alice_result[0][0] == 0 and bob_result[0][0] == 0:
            occurrences_a2b1['00'] += 1
        elif alice_result[0][0] == 0 and bob_result[0][0] == 1:
            occurrences_a2b1['01'] += 1
        elif alice_result[0][0] == 1 and bob_result[0][0] == 0:
            occurrences_a2b1['10'] += 1
        else:
            occurrences_a2b1['11'] += 1

    elif (alice_random_base == 'a3' and bob_random_base == 'b2') :
        keyGeneration.append(int(alice_result[0][0]))

        #Counting the number of occurrences that the states |00>, |01>, |10>, and |11> show up.
        if alice_result[0][0] == 0 and bob_result[0][0] == 0:
            occurrences_a3b2['00'] += 1
        elif alice_result[0][0] == 0 and bob_result[0][0] == 1:
            occurrences_a3b2['01'] += 1
        elif alice_result[0][0] == 1 and bob_result[0][0] == 0:
            occurrences_a3b2['10'] += 1
        else:
            occurrences_a3b2['11'] += 1

    else:
        chsh_calculation.append({
            'alice_random_base' : alice_random_base,
            'bob_random_base' : bob_random_base,
            'alice_outcome' : alice_outcome,
            'bob_outcome' : bob_outcome
        })


#Helper method to run the experiment based on the number of rounds and the type of circuit meant to be used. 
def run_experiment(num_rounds:int, circuit:str, noise_strength:float, eve_strength:float):
    occurrences_a2b1 = {'00': 0, '01': 0, '10': 0, '11': 0}
    occurrences_a3b2 = {'00': 0, '01': 0, '10': 0, '11': 0}
    chsh_calculation = []
    keyGeneration = []

    #Determines which method to run based off the circuit being used (changes whether eve exists on the circuit or not)
    for _ in range(num_rounds):
        if circuit == "clean":
            result = run_clean()
        elif circuit == "naive_eve":
            result = run_naive()
        elif circuit == "noisy":
            result = run_noisy(noise_strength)
        elif circuit == "fixed_naive_eve":
            result = run_fixed_naive()
        elif circuit == "fixed_ancilla_eve":
            result = run_fixed_eve_ancilla(eve_strength)
        elif circuit == "random_ancilla_eve":
            result = run_random_eve_ancilla(eve_strength)

        #Takes the result from the method used and splits it into the key generation group or the chsh calculation group. 
        split_in_groups(result, chsh_calculation, keyGeneration, occurrences_a2b1, occurrences_a3b2)

    #Creates historam data in dictionary format to be used with the state and then the number of occurrences it has within matching bases. 
    histogramData_a2b1 = {
        '|00>' : occurrences_a2b1['00'],
        '|01>' : occurrences_a2b1['01'],
        '|10>' : occurrences_a2b1['10'],
        '|11>' : occurrences_a2b1['11']
    }

    #Creates historam data in dictionary format to be used with the state and then the number of occurrences it has within matching bases. 
    histogramData_a3b2 = {
        '|00>' : occurrences_a3b2['00'],
        '|01>' : occurrences_a3b2['01'],
        '|10>' : occurrences_a3b2['10'],
        '|11>' : occurrences_a3b2['11']
    }

    #Human-readable label for which circuit produced this data, used to title the histograms below.
    circuit_labels = {
        'clean': 'Clean Circuit',
        'naive_eve': 'Naive Eve Circuit',
        'fixed_naive_eve': 'Fixed Naive Eve Circuit',
        'ancilla_eve': 'Ancilla Eve Circuit',
        'noisy': 'Noisy Circuit',
        'fixed_ancilla_eve': 'Fixed Ancilla Eve'
    }
    circuit_label = circuit_labels.get(circuit, circuit)

    #Histogram plotting - side by side subplots so both are visible at once
    fig, (ax_a2b1, ax_a3b2) = plt.subplots(1, 2, figsize=(10, 4))
    fig.suptitle(circuit_label)

    hist_a2b1 = ax_a2b1.bar(histogramData_a2b1.keys(), histogramData_a2b1.values(), edgecolor='black')
    ax_a2b1.set_xlabel("State")
    ax_a2b1.set_ylabel("Occurrences")
    ax_a2b1.set_title("Distribution of States in Protocol Using A2-B1 Bases")

    hist_a3b2 = ax_a3b2.bar(histogramData_a3b2.keys(), histogramData_a3b2.values(), edgecolor='black')
    ax_a3b2.set_xlabel("State")
    ax_a3b2.set_ylabel("Occurrences")
    ax_a3b2.set_title("Distribution of States in Protocol Using A3-B2 Bases")

    fig.tight_layout()

    #Sets 's' to be the CHSH S value after the calculation. 
    s = abs(chshValue(chsh_calculation))


    #Calculate the error between a2b1 and a3b2
    error_a2b1 = key_round_error(occurrences_a2b1)
    error_a3b2 = key_round_error(occurrences_a3b2)

    #Return the S value, the generated key, the histogram, and errors.
    return s, keyGeneration, fig, error_a2b1, error_a3b2

