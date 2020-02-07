import numpy as np
from matplotlib import pyplot, animation
from mpl_toolkits.mplot3d import Axes3D #Enables 3D functionality
from time import sleep
from mechlib import geometry as g

#Objects
p1=g.Vector3()
p2=g.Vector3(1,1,1)
graphables = [g.Origin(origin=p1), g.Origin(origin=p2), g.Line(p1, p2)]

#SETUP
fig = pyplot.figure(figsize=plt.figaspect(2.)) #The graphical figure
fig.suptitle('3D Lin-Alg Rotations')
ax = fig.add_subplot(2,1,1, projection='3d') #The graphing subplot

setAxesRange(ax3D, 4)

#Drawing
for o in graphables:
    o.draw(ax)

ax = fig.add_subplot(2,1,2) #The slider subplot
s = pyplot.Slider(axSlider, "Theta", 0, 360, 0) #The slider

fig.show()

#SHOW
#while True:
#    graphables[0].rotate('z', np.radians(s.val))
#    fig.canvas.draw()