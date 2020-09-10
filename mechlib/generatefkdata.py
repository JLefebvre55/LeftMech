import tensorflow as tf
import forwardkinematics as fk
from robot import Robot
from pathlib import Path
import json
from time import time
import numpy as np

filename = "largeDataNormalized_{}.json"

def generateDataset(robot, items, split):
    assert(split <=1 and split >=0)
    print("Making {}-long FK dataset...".format(items))
    print("0.0%")
    x = []
    y = []
    lastPrint = time()
    startTime = time()
    for i in range(items): #Generates a list of angles-transform pairs (items)
        if(time() - lastPrint > 1):
            print("{:.1f}%".format(float(i)/items*100))
            lastPrint = time()
        rand = np.random.random((robot.numjoints,)) #Generates a random angle input for each joint (0-2pi)
        y.append(rand.tolist()) #Add to NN-output train pile
        #print("Angles: {}".format(y[-1]))
        temp = fk.getNetTransform(robot.getParams(rand)) #Get and pass DH-parameter Tensor matrix to FK computer
        out = temp[:-1,-1] #for now, position ONLY - for simplicity
        x.append(out.tolist())
        #print("Transform: {}".format(x[-1]))
    print("100.0% - took {:.2f}s".format(time()-startTime))
    return x, y

def makeDataset(robot, items=1000, split = .8):
    x, y = generateDataset(robot, items, split)
    fn = filename.format(robot.fileSafeName)
    datastore = {
        "angles": y,
        "transforms": x,
    }
    my_file = Path(fn)
    if my_file.is_file():
        mode = 'w'
    else:
        mode = 'x'
    with open(fn, mode) as f:
        json.dump(datastore, f)
        print("Saved to file {}".format(fn))

def getDataset(robot, split):
    print("Loading data...")
    with open(filename.format(robot.fileSafeName), 'r') as f:
        data = json.load(f)
    angles = data["angles"]
    transforms = data["transforms"]
    print("Dataset (size: {}) loaded.".format(len(angles)))
    i = int(split*len(angles))
    xtrain = tf.convert_to_tensor(transforms[:i])
    ytrain = tf.convert_to_tensor(angles[:i])
    xtest = tf.convert_to_tensor(transforms[i:])
    ytest = tf.convert_to_tensor(angles[i:])
    return xtrain, ytrain, xtest, ytest

if __name__ == "__main__":
    makeDataset(Robot("Mech"), 1000)