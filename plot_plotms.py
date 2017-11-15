################################################################################
# set plotedure
plottitle = {
    1:'plot result (possm)',
    2:'plot result (uvplot)',
    3:'plot result (vplot)',
    4:'plot result (possm-RFI check)',
    }
if (plotamp == False):
    ydatalist = ['phase']
elif (plotphase == False):
    ydatalist = ['amp']
else:
    ydatalist = ['amp','phase']
################################################################################

# ==============================================================================
# Common settings for plotms
# ==============================================================================
default(plotms)
vis         = msactive
showgui     = False
overwrite   = True

# data column
scan        = obsscan
correlation = 'rr,ll'
spw         = SpwRange
if callibread=='':
    callib  = ['']
    ydatacolumn = 'data'
elif callibread is 'corrected':
    callib  = ['']
    ydatacolumn = 'corrected'
else:
    callib  = callibread
    ydatacolumn = 'corrected'

# Title, label etc.
highres     = True
(width, height)                   = (1580, 780)
(titlefont, xaxisfont, yaxisfont) = (8, 10, 10)

# axis
(xselfscale, xsharedaxis) = (True, True)
(yselfscale, ysharedaxis) = (True, True)

# ==============================================================================
# POSSM
# ==============================================================================
myplot = 1
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # spectral window and time range
    avgscan     = True
    (avgtime, avgchannel) = ('10000', '')

    # grid
    (gridrows, gridcols) = (8, 2)

    # axis
    (xaxis, yaxis) = ('freq', '')
    (coloraxis, iteraxis, exprange) = ('spw', 'baseline', 'all')

    # loop for plot each sourcce and y-axis
    for i in xrange(len(plotsource)):
        field   = plotsource[i].get_field()
        for yaxis in ydatalist:
            plotrange   = [minFreq, maxFreq, 0, 0]
            if yaxis is 'phase':
                plotrange   = [minFreq, maxFreq, -180, 180]
            title    = '%%yaxis%%'
            plotfile = possmpath+str(mystep)+'_'+field+'_'+yaxis+'.png'
            plotms()

# ==============================================================================
# UVPLOT
# ==============================================================================
myplot = 2
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # spectral window and time range
    spw         = SpwRange
    avgscan     = False
    (avgtime, avgchannel) = ('', str(numChan))

    # grid
    (gridrows, gridcols) = (2, 2)

    # axis
    (xaxis, yaxis) = ('uvwave', '')
    (xselfscale, xsharedaxis) = (True, True)
    (yselfscale, ysharedaxis) = (True, True)
    (coloraxis, iteraxis, exprange) = ('Antenna', 'spw', 'all')

    # loop for plot each sourcce and y-axis
    for i in xrange(len(plotsource)):
        field   = plotsource[i].get_field()
        for yaxis in ydatalist:
            plotrange   = []
            if yaxis == 'phase':
                plotrange   = [0, 0, -180, 180]
            title       = '%%yaxis%%'
            plotfile    = uvplotpath+str(mystep)+'_'+field+'_'+yaxis+'.png'
            plotms()

# ==============================================================================
# VPLOT
# ==============================================================================
myplot = 3
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # spectral window and time range
    avgscan     = False
    (avgtime, avgchannel) = (str(intTime*3), str(numChan))

    # grid
    (gridrows, gridcols) = (8, 2)

    # axis
    (xaxis, yaxis) = ('time', '')
    (coloraxis, iteraxis, exprange) = ('spw', 'baseline', 'all')
    plotrange   = []

    # loop for plot each y-axis
    field   = get_source(plotsource)
    for yaxis in ydatalist:
        plotrange   = []
        if yaxis == 'phase':
            plotrange   = [0,0,-180,180]
        title       = '%%yaxis%%'
        plotfile    = vplotpath+str(mystep)+'_'+yaxis+'.png'
        plotms()

# ==============================================================================
# RFI check
# ==============================================================================
myplot = 4
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # spectral window and time range
    avgscan     = False

    # grid
    (gridrows, gridcols) = (4, 2)

    # axis
    (xaxis, yaxis) = ('freq', 'amp')
    (coloraxis, iteraxis, exprange) = ('spw', 'Antenna', 'all')
    plotrange   = []
    symbolshape = 'circle'

    # loop for plot each sourcce and y-axis
    for i in xrange(len(plotsource)):
        field   = plotsource[i].get_field()
        for yaxis in ydatalist:
            plotrange   = [minFreq, maxFreq, 0, 0]
            if yaxis == 'phase':
                plotrange   = [minFreq, maxFreq, -180, 180]
            title       = '%%yaxis%%'
            plotfile    = possmpath+str(mystep)+'c_'+field+'_'+yaxis+'.png'
            plotms()

