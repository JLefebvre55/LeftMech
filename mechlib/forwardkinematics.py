import numpy as np

def getSingleTransform(theta, alpha, r, d):
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    cosalpha = np.cos(alpha)
    sinalpha = np.sin(alpha)
    new = np.array([
        [costheta, -sintheta*cosalpha, sintheta*sinalpha, r*costheta],
        [sintheta, costheta*cosalpha, -costheta*sinalpha, r*sintheta],
        [0., sinalpha, cosalpha, d],
        [0., 0., 0., 1.]
    ])
    return new

def getNetTransform(params):
    transform = np.identity(4)
    for (theta, alpha, r, d) in params:
        new = getSingleTransform(theta, alpha, r, d)
        transform = np.dot(transform, new)
    return transform

def getAllTransforms(params):
    transform = np.identity(4)
    transforms = [transform]
    for (theta, alpha, r, d) in params:
        new = getSingleTransform(theta, alpha, r, d)
        transform = np.dot(transform, new)
        transforms.append(transform)
    return transforms