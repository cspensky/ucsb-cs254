import matplotlib.pyplot as plt

# Import the shmoo plot
freq_vdd = [(2, .9, 1),
            (2, 1, 2),
            (2, 1.1, 2),
            (2, 1.2, 2),
            (2, 1.3, 4),

            (2.2, .9, 1),
            (2.2, 1, 2),
            (2.2, 1.1, 2),
            (2.2, 1.2, 3),
            (2.2, 1.3, 4),

            (2.4, .9, 1),
            (2.4, 1, 2),
            (2.4, 1.1, 3),
            (2.4, 1.2, 3),
            (2.4, 1.3, 5),

            (2.6, .9, 2),
            (2.6, 1, 2),
            (2.6, 1.1, 3),
            (2.6, 1.2, 4),
            (2.6, 1.3, 6),

            (2.8, .9, 2),
            (2.8, 1, 2),
            (2.8, 1.1, 3),
            (2.8, 1.2, 4),
            (2.8, 1.3, 6),

            (3, .9, 2),
            (3, 1, 3),
            (3, 1.1, 3),
            (3, 1.2, 4),
            (3, 1.3, 7),

            (3.2, 1, 3),
            (3.2, 1.1, 4),
            (3.2, 1.2, 5),
            (3.2, 1.3, 7),

            (3.4, 1, 3),
            (3.4, 1.1, 4),
            (3.4, 1.2, 5),
            (3.4, 1.3, 7),

            (3.6, 1, 3),
            (3.6, 1.1, 4),
            (3.6, 1.2, 5),
            (3.6, 1.3, 8),

            (3.8, 1, 3),
            (3.8, 1.1, 4),
            (3.8, 1.2, 5),
            (3.8, 1.3, 8),

            (4, 1.1, 4),
            (4, 1.2, 6),
            (4, 1.3, 9),

            (4.2, 1.2, 6),
            (4.2, 1.3, 9),

            (4.4, 1.2, 7),
            (4.4, 1.3, 10),

            (4.6, 1.3, 10),

            (4.8, 1.3, 10),

            (5, 1.3, 11),
            ]

x = []
y = []
freq = {}
for data in freq_vdd:
    y.append(data[2])
    x.append(data[0])

    if data[0] not in freq:
        freq[data[0]] = []

    freq[data[0]].append(data[2])

# Get our optimal power plot
min_power = []
for f in x:
    min_w = min(freq[f])
    min_power.append(min_w)

# Get our optimal points
pareto_optimal_freq = []
paraeto_optimal_power = []
for idx in range(len(x)):
    f = x[idx]
    power = min_power[idx]

    # If its the same power and higher freq., it's strictly better
    try:
        power_idx = paraeto_optimal_power.index(power)
        if freq > pareto_optimal_freq[power_idx]:
            pareto_optimal_freq[power_idx] = f
    except:
        pareto_optimal_freq.append(f)
        paraeto_optimal_power.append(power)

# Plot our graph
plt.scatter(x, y)
plt.plot(pareto_optimal_freq, paraeto_optimal_power, "*-", label="Optimal")
plt.title("Power vs. Frequency")
plt.ylabel("Power (Watts)")
plt.xlabel("Frequency (GHz)")
plt.legend(loc="upper left")
plt.savefig('power_perf.png')

# Figure out the minimal energy
instructions = 1000000000
min_joules = []
for f in freq:
    ins_sec = f * 1000000000.0
    min_w = min(freq[f])
    watts = min_w

    time_per_core = instructions / ins_sec

    # print "Time per core @ %1.1fGhz: %f" % (f, time_per_core)

    # How many cores?
    cores = 1
    while time_per_core / cores > .1:
        cores += 1

    # How much energy? (*cores/cores cancel out)
    joules = watts * time_per_core

    # print "Use %d cores and %f Jouels" % (cores, joules)

    min_joules.append((f, cores, joules))

for t in sorted(min_joules, key=lambda x: x[2]):

    # print "%d cores at %1.1f GHz uses %f J"% (t[1],t[0],t[2])

    print "%d & %1.1f & %f \\\\\hline"% (t[1],t[0],t[2])
