
flagsource = fcal


for srcIdx in xrange(len(fcal)):
    ms.open(msactive, nomodify = False)
    ms.selectinit(datadescid = 0)
    staql={
        'field' : fcal[srcIdx].get_field(),
    }
    ms.msselect(staql, onlyparse=True)
    msdata = ms.getdata(['corrected_data','flag'])

    for polIdx in polNum:

    # modify rec['weight'] and rec['data'] values as desired
        ms.putdata(msdata)
    ms.close()

