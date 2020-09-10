import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D #Enables 3D functionality
from time import sleep
import itertools
from robot import Robot
import reversekinematics_ml as rk
import forwardkinematics as fk

def drawAll(ax, vectorsets):
    plt.figure(fig2.number)
    plt.cla()
    ax.set_xlim3d(-4,4)
    ax.set_ylim3d(-4,4)
    ax.set_zlim3d(-4,4)
    end = []
    for vectors in vectorsets:
        (x, y, z) = tuple(zip(*vectors))
        ax.scatter3D(x, y, z)
        ax.plot(x, y, z)
        end.append((x[-1], y[-1], z[-1]))
    ax.plot(*tuple(zip(*end)))

#-----DENAVIT-HARTENBERG NONSENSE-----#
fig1 = plt.figure() #The graphical figure
fig1.suptitle('Joint Theta Values')

#The robot in question
robot = Robot("Mech")
jointSliders = []

for i in range(0, robot.numjoints):
    print("Creating slider {}".format(i+1))
    jointSliders.append(Slider(plt.axes([0.15, 0.1+0.05*i, 0.65, 0.03]), 'Joint {}'.format(i+1), 0., 360., valinit=0, valstep=1))


#-----PRIMARY AXIS-----#
fig2 = plt.figure() #The graphical figure
fig2.suptitle('Robot Arm Reverse Kinematics Prediction')
ax = Axes3D(fig2) 

#-----RUNTIME-----#
def update(*args): #When a slider has been updated
    args = [np.radians(s.val) for s in jointSliders]
    vectors = [i[:-1,-1] for i in fk.getAllTransforms(robot.getParams(args))]
    predicted = rk.predict(vectors[-1])*2*np.pi
    predictedVectors = [i[:-1,-1] for i in fk.getAllTransforms(robot.getParams(predicted))]
    
    drawAll(ax, [vectors, predictedVectors])

for slider in jointSliders:
    slider.on_changed(update)

update()

plt.show()