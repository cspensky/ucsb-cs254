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
time_dict = {}
for data in freq_vdd:
    time = 1.0/data[0]
    energy = data[2] + .3 * data[1] * time
    y.append(energy)
    x.append(time)

    if time not in time_dict:
        time_dict[time] = []

    time_dict[time].append(energy)

# Get our optimal power plot
min_energy = []
for f in x:
    print time_dict[f]
    min_p = min(time_dict[f])
    print min_p
    min_energy.append(min_p)

print min_energy
# Get our optimal points
pareto_optimal_time = []
paraeto_optimal_energy = []
for idx in range(len(x)):
    f = x[idx]
    power = min_energy[idx]

    # If its the same power and higher freq., it's strictly better
    try:
        power_idx = paraeto_optimal_energy.index(power)
        if time_dict < pareto_optimal_freq[power_idx]:
            pareto_optimal_time[power_idx] = f
    except:
        pareto_optimal_time.append(f)
        paraeto_optimal_energy.append(power)

# Plot our graph
plt.scatter(x, y)
plt.plot(pareto_optimal_time, paraeto_optimal_energy, "*-", label="Optimal")
plt.title("Energy vs. Time")
plt.ylabel("Energy (Joules)")
plt.xlabel("Time (Seconds)")
plt.legend(loc="upper right")
plt.savefig('power_perf.png')

# Figure out the minimal energy
instructions = 1000000000
min_joules = []
for f in time_dict:
    ins_sec = f * 1000000000.0
    min_p = min(time_dict[f])
    energy = min_p

    time_per_core = instructions / ins_sec

    time_per_core = f
    # print "Time per core @ %1.1fGhz: %f" % (f, time_per_core)

    # How many cores?
    cores = 1
    while time_per_core / cores > .1:
        cores += 1

    # How much energy? (*cores/cores cancel out)
    joules = energy * time_per_core

    # print "Use %d cores and %f Jouels" % (cores, joules)

    min_joules.append((1/f, cores, joules))

for t in sorted(min_joules, key=lambda x: x[2]):

    # print "%d cores at %1.1f GHz uses %f J"% (t[1],t[0],t[2])

    print "%d & %1.1f & %f \\\\\hline"% (t[1],t[0],t[2])
