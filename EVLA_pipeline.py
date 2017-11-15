# ##############################################################################
#
# EVLA analysis for continuum observations at Ku band
# T. J. Hayashi
#
# 2017 June 13
#
# ##############################################################################
################################################################################
thesteps = [1,3]
# steps 10 and 11 can be skip

steptitle = {
    1: '[GENERAL] Output observation summary: listobs, plotants, vplot',
    2: '[GENERAL] A priori Antenna Position Corrections',
    3: '[GENERAL] Basic flagging & split & Hanning Smoothing',
    # ---------------------------------------------------
    4: '[FCAL] Advanced flagging for flux calibrator without applycal (FLAG bad channel)',
    5: '[FCAL] Calibration for flux calibrator (SETJY, CALIB, FRING, BPASS) 1st time',
    6: '[FCAL] Advanced flagging for flux calibrator (FLAG)',
    7: '[FCAL] Calibration for flux calibrator (CALIB, FRING, BPASS) 2nd time',
    # ---------------------------------------------------
    8: '[PCAL] Advanced Flagging for Phase Calibrator (FLAG bad channel)',
    9: '[PCAL] Calibration for Phase Calibrator (CALIB) and Fluxscaling (GETJY)',
    10: '[PCAL] Flagging for Fluxscale Table (FLAG)',
    # ---------------------------------------------------
    11: '[ALL] Applying the Calibration Table',
    12: '[ALL] Flagging for Target Sources (FLAG)',
    14: '[ALL] Split the ms and output fits (SPLIT)'
    }
################################################################################
print '___________________________________________________________________\n'
execfile('./py/settings.py')

# ==============================================================================
# define MS file
# ==============================================================================
mystep = 1
if(mystep in thesteps):
    print '___________________________________________________________________\n'
    print '+++ Step ', mystep, steptitle[mystep]

    default(listobs)
    vis       = msactive
    listfile  = logpath+'listobs.log'
    overwrite = True
    listobs()

    default(plotants)
    vis       = msactive
    figfile   = logpath+'plotants.png'
    plotants()

# ==============================================================================
# antenna position correction
# ==============================================================================
mystep = 2
if(mystep in thesteps):
    print '___________________________________________________________________\n'
    print '+++ Step ', mystep, steptitle[mystep]

    newAtable = 't.antpos'
    # delete old table
    if os.path.exists(newtable): os.system('rm -rf '+newAtable)

    default(gencal)
    vis               = msactive
    caltype, caltable  = 'antpos', newAtable
    gencal()

# ==============================================================================
# basic flagging -> split -> hannig smootth -> time sort
# ==============================================================================
mystep = 3
if(mystep in thesteps):
    print '___________________________________________________________________\n'
    print '+++ Step ', mystep, steptitle[mystep]

    # --------------------------------------------------------------------------
    # flag system scans
    default(flagdata)
    vis         = msactive
    scan        = systemscan
    correlation = 'ALL'
    inpmode     = 'manual'
    flagbackup  = False
    action      = 'apply'
    flagdata()

    # --------------------------------------------------------------------------
    # flag any
    default(flagcmd)
    vis         = msactive
    correlation = 'ALL'
    inpmode     = 'xml'
    flagbackup  = False
    #tbuff       = intTime
    reason      ='any'
    action      = 'apply'
    flagcmd()

    # --------------------------------------------------------------------------
    # flag shadow
    # [radius in meter] and [tolerated fraction in space]
    (radius, tolfrac) = (25, 0.1)
    tolerance   = radius-(radius**2*(1-tolfrac))**0.5
    default('flagdata')
    vis         = msactive
    spw         = SpwRange
    correlation = 'ALL'
    mode        = 'shadow'
    flagbackup  = False
    action      = 'apply'
    flagdata()

    # --------------------------------------------------------------------------
    # do zero flagging
    default('flagdata')
    vis         = msactive
    scan        = obsscan
    correlation = 'ABS_ALL'
    mode        = 'clip'
    clipzeros   = True
    flagbackup  = False
    action      = 'apply'
    flagdata()


    # file manegement
    msin      = msactive
    mssplit   = msactive.replace('.ms','.split.ms')
    flagin    = msin+'.flagversions'
    flagsplit = mssplit+'.flagversions'

    # --------------------------------------------------------------------------
    # split
    # if both files exist, then only leave original
    if os.path.exists(msin) and os.path.exists(mssplit):
        syscommand = 'rm -rf %s %s' % (mssplit, flagsplit)
        os.system(syscommand)

    default(split)
    (vis, outputvis) = (msin, mssplit)
    scan      = obsscan
    spw       = SpwRange
    correlation = 'rr,ll'
    datacolumn = 'data'
    split()

    # if both files exist, then only leave split
    if os.path.exists(msin) and os.path.exists(mssplit):
        syscommand = 'rm -rf %s %s' % (msin, flagin)
        os.system(syscommand)

    # --------------------------------------------------------------------------
    # hanning smooth
    default(hanningsmooth)
    (vis, outputvis) = (mssplit, msin)
    outputvis = msin
    scan  = obsscan
    spw   = SpwRange
    hanningsmooth()

    # --------------------------------------------------------------------------
    # time sort
    ms.open(msactive, nomodify=False)
    ms.timesort()
    mssorted   = msactive+'.sorted'
    if os.path.exists(mssorted):
        syscommand = 'mv %s %s' % (mssorted, msactive)
        os.system(syscommand)
    ms.done()

    default(flagmanager)
    vis  = msactive
    mode = 'save'
    versionname = 'myflag_start'
    flagmanager()


