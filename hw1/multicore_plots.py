# Native
import math

import matplotlib.pyplot as plt


def perf(r):
    """
    :param r: resources
    :return: See the paper
    """
    return math.sqrt(r)


def speedup_sym(f, n, r, c):
    """

    :param f: fraction of code that is parallelizable
    :param n: number of cores
    :param r: resources
    :param c: overhead for serialization per thread
    :return:
    """
    return 1.0 / (
        ((1.0 - f + n * c) / perf(r)) +
        ((f * r) / (perf(r) * n))
    )


def speedup_asym(f, n, r, c):
    """

    :param f: fraction of code that is parallelizable
    :param n: number of cores
    :param r: resources
    :param c: overhead for serialization per thread
    :return:
    """
    return 1.0 / (
        ((1.0 - f + n * c) / perf(r)) +
        (f / (perf(r) + n - r))
    )


n = 256.0
c = .005  # .5%

speedup_plot_sym = {}
speedup_plot_sym_orig = {}
plot_tick = {.5: "+-",
             .9: "--",
             .975: "*-",
             .99: "^-",
             .999: "-",}
for f in [.5, .9, .975, .99, .999]:
    speedup_plot_sym[f] = []
    speedup_plot_sym_orig[f] = []
    for r_bce in range(1, 256):
        speedup_plot_sym[f].append(speedup_sym(f, n, r_bce, c))
        speedup_plot_sym_orig[f].append(speedup_sym(f, n, r_bce, 0))

    plt.plot(speedup_plot_sym[f], plot_tick[f], label="f=%0.3f" % f)
    plt.plot(speedup_plot_sym_orig[f], plot_tick[f], label="f=%0.3f (orig.)"
                                                           % f)
plt.title("Symmetric (n=%s, c=%s)" % (str(n), str(c)))
plt.xscale("log")
plt.xticks([2 ** x for x in range(9)], [str(2 ** x) for x in range(9)])
plt.xlim([0, 256])
plt.legend(loc="top left")
plt.ylabel("Speedup (symmetric)")
plt.xlabel("r BCEs")
plt.savefig('multicore_symmetric.png')


print "Sym/Orig: Max f = .99: %d"% speedup_plot_sym_orig[.99].index(max(
    speedup_plot_sym_orig[.99]))
print max(speedup_plot_sym_orig[.99])

print "Sym: Max f = .99: %d"% speedup_plot_sym[.99].index(max(speedup_plot_sym[
                                                              .99]))
print max(speedup_plot_sym[.99])


plt.figure()
speedup_plot_asym = {}
speedup_plot_asym_orig = {}
plot_tick = {.5: "+-",
             .9: "--",
             .975: "*-",
             .99: "^-",
             .999: "-",}
for f in [.5, .9, .975, .99, .999]:
    speedup_plot_asym[f] = []
    speedup_plot_asym_orig[f] = []
    for r_bce in range(1, 256):
        speedup_plot_asym[f].append(speedup_asym(f, n, r_bce, c))
        speedup_plot_asym_orig[f].append(speedup_asym(f, n, r_bce, 0))

    plt.plot(speedup_plot_asym[f], plot_tick[f], label="f=%0.3f" % f)
    plt.plot(speedup_plot_asym_orig[f], plot_tick[f], label="f=%0.3f (orig.)"
                                                           % f)
plt.title("Asymmetric (n=%s, c=%s)" % (str(n), str(c)))
plt.xscale("log")
plt.xticks([2 ** x for x in range(9)], [str(2 ** x) for x in range(9)])
plt.xlim([0, 256])
plt.legend(loc="top left")
plt.ylabel("Speedup (asymmetric)")
plt.xlabel("r BCEs")
plt.savefig('multicore_asymmetric.png')

print "ASym/Orig: Max f = .99: %d"% speedup_plot_asym_orig[.99].index(max(
    speedup_plot_asym_orig[.99]))
print max(speedup_plot_asym_orig[.99])

print "ASym: Max f = .99: %d"% speedup_plot_asym[.99].index(max(
    speedup_plot_asym[.99]))
print max(speedup_plot_asym[.99])