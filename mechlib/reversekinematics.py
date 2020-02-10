import tensorflow as tf
import tensorflow.keras.backend as K
import keras_fk as fk
import numpy_fk as nfk
import numpy as np
from time import time

#NN REVERSE KINEMATICS
numjoints = 4
trainingEpochs = 25
trainingDataSize = 1000
zero = K.zeros([], 'float32')
one = K.ones([], 'float32')
#tf.config.experimental_run_functions_eagerly(True)
#tf.compat.v1.enable_eager_execution()

# DONE
def getParams(args):
    args = tf.unstack(args)
    return K.stack([
        K.stack([zero,      zero,         zero,     K.constant(.5, 'float32', [])]),
        K.stack([args[0],   K.constant(np.pi/2, 'float32', []),   zero,     K.constant(2., 'float32', [])]),
        K.stack([args[1],   zero,         one, zero]),
        K.stack([args[2]-K.constant(np.pi/2, 'float32', []), K.constant(-np.pi/2, 'float32', []), zero, zero]),
        K.stack([zero, zero, zero, one]),
        K.stack([args[3], zero, zero, K.constant(.5, 'float32', [])])
    ])

#Get training data - 4 JOINTS
#for now, position ONLY - for simplicity
#DONE
def getFKData(items, split=1):
    assert(split <=1 and split >=0)
    print("Making {}-long FK dataset...".format(items))
    print("0.0%")
    global numjoints
    x = []
    y = []
    lastPrint = time()
    for i in range(items): #Generates a list of angles-transform pairs (items)
        if(time() - lastPrint > 1):
            print("{:.1f}%".format(float(i)/items*100))
            lastPrint = time()
        rand = tf.random.uniform((numjoints,), 0, np.pi*2) #Generates a random angle input for each joint (0-2pi)
        y.append(rand) #Add to NN-output train pile
        temp = fk.getEndTransform(getParams(rand)) #Get and pass DH-parameter Tensor matrix to FK computer
        out = tf.squeeze(tf.slice(temp, [0,3], [3,1])) #for now, position ONLY - for simplicity
        x.append(out)
    print("100.0%")
    i = int(split*items)
    xtrain = tf.convert_to_tensor(x[:i])
    ytrain = tf.convert_to_tensor(y[:i])
    xtest = tf.convert_to_tensor(x[i:])
    ytest = tf.convert_to_tensor(y[i:])
    return xtrain, ytrain, xtest, ytest

xtrain, ytrain, xtest, ytest = getFKData(trainingDataSize)

#Custom loss function
#The square of the distance between the true point and the predicted point
#for now, position ONLY - for simplicity
#DONE ...?
#def lossFKDistance(modelInput):
    #y_true/y_pred are (None,numjoints)-shape Tensors
def lossFKDistance(y_true, y_pred):
    y_pred = tf.reshape(y_pred, (numjoints,))
    x_pred = tf.unstack(tf.slice(fk.getEndTransform(getParams(y_pred)), [0,3], [3,1]))
    #x_true = tf.unstack(tf.reshape(modelInput, (3,)), 3)
    y_true = tf.reshape(y_true, (numjoints,))
    x_true = tf.unstack(tf.slice(fk.getEndTransform(getParams(y_true)), [0,3], [3,1]))
    result = K.pow(x_true[0]-x_pred[0],2) + K.pow(x_true[1]-x_pred[1],2) + K.pow(x_true[2]-x_pred[2],2)
    return result
    #return loss

#Set up model
model = tf.keras.models.Sequential()

#for now, position ONLY - for simplicity
model.add(tf.keras.layers.Dense(20, input_shape=(3,)))
model.add(tf.keras.layers.Dense(20, activation = 'relu'))
model.add(tf.keras.layers.Dense(numjoints, activation = 'relu'))

# Compile the model
model.compile(optimizer='adam',
              loss=lossFKDistance)

#Train the model
model.fit(xtrain, 
          ytrain, 
          #steps_per_epoch = 1,
          batch_size = 1,
          epochs = trainingEpochs)  