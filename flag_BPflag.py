import numpy as np
import shutil
import sys
# for plot
#import os
#from time import sleep
from pylab import *
from matplotlib import pyplot as plt

######################################################################
# set procedure
theproc = [0,1,2,3,4,5,6,7]
proctitle = {
    0: 'reset output flag list',
    1: 'flag based on phase',
    2: 'flag based on phase stat.',
    3: 'flag based on amp.',
    4: 'flag based on amp. stat.',
    5: 'record result to the table',
    6: 'output result with plotcal',
    7: 'flag data using output file (only stat)'
    }

# constant
polnDict = {0:'R',1:'L'}

# parameter
pSNcutoff     = 5
aSNcutoff     = 7
pstatSNcutoff = 5
astatSNcutoff = 7
pmonoSNcutoff = 7
amonoSNcutoff = 7
aLimitMin     = 0.5
aLimitMax     = 2.0
iterr4chan    = 3
iterr4stats   = 2
# for evaluating the program
plotflag      = F
######################################################################

# file manegement
table       = '_t.B0'
backup      = table+".bak"
if not os.path.exists(backup):
    shutil.copytree(table, backup)
else:
    syscommand='rm -rf '+table
    os.system(syscommand)
    shutil.copytree(backup, table)

# ca: open table
ca.open(table)
antList    = ca.antenna()
antNum     = len(antList)
spwNum     = ca.numspw()
chanNum    = np.max(ca.numchannel())
plotsource = ca.field()
msName     = ca.msname()
ca.close()

# tb: open table
tb.open(table)
flag = tb.getcol('FLAG')
data = tb.getcol('CPARAM')
tb.close()

# setting
flagnchan   = 0
flagnspw    = 0

# function
def judge_monotone(a):
    sum = 0
    for i in range(len(a)-2):
        if((a[i]-a[i+1])*(a[i+1]-a[i+2]) < 0):
            j = 0
            while(((a[i]-a[i+1])*(a[i+j+1]-a[i+j+2]) < 0) and (i+2+j < len(a)-2)):
                sum = sum + pow(a[i+j+1]-a[i+j+2],2)
                j = j+1
    return sum

# ==============================================================================
# file: open outfile
# ==============================================================================
myproc=0
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    outfilename = './log/flag_Blist.txt'
    if os.path.exists(outfilename):
        os.remove(outfilename)
    fp = open(outfilename, 'w')


# ==============================================================================
# flag based phase std for each [antenna][spw][polIdx]
# ==============================================================================
myproc=1
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    dataStd = []
    dataAnt = []
    dataSpc = []
    dataPol = []
    dataMono = []
    for antIdx in range(antNum): # eaN where N is antIdx+1
        for spcIdx in range(spwNum):
            for polIdx in range(2):
#                print 'ant: %s-%s, spw: %2d' % (antList[antIdx], polIdx, spcIdx)
                for i in range(iterr4chan):
                    # copy unflaged data
                    tmpdata = []
                    tmpchan = []
                    for chnIdx in range(chanNum):
                        if(flag[polIdx][chnIdx][spcIdx*antNum+antIdx] == False):
                            tmpdata.append(np.angle(data[polIdx][chnIdx][spcIdx*antNum+antIdx]))
                            tmpchan.append(chnIdx)
                        elif(i == 0):
                            outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d:%2d\' reason=\'B0_NOSOLUTION\'\n'\
                             % (antList[antIdx], polnDict[polIdx], polnDict[polIdx], spcIdx, chnIdx)
                            fp.write(outstr)
                    # get statistics for unflaged data
                    if(tmpdata != []):
                        max  = np.max(tmpdata)
                        min  = np.min(tmpdata)
                        mean = np.mean(tmpdata)
                        std  = np.std(tmpdata)
                        #print '   max  : %6.2f' % (max*180/np.pi)
                        #print '   min  : %6.2f' % (min*180/np.pi)
                        #print '   mean : %6.2f' % (mean*180/np.pi)
                        #print '   std. : %6.2f' % (std*180/np.pi)
                        for chnIdx in range(len(tmpdata)):
                            # flagging bad data
                            tmpdata[chnIdx] = tmpdata[chnIdx] - mean
                        if(i == 0):
                            dataMono.append(judge_monotone(tmpdata))
                        elif(i == iterr4chan-1):
                            dataStd.append(std)
                            dataAnt.append(antIdx)
                            dataSpc.append(spcIdx)
                            dataPol.append(polIdx)
                        # loop for [channel] to find bad channel
                        for chnIdx in range(len(tmpdata)):
                            # flagging bad data
                            SN    = tmpdata[chnIdx]/std
                            if(np.abs(SN) > pSNcutoff):
