import random
#will be eve's naive intercept and resend attack (positive control)

alice_bases = {
    'a1' : 0,
    'a2' : np.pi/4,
     'a3' : np.pi/2
}

bob_bases = {
    'b1' : np.pi/4,
    'b2' : np.pi/2,
    'b3' : 3*np.pi/4
}

def run_naive():
    alice_random_base = random.choice(list(alice_bases.keys()))
    alice_theta = alice_bases[alice_random_base] 

    bob_random_base = random.choice(list(bob_bases.keys()))
    bob_theta = bob_bases[bob_random_base]


