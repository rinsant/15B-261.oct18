################################################################################
# set plotedure
plottitle = {
    5:'bpplot',
    6:'snplot',
    7:'delayplot'
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
vis         = tableactive
showgui     = False
overwrite   = True

# data column
field       = get_source(plotsource)
correlation = 'rr,ll'

# Title, label etc.
highres     = True
(width, height)                   = (1580, 780)
(titlefont, xaxisfont, yaxisfont) = (8, 10, 10)

# axis
(xselfscale, xsharedaxis) = (True, True)
(yselfscale, ysharedaxis) = (True, True)
showmajorgrid = True

# ==============================================================================
# BPPLOT
# ==============================================================================
myplot = 5
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # grid
    (gridrows, gridcols) = (4, 1)

    # axis
    (xaxis, yaxis) = ('freq', '')
    (coloraxis, iteraxis, exprange) = ('spw', 'Antenna', 'all')

    # loop for plot each sourcce and y-axis
    for correlation in polList:
        for yaxis in ydatalist:
            plotrange   = [minFreq, maxFreq, 0, 2]
            if yaxis == 'phase':
                plotrange   = [minFreq, maxFreq, -180, 180]
            title       = '%%yaxis%%'
            plotfile    = bpplotpath+str(mystep)+'_'+vis+'_'+correlation+'_'+yaxis+'.png'
            plotms()


# ==============================================================================
# SNPLOT
# ==============================================================================
myplot = 6
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    # grid
    (gridrows, gridcols) = (5, 2)

    # axis
    (xaxis, yaxis) = ('time', '')
    (coloraxis, iteraxis, exprange) = ('spw', 'antenna', 'all')
    customsymbol = True
    symbolshape = 'circle'
    symbolsize  = 5

    # loop for plot each y-axis
    for yaxis in ydatalist:
        for polName in polList:
            correlation = polName
            plotrange   = []
            if yaxis == 'phase':
                plotrange   = [0,0,-180,180]
            title       = '%%yaxis%%'
            plotfile    = snplotpath+str(mystep)+'_'+vis+'_'+yaxis+'_'+correlation+'.png'
            plotms()

# ==============================================================================
# Delay PLOT
# ==============================================================================
myplot = 7
if(myplot in theplot):
    print '\n  + Plot ', myplot, plottitle[myplot]

    correlation = ''

    # grid
    (gridrows, gridcols) = (2, 2)

    # axis
    (xaxis, yaxis) = ('antenna1', 'delay')
    (coloraxis, iteraxis, exprange) = ('corr', 'spw', 'all')
    customsymbol = True
    symbolshape = 'circle'
    symbolsize  = 10

    # loop for plot each y-axis
    plotrange   = []
    title       = '%%yaxis%%'
    plotfile    = delayplotpath+str(mystep)+'_'+vis+'.png'
    plotms()