#                                print '      chan: %2d, phase: %6.2f, SN: %4.1f' % (tmpchan[chnIdx], value*180/np.pi, SN)
                                flag[polIdx][tmpchan[chnIdx]][spcIdx*antNum+antIdx] = True
                                flagnchan = flagnchan + 1
                                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d:%2d\' reason=\'B0_PHAS\'\n'\
                                 % (antList[antIdx],polnDict[polIdx],polnDict[polIdx], spcIdx, tmpchan[chnIdx])
                                fp.write(outstr)


# ==============================================================================
# flag based phase stat.
# ==============================================================================
myproc=2
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]

    print '\n ## Flag by phase statistics'
    for j in range(iterr4stats):
        max  = np.max(dataStd)
        min  = np.min(dataStd)
        mean = np.mean(dataStd)
        std  = np.std(dataStd)
        print '   max  : %6.2f' % (max*180/np.pi)
        print '   min  : %6.2f' % (min*180/np.pi)
        print '   mean : %6.2f' % (mean*180/np.pi)
        print '   std. : %6.2f' % (std*180/np.pi)
        print '   ----------------------'
        for i in range(len(dataStd)):
            value = dataStd[i]
            SN    = (value-mean)/std
            if(np.abs(SN) > pstatSNcutoff):
                print '      ant: %s-%s, spw: %2d' % (antList[dataAnt[i]], dataPol[i], dataSpc[i])
                print '      std.: %6.2f, SN: %5.2f' % (value*180/np.pi, SN)
                print '      ----------------------'
                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d\' reason=\'B0_STAT\'\n'\
                 % (antList[dataAnt[i]], polnDict[dataPol[i]], polnDict[dataPol[i]], dataSpc[i])
                fp.write(outstr)
                dataStd[i] = mean
                for chnIdx in range(chanNum):
                    flag[dataPol[i]][chnIdx][dataSpc[i]*antNum+dataAnt[i]] = True
                flagnspw = flagnspw + 1

    print '\n ## Flag by phase monotone'
    for j in range(iterr4stats):
        max  = np.max(dataMono)
        min  = np.min(dataMono)
        mean = np.mean(dataMono)
        std  = np.std(dataMono)
#        print '   max  :  %3d' % (max)
#        print '   min  :  %3d' % (min)
        print '   max  : %4.1f' % (max*180/np.pi)
        print '   min  : %4.1f' % (min*180/np.pi)
        print '   mean : %4.1f' % (mean*180/np.pi)
        print '   std. : %4.1f' % (std*180/np.pi)
        print '   ----------------------'
        for i in range(len(dataMono)):
            value = dataMono[i]
            SN    = (value-mean)/std
            if(np.abs(SN) > pmonoSNcutoff):
                print '      ant: %s-%s, spw: %2d' % (antList[dataAnt[i]], dataPol[i], dataSpc[i])
                print '      mon.: %4d, SN: %5.2f' % (value, SN)
                print '      ----------------------'
                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d\' reason=\'B0_STAT\'\n'\
                 % (antList[dataAnt[i]], polnDict[dataPol[i]], polnDict[dataPol[i]], dataSpc[i])
                fp.write(outstr)
                dataMono[i] = mean
                for chnIdx in range(chanNum):
                    flag[dataPol[i]][chnIdx][dataSpc[i]*antNum+dataAnt[i]] = True
                flagnspw = flagnspw + 1


# ==============================================================================
# flag based amp for each [antenna][spw][polIdx]
# ==============================================================================
myproc=3
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    dataStd = []
    dataAnt = []
    dataSpc = []
    dataPol = []
    dataMono= []
    for antIdx in range(antNum): # eaN where N is antIdx+1
        for spcIdx in range(spwNum):
            for polIdx in range(2):
