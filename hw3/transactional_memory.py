import random

import numpy as np
import matplotlib.pyplot as plt

class Processor:

    def __init__(self, hash_size):
        self.hash_size = hash_size
        self.update()

    def update(self):
        self.hash_idx = random.randint(1,self.hash_size)
        self.instruction_count = random.randint(50,150)

    def get_hash_index(self):
        return self.hash_idx

    def get_instruction_count(self):
        return self.instruction_count


plot = {}
hash_sizes = [2, 5, 10,100,1000,10000,100000,1000000] #range(100,1000,10)

for processor_count in [1,2,4,16]:
    plot[processor_count] = []

    for hash_size in hash_sizes:

        # print hash_size
        processors = []
        # Init our processors
        for i in range(processor_count):
            processors.append(Processor(hash_size))

        # print processors
        # Do a bunch of trials
        trail_results = []
        collisions = 0
        for trial in range(10000):
            for p in processors:
                p.update()

            total_instructions = 0

            for x in range(len(processors)):

                # print processors[x].get_instruction_count()
                total_instructions += processors[x].get_instruction_count()

                if x+1 == len(processors):
                    break

                for y in range(x+1,len(processors)):
                    if processors[x].get_hash_index() == processors[y].get_hash_index():
                        # always assume the x thread was the second, it must redo everything and have a 20 ins penalty
                        # print total_instructions
                        total_instructions += processors[x].get_instruction_count() + 20
                        collisions += 1
                        # print total_instructions
                        # print "hash collision!"

            # print hash_size, processor_count, collisions

            # print total_instructions, hash_size, processor_count
            # print total_instructions
            transaction_per_section = processor_count*(1.0/(total_instructions/processor_count))*(2/1)*(1/.5)*(10.0**9)
            # print transaction_per_section
            trail_results.append(transaction_per_section)

        # print hash_size, processor_count, collisions, np.mean(trail_results)
        plot[processor_count].append([trail_results])
        # print plot[processor_count]
        # plot[(hash_size,processor_count)].append(transaction_per_section)

for processor_count in plot:
    # print len(plot[processor_count])
    results_y = [(np.mean(t)-40*10**6)/(40*10**6) for t in plot[processor_count]]
    print results_y
    # print hash_sizes
    # print results_y
    plt.plot(hash_sizes, results_y, "*-", label="%d Processor"%processor_count)

plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()
# print plot

# transaction_per_section = (1.0/update_instructions)*(.2/1)*(1/.5)*(10.0**9)
#
# print transaction_per_section
