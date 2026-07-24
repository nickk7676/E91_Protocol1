from protocol import run_clean
import matplotlib.pyplot as plt

def chshValue(chsh_calculation):
    a1b1 = []
    a1b3 = []
    a3b1 = []
    a3b3 = []

    for i in range(len(chsh_calculation)):
        entry = chsh_calculation[i]
        alice_base = entry['alice_random_base']
        bob_base = entry['bob_random_base']
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

    s = a1b1_E - a1b3_E + a3b1_E + a3b3_E 
    return s


def split_in_groups(result, chsh_calculation, keyGeneration, occurrences):

    alice_result = result['alice_result']
    alice_random_base = result['alice_random_base']
    bob_result = result['bob_result']
    bob_random_base = result['bob_random_base']

    if alice_result[0][0] == 0 :
        alice_outcome = 1
    else:
        alice_outcome = -1

    if bob_result[0][0] == 0 :
        bob_outcome = 1
    else:
        bob_outcome = -1

    if (alice_random_base == 'a2' and bob_random_base == 'b1') or (alice_random_base == 'a3' and bob_random_base == 'b2') :
        keyGeneration.append(int(alice_result[0][0]))
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



def run_experiment(num_rounds):
    occurrences = {'00': 0, '01': 0, '10': 0, '11': 0}
    chsh_calculation = []
    keyGeneration = []

    for _ in range(num_rounds):
        result = run_clean()
        split_in_groups(result, chsh_calculation, keyGeneration, occurrences)

    histogramData = {
        '|00>' : occurrences['00'],
        '|01>' : occurrences['01'],
        '|10>' : occurrences['10'],
        '|11>' : occurrences['11']
    }
    hist = plt.bar(histogramData.keys(), histogramData.values(), edgecolor='black')
    hist = plt.xlabel("State")
    hist = plt.ylabel("Count")
    hist = plt.title("Distribution of States in Protocol")
    s = abs(chshValue(chsh_calculation))
    return s, keyGeneration, hist


