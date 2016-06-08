from scipy.special import binom

binsum = 0
for i in range (16):
	binsum += binom(16, i)

print "Cycles for F:",
print 16*(2*.3**16*2+11*(1-.3**16*2-(2*(.7*.7)**16*binsum))+20*(2*(.7*.7)**16*binsum)+5)


E15 = 15*(2*.3**15*2+11*(1-.3**15*2-(2*(.7*.7)**15*binsum))+20*(2*(.7*.7)**15*binsum)+5)

print "Cycles for G:",
print 16*((.3**2*(4+E15)+22*(.3*.7)*2+.7**2*40) +10)


print "Cycles for H:",
print E15+ ((.3**2*4*+22*(.3*.7)*2+.7**2*40) +10)
# print .3**16*2+(.3*.7)**16*binsum+(1-.3**16*2-(.3*.7)**16*binsum)+5)
