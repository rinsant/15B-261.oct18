getmed  = np.median
getave  = np.average
getsum  = np.sum
getstd  = np.std
getabs  = np.abs
getarg  = np.angle
def getave2(data):
    return getsum(data)/np.float(len(data))
def getIQR(data):
    return (stats.scoreatpercentile(data,75) - stats.scoreatpercentile(data,25))
def getstd2(data):
    return IQR(data)*0.7413