#                print 'ant: %s-%s, spw: %2d' % (antList[antIdx], polIdx, spcIdx)
                for i in range(iterr4chan):
                    # copy unflaged data
                    tmpdata = []
                    tmpchan = []
                    tmpdata4fit = []
                    tmpchan4fit = []
                    for chnIdx in range(chanNum):
                        if(flag[polIdx][chnIdx][spcIdx*antNum+antIdx] == False):
                            tmpdata.append(np.abs(data[polIdx][chnIdx][spcIdx*antNum+antIdx]))
                            tmpchan.append(chnIdx)
                            if(chnIdx > chanNum/20 and chnIdx < chanNum*19/20):
                                tmpdata4fit.append(np.abs(data[polIdx][chnIdx][spcIdx*antNum+antIdx]))
                                tmpchan4fit.append(chnIdx)
                            # weight
                            if(chnIdx > chanNum/8 and chnIdx < chanNum*7/8):
                                tmpdata4fit.append(np.abs(data[polIdx][chnIdx][spcIdx*antNum+antIdx]))
                                tmpchan4fit.append(chnIdx)
                            if(chnIdx > chanNum/4 and chnIdx < chanNum*3/4):
                                tmpdata4fit.append(np.abs(data[polIdx][chnIdx][spcIdx*antNum+antIdx]))
                                tmpchan4fit.append(chnIdx)
                    # loop for [channel] to find bad channel
                    for chnIdx in range(len(tmpdata)):
                        # flagging bad data below threshold
                        if(tmpdata[chnIdx] < aLimitMin):
#                            print '      chan: %2d, amp.: %6.2f  [less than MIN]' % (tmpchan[chnIdx], tmpdata[chnIdx])
                            flag[polIdx][tmpchan[chnIdx]][spcIdx*antNum+antIdx] = True
                            flagnchan = flagnchan + 1
                            outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d:%2d\' reason=\'B0_AMP\'\n'\
                             % (antList[antIdx], polnDict[polIdx], polnDict[polIdx], spcIdx, tmpchan[chnIdx])
                            fp.write(outstr)
                        elif(tmpdata[chnIdx] > aLimitMax):
#                            print '      chan: %2d, amp.: %6.2f  [more than MAX]' % (tmpchan[chnIdx], tmpdata[chnIdx])
                            flag[polIdx][tmpchan[chnIdx]][spcIdx*antNum+antIdx] = True
                            flagnchan = flagnchan + 1
                            outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d:%2d\' reason=\'B0_AMP\'\n'\
                             % (antList[antIdx], polnDict[polIdx], polnDict[polIdx], spcIdx, tmpchan[chnIdx])
                            fp.write(outstr)
                    # get statistics for unflaged data
                    if(tmpdata != []):
                        # fitting
                        func = np.poly1d(np.polyfit(tmpchan4fit, tmpdata4fit, 4))
                        # loop for plot result
                        if(plotflag == T and (i == 0 or i == iterr4chan-1)):
                            axis([0,chanNum-1,0,2])
                            plt.scatter(tmpchan,tmpdata)
                            plt.plot(tmpchan,func(tmpchan))
                            plt.savefig('./log/plotcal-bpplot/'+antList[antIdx]+'_'+str(spcIdx)+'_'+str(polIdx)+'_'+str(i)+'.png')
                            plt.close()
                        # get resigual
                        for chnIdx in range(len(tmpdata)):
                            tmpdata[chnIdx] = tmpdata[chnIdx]-func(tmpchan[chnIdx])
                        # evaluation monotone
                        if(i == 0):
                            dataMono.append(judge_monotone(tmpdata))
                        # loop for [channnel] to get statistics of specific [antenna][spw]
                        for chnIdx in range(len(tmpdata4fit)):
                            tmpdata4fit[chnIdx] = tmpdata4fit[chnIdx]-func(tmpchan4fit[chnIdx])
                        max  = np.max(tmpdata4fit)
                        min  = np.min(tmpdata4fit)
                        mean = np.mean(tmpdata4fit)
                        std  = np.std(tmpdata4fit)
                        if(i == 0):
                            dataStd.append(std)
                            dataAnt.append(antIdx)
                            dataSpc.append(spcIdx)
                            dataPol.append(polIdx)
                            #print '   max  : %6.2f' % (max)
                            #print '   min  : %6.2f' % (min)
                            #print '   mean : %6.2f' % (mean)
                            #print '   std. : %6.2f' % (std)
                        # loop for [channnel] to find bad channel
                        for chnIdx in range(len(tmpdata)):
                            # flagging bad data
                            SN    = tmpdata[chnIdx]/std
                            if(np.abs(SN) > aSNcutoff):
#                                print '      chan: %2d, amp.: %6.2f, SN: %4.1f' % (tmpchan[chnIdx], tmpdata[chnIdx]+func(tmpchan[chnIdx]), SN)
                                flag[polIdx][tmpchan[chnIdx]][spcIdx*antNum+antIdx] = True
                                flagnchan = flagnchan + 1
                                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d:%2d\' reason=\'B0_AMP\'\n'\
                                 % (antList[antIdx], polnDict[polIdx], polnDict[polIdx], spcIdx, tmpchan[chnIdx])
                                fp.write(outstr)

    #from matplotlib import pyplot as plt
    #plt.scatter(tmpchan,tmpdata)
    #plt.plot(tmpchan, np.poly1d(np.polyfit(tmpchan4fit, tmpdata4fit, 2))(tmpchan), label='d=1')
    #plt.close()

