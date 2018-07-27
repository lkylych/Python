import random
import math


def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        # Start your code
        p = math.log(0.5) + math.log(self.emission[states[0]][sequence[0]])
        for n in range(len(sequence)-1):
            p = p + math.log(self.transition[states[n]][states[n+1]]) + math.log(self.emission[states[n+1]][sequence[n+1]])
        return p
        # End your code
        ###########################################


    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        states = [0,1]
        states[0] = []
        states[1] = []
        cost = [0,1]
        cost00 = math.log(0.5) + math.log(self.emission[0][sequence[0]])        #calculating initial log probabilities of: state 0 if previous state is 0
        cost10 = math.log(0.5) + math.log(self.emission[0][sequence[0]])        #state 0 if previous state is 1
        cost11 = math.log(0.5) + math.log(self.emission[1][sequence[0]])        #state 1 if previous state 1
        cost01 = math.log(0.5) + math.log(self.emission[1][sequence[0]])        #state 1 if previous state 0
        states[0].append(0)                                                     #initialization of lists with choises we make (state[0][n] = 1 means that for state number n if this state is 0 the best probability is 
        states[1].append(1)                                                     #derived if at all previous steps we choose states which gives best probability for state = 1 at position n-1, and so on)
        for n in range(len(sequence)-1):                                        #in loop we assemble lists of choises of states and list of probabilities (named cost)
            if (cost00 > cost10):
                if (cost11 > cost01):
                    states[1].append(1)
                    cost[1] = cost11
                else:
                    states[1].append(0)
                    cost[1] = cost01
                states[0].append(0)
                cost[0] = cost00
            else:
                states[0].append(1)
                cost[0] = cost10
                if (cost11 > cost01):
                    states[1].append(1)
                    cost[1] = cost11
                else:
                    states[1].append(0)
                    cost[1] = cost01
            cost00 = cost[0] + math.log(self.transition[0][0]) + math.log(self.emission[0][sequence[n+1]])  #updating log probabilities
            cost10 = cost[1] + math.log(self.transition[1][0]) + math.log(self.emission[0][sequence[n+1]])
            cost11 = cost[1] + math.log(self.transition[1][1]) + math.log(self.emission[1][sequence[n+1]])
            cost01 = cost[0] + math.log(self.transition[0][1]) + math.log(self.emission[1][sequence[n+1]])

        if cost[0] >= cost[1]:      #deciding 0 or 1 as a last state gives the best cost
            c = 0
        else:
            c = 1
        seqStates = []
        seqStates.append(c)        #append this best last state to the list
        for n in range(len(sequence)-1):    #calculating other best states from lists with decisions
            c = states[c][-(n)]
            seqStates.append(c)

        seqStates.reverse()  #revrse our list, as it was constructed from last state to first
        return seqStates

        # End your code
        ###########################################

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

sequence = read_sequence("small.txt")
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
print(logprob)


sequence = read_sequence("ecoli.txt")
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
print(logprob)

