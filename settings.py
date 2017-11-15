# ==============================================================================
# import macro etc.
# ==============================================================================
import numpy as np
import scipy as scp
import math
from scipy import stats
execfile('./py/util_definition.py')
execfile('./py/util_function.py')
execfile('./py/util_directry.py')

# ==============================================================================
# visibility information
# ==============================================================================
print ' + MS information'
# MS file name
msactive='15B-261.oct18.ms'
print('   MS file name      : '+msactive)

# scans
systemscan = '2,3,4,6,7,17,18'
obsscan    = '1,5,8,9,10,11,12,13,14,15,16,19'

# polarization list
polList = ['R','L']
polNum  = len(polList)

# antenna information
antList  = get_ant(msactive)
antNum   = len(antList)
##print ' antenna list: %s' % antList
refantname = 'ea12'
print('   reference antenna : '+refantname)


# frequency and time information
minFreq, maxFreq, SpwRange, SpwList, ChanNum, intTime = get_frequency(msactive)
SpwNum = len(SpwList)
print '   frequency range   : %5.1f - %5.1f' % (minFreq, maxFreq)
print '   spw setting       : %s' % SpwRange
print '   integration time  : %3.1fs' % intTime

# ==============================================================================
# sources information
# ==============================================================================
print '\n + Source information'
# fcal
print ' ++ Flux calibrator'
fcal1 = Source('0137+331=3C48','0~60klambda','15s')
fcal  = [fcal1]
display_source(fcal)
fcalname = '3C48'
fcalband = 'U'

# pcal
print '\n ++ Phase calibrator'
pcal1 = Source('J2213-2529','0~300klambda','15s')
pcal  = [pcal1]
display_source(pcal)

# target
print '\n ++ Target'
targ1 = Source('21329-2346', '', '15s', pcal1)
targ2 = Source('22491-1808', '', '15s', pcal1)
targ  = [targ1, targ2]
display_source(targ)

# all sources
fpcal  = fcal + pcal
allsources = fcal + pcal + targ