# ==============================================================================
# flag based amp stat.
# ==============================================================================
myproc=4
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]

    print '\n ## Flag by amp. statistics'
    for j in range(iterr4stats):
        max  = np.max(dataStd)
        min  = np.min(dataStd)
        mean = np.mean(dataStd)
        std  = np.std(dataStd)
        print '   max  : %6.4f' % (max)
        print '   min  : %6.4f' % (min)
        print '   mean : %6.4f' % (mean)
        print '   std. : %6.4f' % (std)
        print '   ----------------------'
        for i in range(len(dataStd)):
            value = dataStd[i]
            SN    = (value-mean)/std
            if(np.abs(SN) > astatSNcutoff):
                print '      ant: %s-%s, spw: %2d' % (antList[dataAnt[i]], dataPol[i], dataSpc[i])
                print '      std.: %6.4f, SN: %5.3f' % (value, SN)
                print '      ----------------------'
                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d\' reason=\'B0_STAT\'\n'\
                 % (antList[dataAnt[i]], polnDict[dataPol[i]], polnDict[dataPol[i]], dataSpc[i])
                fp.write(outstr)
                dataStd[i] = mean
                for chnIdx in range(chanNum):
                    flag[dataPol[i]][chnIdx][dataSpc[i]*antNum+dataAnt[i]] = True
                flagnspw = flagnspw + 1


    print '\n ## Flag by amp. monotone'
    for j in range(iterr4stats):
        max  = np.max(dataMono)
        min  = np.min(dataMono)
        mean = np.mean(dataMono)
        std  = np.std(dataMono)
#        print '   max  :  %3d' % (max)
#        print '   min  :  %3d' % (min)
        print '   max  : %6.4f' % (max)
        print '   min  : %6.4f' % (min)
        print '   mean : %6.4f' % (mean)
        print '   std. : %6.4f' % (std)
        print '   ----------------------'
        for i in range(len(dataMono)):
            value = dataMono[i]
            SN    = (value-mean)/std
            if(np.abs(SN) > amonoSNcutoff):
                print '      ant: %s-%s, spw: %2d' % (antList[dataAnt[i]], dataPol[i], dataSpc[i])
                print '      mon.: %4.2f, SN: %5.2f' % (value, SN)
                print '      ----------------------'
                outstr = 'antenna=\'%s&&*\' correlation=\'%1s%1s\' spw=\'%2d\' reason=\'B0_STAT\'\n'\
                 % (antList[dataAnt[i]], polnDict[dataPol[i]], polnDict[dataPol[i]], dataSpc[i])
                fp.write(outstr)
                dataMono[i] = mean
                for chnIdx in range(chanNum):
                    flag[dataPol[i]][chnIdx][dataSpc[i]*antNum+dataAnt[i]] = True
                flagnspw = flagnspw + 1

# ==============================================================================
# flag
# ==============================================================================
print '\n ### End of the checking'
print ' ### flagged number of channel : %4d' % flagnchan
print ' ### flagged number of spw     : %4d' % flagnspw

myproc=5
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    tb.open(table, nomodify = False)
    tb.putcol("FLAG", flag)
    tb.flush()
    tb.close()

# ==============================================================================
# output file for flagcmd
# ==============================================================================
# sort
myproc=0
if(myproc in theproc):
    fp.close()
fp = open(outfilename, "r")
lines = fp.readlines()
fp.close()

fp = open(outfilename, "w")
lines_sorted = sorted(lines)
for outstr in lines_sorted:
    fp.write(outstr)
fp.close()


# ==============================================================================
# plot table
# ==============================================================================
myproc=6
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    # param for plotresult (1:possm, 2:uvplot, 3:vplot)
    theplot = [5]
    tableactive = '_t.B0'
    plotamp   = True
    plotphase = True
    callibread = ''
    plotsource = fcal
    execfile(pipepath+'pipe_plotms.py')

# ==============================================================================
# flagdata
# ==============================================================================
myproc=7
if(myproc in theproc):
    print '\n ### Proc ', myproc, proctitle[myproc]
    default(flagdata)
    vis     = msName
    mode    = 'list'
    inpfile = outfilename
    reason  = 'B0_STAT'
    action  = 'apply'
    display = 'none'
    flagbackup = False
    flagdata()