# ==============================================================================
# instant calibration for fcal
# ==============================================================================
mystep = 4
if(mystep in thesteps):
    print '___________________________________________________________________\n'
    print '+++ Step ', mystep, steptitle[mystep]

    newGtable = '_t.G0'
    newKtable = '_t.K0'
    newBtable = '_t.B0'
    for deltable in [newBtable,newKtable,newGtable]:
        if os.path.exists(deltable): os.system('rm -rf '+deltable+'*')
    ydatalist = ['amp','phase']

    # --------------------------------------------------------------------------
    # gain calibration
    default(gaincal)
    vis                 = msactive
    scan, spw           = obsscan, SpwRange
    docallib, callib    = True, callibpath+'callib-05-1_gaincal.dat'
    gaintype, calmode   = 'G', 'ap'
    caltable            = newGtable
    minsnr, minblperant = 5, 3
    refant              = refantname

    # fcal
    for i in xrange(len(fcal)):
        field     = fcal[i].get_field()
        solint    = fcal[i].get_solint()
        uvrange   = fcal[i].get_uvr()
        gaincal()
        append    = True

    # --------------------------------------------------------------------------
    # delay calibration
    default(gaincal)
    vis                 = msactive
    scan, spw           = obsscan, SpwRange
    docallib, callib    = True, callibpath+'callib-05-2_fring.dat'
    gaintype            = 'K'
    caltable            = newKtable
    minsnr, minblperant = 5, 3
    refant              = refantname

    field       = get_source(fcal)
    uvrange     = ''
    solint      = 'inf'
    combine     = 'scan'
    gaincal()

    # --------------------------------------------------------------------------
    # bandpass
    default(bandpass)
    vis                 = msactive
    scan, spw           = obsscan, SpwRange
    docallib, callib    = True, callibpath+'callib-05-3_bandpass.dat'
    bandtype            = 'B'
    caltable            = newBtable
    solnorm             = True
    minsnr, minblperant = 5, 3
    refant              = refantname

    field       = get_source(fcal)
    uvrange     = ''
    solint      = 'inf'
    combine     = 'scan'
    bandpass()

    # --------------------------------------------------------------------------
    if os.path.exists(newGtable): os.system('rm -rf '+newGtable)
    # gain calibration
    default(gaincal)
    vis                 = msactive
    scan, spw           = obsscan, SpwRange
    docallib, callib    = True, callibpath+'callib-05-4_gaincal.dat'
    gaintype, calmode   = 'G', 'ap'
    caltable            = newGtable
    minsnr, minblperant = 5, 3
    refant              = refantname

    # fcal
    for i in xrange(len(fcal)):
        field     = fcal[i].get_field()
        solint    = fcal[i].get_solint()
        uvrange   = fcal[i].get_uvr()
        gaincal()
        append    = True

    # --------------------------------------------------------------------------
    # SNPLOT
    # param for plotresult (5: BP, 6:SN, 7:Delay)
    theplot = [6]
    tableactive = newGtable
    plotamp, plotphase  = True, True
    plotsource = fcal
    execfile(pipepath+'plot_plotcal.py')

    # SNPLOT BP
    # param for plotresult (5: BP, 6:SN, 7:Delay)
    theplot = [5]
    tableactive = newBtable
    plotamp, plotphase  = True, True
    plotsource = fcal
    execfile(pipepath+'plot_plotcal.py')

    # SNPLOT Delay
    # param for plotresult (5: BP, 6:SN, 7:Delay)
    theplot = [7]
    tableactive = newKtable
    plotsource = fcal
    execfile(pipepath+'plot_plotcal.py')
    # --------------------------------------------------------------------------
    # plot result
    theplot = [1]
    plotamp, plotphase  = True, True
    callibread = callibpath+'callib-05-6_plotms.dat'
    plotsource = fcal
    execfile(pipepath+'plot_plotms.py')

    # param for plotresult (1:possm, 2:uvplot, 3:vplot)
    theplot = [2]
    plotamp   = True
    plotphase = False
    callibread = callibpath+'callib-05-6_plotms.dat'
    plotsource = fcal
    execfile(pipepath+'plot_plotms.py')

# ==============================================================================
# flag
# ==============================================================================



# ==============================================================================
# END
# ==============================================================================
mystep = np.max(thesteps)
