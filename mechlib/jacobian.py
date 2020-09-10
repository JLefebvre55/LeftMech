import numpy as np
import mechlib.forwardkinematics as fk

def getJacobianMatrix(params):
    jm = np.zeros((6, len(params)+1))
    transforms = fk.getAllTransforms(params)
    for i in range(len(transforms)):
        jm[:3,i] = np.cross(transforms[i][:2, 2], transforms[-1][:3,3]-transforms[i][:3,3])
        jm[4:,i] = transforms[i][:2, 2]
    return jm

def getVelocities(jointVelocities, params):
    return np.dot(getJacobianMatrix(params), jointVelocities)