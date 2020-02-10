import numpy as np
import tensorflow as tf

__dhparams__ = []

class DHParameters():
    def __init__(self, theta, alpha, r, d):
        global __dhparams__
        self.r, self.alpha, self.d, self.theta = r, alpha, d, theta
        __dhparams__.append(self)
        print("FK: Added frame {} to global DH params!".format(len(__dhparams__)-1))
    def getTransform(self):
        return np.reshape((
                    np.cos(self.theta), -np.sin(self.theta)*np.cos(self.alpha), np.sin(self.theta)*np.sin(self.alpha),  self.r*np.cos(self.theta),
                    np.sin(self.theta), np.cos(self.theta)*np.cos(self.alpha),  -np.cos(self.theta)*np.sin(self.alpha), self.r*np.sin(self.theta),
                    0,                  np.sin(self.alpha),                     np.cos(self.alpha),                     self.d,
                    0,                  0,                                      0,                                      1
                
                ), (4,4))

def initParams(table):
    resetDHParams()
    for row in table:
        assert(len(row) is 4)
        DHParameters(*row)

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
    print("FK: Global DH params reset!")
    