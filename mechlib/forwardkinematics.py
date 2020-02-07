import numpy as np

__dhparams__ = []

class DHParameters():
    def __init__(self, theta, alpha, r, d):
        global __dhparams__
        self.r, self.alpha, self.d, self.theta = r, alpha, d, theta
        __dhparams__.append(self)
    def getTransform(self):
        return np.reshape((
                    np.cos(self.theta), -np.sin(self.theta)*np.cos(self.alpha), np.sin(self.theta)*np.sin(self.alpha),  self.r*np.cos(self.theta),
                    np.sin(self.theta), np.cos(self.theta)*np.cos(self.alpha),  -np.cos(self.theta)*np.sin(self.alpha), self.r*np.sin(self.theta),
                    0,                  np.sin(self.alpha),                     np.cos(self.alpha),                     self.d,
                    0,                  0,                                      0,                                      1
                
                ), (4,4))

def getEndTransform():
    n = np.identity(4)
    for d in getAllTransforms():
        n = np.dot(n, d)
    return n

def getAllTransforms():
    l = [__dhparams__[0].getTransform()]
    for d in __dhparams__[1:]:
        l.append(np.dot(l[-1], d.getTransform()))
    return l

def resetDHParams():
    global __dhparams__
    __dhparams__ = []