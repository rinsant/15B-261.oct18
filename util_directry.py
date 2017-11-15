pipepath  = './py/'
if not os.path.exists(pipepath):
    os.makedirs(pipepath)

callibpath  = pipepath+'./callib/'
if not os.path.exists(callibpath):
    os.makedirs(callibpath)

logpath    = './log/'
if not os.path.exists(logpath):
    os.makedirs(logpath)

possmpath  = logpath+'./plotms-possm/'
if not os.path.exists(possmpath):
    os.makedirs(possmpath)

vplotpath  = logpath+'./plotms-vplot/'
if not os.path.exists(vplotpath):
    os.makedirs(vplotpath)

uvplotpath = logpath+'./plotms-uvplot/'
if not os.path.exists(uvplotpath):
    os.makedirs(uvplotpath)

snplotpath = logpath+'./plotcal-snplot/'
if not os.path.exists(snplotpath):
    os.makedirs(snplotpath)

bpplotpath = logpath+'./plotcal-bpplot/'
if not os.path.exists(bpplotpath):
    os.makedirs(bpplotpath)

delayplotpath  = logpath+'./plotcal-delayplot/'
if not os.path.exists(delayplotpath):
    os.makedirs(delayplotpath)

fitspath   = './output/fits/'
if not os.path.exists(fitspath):
    os.makedirs(fitspath)

splitpath  = './output/split/'
if not os.path.exists(splitpath):
    os.makedirs(splitpath)
