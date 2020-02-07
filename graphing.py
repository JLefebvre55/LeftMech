import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.mplot3d import Axes3D #Enables 3D functionality
from time import sleep
from mechlib import forwardkinematics as fk

def setAxisRange(ax, axmin, axmax):
    ax.set_xlim3d(axmin,axmax)
    ax.set_ylim3d(axmin,axmax)
    ax.set_zlim3d(axmin,axmax)

def drawAll(ax, vectors):
    plt.cla()
    setAxisRange(ax, -4, 4)
    x, y, z = [], [], []
    for o in vectors:
        x.append(o[0])
        y.append(o[1])
        z.append(o[2])
    ax.scatter3D(x, y, z)
    ax.plot(x, y, z)

#-----DENAVIT-HARTENBERG NONSENSE-----#
fig1 = plt.figure() #The graphical figure
fig1.suptitle('Joint Theta Values')

numjoints = 4
jointSliders = []

for i in range(0, numjoints):
    print("Creating slider {}".format(i+1))
    jointSliders.append(Slider(plt.axes([0.15, 0.1+0.05*i, 0.65, 0.03]), 'Joint {}'.format(i+1), 0., 360., valinit=0, valstep=1))
    
    
def updateDHParams():
    fk.resetDHParams()
    fk.DHParameters(0,                                       0,          0, .5)
    fk.DHParameters(np.radians(jointSliders[0].val),         np.pi/2,    0,  2)
    fk.DHParameters(np.radians(jointSliders[1].val),         0,          1,  0)
    fk.DHParameters(np.radians(jointSliders[2].val)-np.pi/2, -np.pi/2,    0,  0)
    fk.DHParameters(0,                                       0,          0,  1)
    fk.DHParameters(np.radians(jointSliders[3].val),         0,          0,  .5)
#initialize and add all dhparams to global list
updateDHParams()

#-----PRIMARY AXIS-----#
fig2 = plt.figure() #The graphical figure
fig2.suptitle('Robot Arm Forward Kinematics')
ax = Axes3D(fig2) 

#-----RUNTIME-----#
def update(*args): #When a slider has been updated
    plt.figure(fig2.number)
    updateDHParams()
    vectors = [[0,0,0]]
    for i in fk.getAllTransforms():
        print(i)
        vectors.append(i[:-1,-1])
    drawAll(ax, vectors)

for slider in jointSliders:
    slider.on_changed(update)

update()

plt.show()