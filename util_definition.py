# ==============================================================================
# get source information
# ==============================================================================
class DummyClass(): pass

class Source:
    fieldname     = ''
    pcalclass     = ''

    def __init__(self, name, uvr='', inttime='60s', pcal=DummyClass):
        self.fieldname = name
        self.uvrange   = uvr
        self.inttime   = inttime
        self.pcalclass = pcal

    def display(self):
        print('  + '+self.fieldname)
        print '      int:%4s, uvr:%15s' % (self.inttime, self.uvrange)
        if self.pcalclass != DummyClass:
             print ('      pcal  : '+self.pcalclass.fieldname)

    def get_field(self):
        return str(self.fieldname)

    def get_solint(self):
        return str(self.inttime)

    def get_uvr(self):
        return str(self.uvrange)

    def get_pcal(self, output):
        return self.pcalclass.get(output)

    def get(self, output):
        if output == 'fieldname':
            return str(self.fieldname)
        elif output == 'scan':
            return str(self.scan)
        elif output == 'pcal':
            return str(self.pcalclass)
        elif output == 'solint':
            return str(self.inttime)
        elif output == 'uvr':
            return str(self.uvrange)

def display_source(cl):
    for i in xrange(len(cl)):
        cl[i].display()

def get_source(cl):
    tmp = ''
    for i in xrange(len(cl)):
        if i != 0:
            tmp = tmp + ','
        tmp = tmp + cl[i].get_field()
    tmp = tmp.replace('\',\'',',')
    return tmp

# usage
# get_targ(targ, pcal[0])
def get_targ(groupTarg, classPcal):
    groupTargMatch = []
    for i in xrange(len(groupTarg)):
        if(groupTarg[i].get_pcal(output) == classPcal.get_field):
            groupTargMatch.append(groupTarg[i])
    return get_source(groupTargMatch, output)

# ==============================================================================
# get antenna information
# ==============================================================================
def get_ant(vis):
    tb.open( '%s/ANTENNA' % vis)
    antList  = tb.getcol( 'NAME' )
    tb.close()
    return antList

# ==============================================================================
# get frequency information
# ==============================================================================
def get_frequency(vis):
    # load data
    ms.open(vis)
    ScanSummary = ms.getscansummary()
    SpwInfo = ms.getspectralwindowinfo()
    ms.close()

    # --------------------------------------------------------------------------
    # scan list
    # --------------------------------------------------------------------------
    intScanList = []
    for scanID in ScanSummary:
        intScanList.append(int(scanID))
    sortedScanList = sorted(intScanList)
    # find max and median integration times
    intTimes   = []
    SpwIdsList = []
    SpwNumList = []
    for iScan in sortedScanList:
        intTimes.append(ScanSummary[str(iScan)]['0']['IntegrationTime'])
    maximum_intTime = np.max(intTimes)
    intTime=maximum_intTime

    # --------------------------------------------------------------------------
    # channel
    # --------------------------------------------------------------------------
    intSpwList    = [int(SpwID) for SpwID in SpwInfo ]
    SpwListNum    = len(intSpwList)
    ChanWidthList = [ SpwInfo[str(iSpw)]['ChanWidth'] for iSpw in xrange(SpwListNum) ]
    numChanList   = [ SpwInfo[str(iSpw)]['NumChan']   for iSpw in xrange(SpwListNum) ]
    FreqList      = [ SpwInfo[str(iSpw)]['Chan1Freq'] for iSpw in xrange(SpwListNum) ]

    ChanNum   = int(np.median(numChanList))
    ChanWidth = np.median(ChanWidthList)
    spwWidth  = ChanWidth*ChanNum

    # get spw for observations
    medFreq = np.median(FreqList)
    for iSpw in xrange(SpwListNum):
        if getabs(medFreq - FreqList[iSpw]) < spwWidth:
            maxSpw, tmpFreq1 = iSpw, FreqList[iSpw]
            minSpw, tmpFreq2 = iSpw, FreqList[iSpw]
            break
    while (getabs(tmpFreq1 - FreqList[maxSpw+1]) < spwWidth+1.1 ):
        maxSpw += 1
        tmpFreq1 = FreqList[maxSpw]
        if maxSpw == SpwListNum -1:
            break
    while (getabs(tmpFreq2 - FreqList[minSpw-1]) < spwWidth+1.1 ):
        minSpw -= 1
        tmpFreq2 = FreqList[minSpw]
        if minSpw == 0:
            break

    #
    minFreq   = float(np.floor( min(tmpFreq1, tmpFreq2)/1e9*10)/10)
    maxFreq   = float(np.ceil( (max(tmpFreq1, tmpFreq2)+spwWidth)/1e9*10)/10)
    SpwRange  = str(minSpw)+'~'+str(maxSpw)
    SpwList   = range(minSpw, maxSpw+1)
    spwNum    = maxSpw-minSpw+1

    return minFreq, maxFreq, SpwRange, SpwList, ChanNum, intTime

