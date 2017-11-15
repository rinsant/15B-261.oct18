from callibrary import applycaltocallib as makecallib
# ##############################################################################
#
# EVLA analysis for continuum observations at Ku band
# T. J. Hayashi
#
# 2017 June 10
#
# ##############################################################################
thecals   = [1]
cal_title = {
    1: 'create callibrary'
    }
pipepath = './py/'
t_antpos    = '_t.antpos'
t_G0        = '_t.G0'
tmp_G1       = 'tmp.G1'
t_G1a       = '_t.G1.a'
t_G1p       = '_t.G1.p'
t_K         = '_t.K0'
t_B         = '_t.B0'
t_fluxscale = '_t.fluxscale'
set_spw  = SpwList
# ##############################################################################
def make_antpos(outfile,set_append=False):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_antpos, spwmap=[ 0 for iSpw in xrange(SpwNum)])
def make_G0(outfile, set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_G0, spwmap=set_spw, interp='linear')
def make_G1t(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=tmp_G1, spwmap=set_spw, interp='linear')
def make_G1a(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_G1a, spwmap=set_spw, interp='linear')
def make_G1p(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_G1p, spwmap=set_spw, interp='linear')
def make_K0(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_K, spwmap=set_spw, interp='linear')
def make_B0(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_B, spwmap=set_spw, interp='nearest,linear')
def make_fluxscale(outfile,set_append=True):
    makecallib(filename=outfile, append=set_append,
    gaintable=t_fluxscale, spwmap=set_spw, interp='linear')
######################################################################
#----------------- Delete old table
syscommand='rm -rf '+callibpath+'callib-*.dat'
os.system(syscommand)

#-----------------
mycal = 1
if(mycal in thecals):
    print '\n ++ Proc ', mycal, cal_title[mycal]

    tmp = callibpath+'callib-05-1_gaincal.dat'

    outlib = open(tmp, 'w')
    if os.path.exists(t_antpos):
        make_antpos(outfile=tmp, set_append=False)
    outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-05-2_fring.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_G0(outfile=tmp)

     else:
         make_G0(outfile=tmp, set_append=False)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-05-3_bandpass.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_G0(outfile=tmp)
     else:
         make_G0(outfile=tmp, set_append=False)

     make_K0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
    tmp = callibpath+'callib-05-4_gaincal.dat'
    outlib = open(tmp, 'w')

    if os.path.exists(t_antpos):
        make_antpos(outfile=tmp, set_append=False)
        make_K0(outfile=tmp)
    else:
        make_K0(outfile=tmp)
    make_B0(outfile=tmp)
    outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-05-6_plotms.dat'
     outlib = open(tmp, 'w')
     make_G0(outfile=tmp, set_append=False)
     make_K0(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-06_applycal.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_G0(outfile=tmp)
     else:
         make_G0(outfile=tmp, set_append=False)
     make_K0(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()


mycal = 1
if(mycal in thecals):
    tmp = callibpath+'callib-07-1_gaincal.dat'
    outlib = open(tmp, 'w')

    if os.path.exists(t_antpos):
        make_antpos(outfile=tmp, set_append=False)
        make_B0(outfile=tmp)
    else:
        make_B0(outfile=tmp)
    outlib.close()


mycal = 1
if(mycal in thecals):
    tmp = callibpath+'callib-07-2_fring.dat'
    outlib = open(tmp, 'w')

    if os.path.exists(t_antpos):
        make_antpos(outfile=tmp, set_append=False)
        make_G0(outfile=tmp)
    else:
        make_G0(outfile=tmp)
    make_B0(outfile=tmp)
    outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-08_gaincal.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_K0(outfile=tmp)
     else:
         make_K0(outfile=tmp, set_append=False)

     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-08_applycal.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_K0(outfile=tmp)
     else:
         make_K0(outfile=tmp, set_append=False)

     make_G1t(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-09-1_gaincal-p.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_K0(outfile=tmp)
     else:
         make_K0(outfile=tmp, set_append=False)

     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-09-2_gaincal-a.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_K0(outfile=tmp)
     else:
         make_K0(outfile=tmp, set_append=False)

     make_G1p(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-09_plotms1.dat'
     outlib = open(tmp, 'w')

#     if os.path.exists(t_antpos):
#         make_antpos(outfile=tmp, set_append=False)
#         make_G1(outfile=tmp)
#     else:
#         make_G1(outfile=tmp, set_append=False)

     #make_G0(outfile=tmp, set_append=False)
     make_G1p(outfile=tmp, set_append=False)
     make_G1a(outfile=tmp)
     make_K0(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()

mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-09_plotms2.dat'
     outlib = open(tmp, 'w')

     #if os.path.exists(t_antpos):
     #    make_antpos(outfile=tmp, set_append=False)
     #    make_G1(outfile=tmp)
     #else:
     #    make_G1(outfile=tmp, set_append=False)

#     make_G1(outfile=tmp, set_append=False)
     make_K0(outfile=tmp, set_append=False)
     make_B0(outfile=tmp)
     make_fluxscale(outfile=tmp)
     make_G1p(outfile=tmp)
     outlib.close()


mycal = 1
if(mycal in thecals):
     tmp = callibpath+'callib-11_applycal.dat'
     outlib = open(tmp, 'w')

     if os.path.exists(t_antpos):
         make_antpos(outfile=tmp, set_append=False)
         make_fluxscale(outfile=tmp)
     else:
         make_fluxscale(outfile=tmp, set_append=False)

     make_G1p(outfile=tmp)
     make_K0(outfile=tmp)
     make_B0(outfile=tmp)
     outlib.close()
