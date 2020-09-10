import json
import itertools
import re
import numpy as np
import tensorflow as tf

#Generates an interactive Robot as defined in the robots.json file
class Robot():
    def __init__(self, name, file = "robots.json"):
        with open(file, 'r') as f:
            me = json.load(f)[name]
        #Get the rest of the info
        self.name = me["name"]
        #spaces to _
        #keep alphanumeric
        self.fileSafeName = "".join([c for c in self.name.replace(" ", "_") if c.isalnum() or c is "_"]).rstrip()
        self.joints = me["joints"]
        self.numjoints = len(self.joints)
        self.getParams, self.getKerasParams = Robot.parseDHFunction(me["dhparameters"])
        del(me)
    def __str__(self):
        return "Robot '{}' ({} joints)".format(self.name, self.numjoints)
    @staticmethod
    def parseDHFunction(dh):
        kpi = tf.Variable(np.pi)
        
        recompute = []
        #Simultaneous precompute
        ntable = []
        ktable = []
        for row in range(len(dh)):
            nrow = []
            krow = []
            for item in range(len(dh[row])):
                #If is args
                x = dh[row][item]
                if "args" in str(x):
                    recompute.append((row, item))
                    nrow.append(0)
                    krow.append(tf.zeros((), dtype="float32"))
                #if is number
                elif (isinstance(x, int) or isinstance(x, float)):
                    nrow.append(float(x))
                    krow.append(tf.Variable(float(x), dtype="float32"))
                #if is non-args evaluative
                else:
                    nrow.append(eval(x, None, dict({"pi" : np.pi})))
                    krow.append(tf.Variable(eval(x, None, dict({"pi" : kpi})), dtype="float32"))
            ntable.append(nrow)
            ktable.append(krow)
        def f(args): 
            #REPLACE
            for coord in recompute:
                ntable[coord[0]][coord[1]] = eval(dh[coord[0]][coord[1]], None, dict({"args" : args, "pi" : np.pi}))
            #CONVERT
            return np.array(ntable, dtype='float32')
        def g(args):
            #REPLACE
            for coord in recompute:
                ktable[coord[0]][coord[1]] = eval(dh[coord[0]][coord[1]], None, dict({"args" : args, "pi" : kpi}))
            #CONVERT
            return tf.convert_to_tensor(ktable, dtype='float32')
        return f, g
    
Robot("Mech")