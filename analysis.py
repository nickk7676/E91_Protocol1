from protocol import run_clean
from eve_naive import run_naive
import matplotlib.pyplot as plt

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

#Takes the result from the circuit measurement and then places it into a group depending whether the bases match or they do not. 
def split_in_groups(result, chsh_calculation, keyGeneration, occurrences):

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
    if (alice_random_base == 'a2' and bob_random_base == 'b1') or (alice_random_base == 'a3' and bob_random_base == 'b2') :
        keyGeneration.append(int(alice_result[0][0]))

        #Counting the number of occurrences that the states |00>, |01>, |10>, and |11> show up. 
        if alice_result[0][0] == 0 and bob_result[0][0] == 0:
            occurrences['00'] += 1
        elif alice_result[0][0] == 0 and bob_result[0][0] == 1:
            occurrences['01'] += 1
        elif alice_result[0][0] == 1 and bob_result[0][0] == 0:
            occurrences['10'] += 1
        else: 
            occurrences['11'] += 1
    else:
        chsh_calculation.append({
            'alice_random_base' : alice_random_base,
            'bob_random_base' : bob_random_base,
            'alice_outcome' : alice_outcome,
            'bob_outcome' : bob_outcome
        })


#Helper method to run the experiment based on the number of rounds and the type of circuit meant to be used. 
def run_experiment(num_rounds:int, circuit:str):
    occurrences = {'00': 0, '01': 0, '10': 0, '11': 0}
    chsh_calculation = []
    keyGeneration = []

    #Determines which method to run based off the circuit being used (changes whether eve exists on the circuit or not)
    for _ in range(num_rounds):
        if circuit == "clean":
            result = run_clean()
        elif circuit == "naive_eve":
            result = run_naive()

        #Takes the result from the method used and splits it into the key generation group or the chsh calculation group. 
        split_in_groups(result, chsh_calculation, keyGeneration, occurrences)

    #Creates historam data in dictionary format to be used with the state and then the number of occurrences it has within matching bases. 
    histogramData = {
        '|00>' : occurrences['00'],
        '|01>' : occurrences['01'],
        '|10>' : occurrences['10'],
        '|11>' : occurrences['11']
    }

    #Histogram plottnig
    hist = plt.bar(histogramData.keys(), histogramData.values(), edgecolor='black')
    hist = plt.xlabel("State")
    hist = plt.ylabel("Occurrences")
    hist = plt.title("Distribution of States in Protocol")

    #Calculate Fidelity (how likely the measurement of alice's entangled qubit directly anti-correlates to the bob's entangled qubit)
    fidelity = (occurrences['01'] + occurrences['10'])/(occurrences['00'] + occurrences['01'] + occurrences['10'] + occurrences['11'])

    #Sets 's' to be the CHSH S value after the calculation. 
    s = abs(chshValue(chsh_calculation))

    #Return the S value, the generated key, the histogram, and the fidelity. 
    return s, keyGeneration, hist, fidelity


