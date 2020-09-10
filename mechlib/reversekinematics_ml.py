import tensorflow as tf
import tensorflow.keras.backend as K
import keras_fk as fk
import numpy as np
from time import time
from robot import Robot
import generatefkdata as data

#NN REVERSE KINEMATICS
trainingEpochs = 25
zero = K.zeros([], 'float32')
one = K.ones([], 'float32')
hasRun = False
robot = Robot("Mech")
model = tf.keras.models.Sequential()
#tf.config.experimental_run_functions_eagerly(True)
#tf.compat.v1.enable_eager_execution()

#Custom loss function
#The square of the distance between the true point and the predicted point
#for now, position ONLY - for simplicity
#DONE ...?
#def lossFKDistance(modelInput):
    #y_true/y_pred are (None,numjoints)-shape Tensors
def lossFKDistance(y_true, y_pred):
    
    y_pred = tf.reshape(y_pred, (robot.numjoints,))
    x_pred = tf.unstack(
        tf.slice(
            fk.getEndTransform(
                
                    robot.getKerasParams(y_pred*2*np.pi)
                    
                ), [0,3], [3,1]
            )
        )
    #x_true = tf.unstack(tf.reshape(modelInput, (3,)), 3)
    y_true = tf.reshape(y_true, (robot.numjoints,))
    x_true = tf.unstack(
        tf.slice(
            fk.getEndTransform(
                
                    robot.getKerasParams(y_true*2*np.pi)
                    
                ), [0,3], [3,1]
            )
        )
    result = K.pow(x_true[0]-x_pred[0],2) + K.pow(x_true[1]-x_pred[1],2) + K.pow(x_true[2]-x_pred[2],2)
    return result
    #return loss


def train(r = robot):
    global hasRun, robot
    robot = r
    
    #for now, position ONLY - for simplicity
    model.add(tf.keras.layers.Dense(20, input_shape=(3,)))
    #odel.add(tf.keras.layers.Dense(40, activation = 'relu'))
    #model.add(tf.keras.layers.Dense(40, activation = 'relu'))
    model.add(tf.keras.layers.Dense(20, activation = 'relu'))
    model.add(tf.keras.layers.Dense(robot.numjoints, activation = 'tanh'))

    # Compile the model
    model.compile(optimizer='adam',
                    #tf.keras.optimizers.SGD(learning_rate=1, momentum=0.1, nesterov=False),
                loss=lossFKDistance,
                metrics=["accuracy"])
    
    #Get data
    xtrain, ytrain, xtest, ytest = data.getDataset(robot, 1)

    #Train the model
    model.fit(xtrain, 
            ytrain, 
            #steps_per_epoch = 1,
            batch_size = 1,
            epochs = trainingEpochs)
    
    hasRun = True  

if __name__ == "__main__":
    train()

def predict(position, r = robot):
    global robot
    robot = r
    if not hasRun: train(robot)
    return model.predict(np.reshape(position, (1,3)),
                         batch_size = 1)[0]