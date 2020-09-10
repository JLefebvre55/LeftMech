import tensorflow as tf
import tensorflow.keras.backend as K

zero = K.zeros((), 'float32')
one = K.ones((), 'float32')

#DONE
def getEndTransform(dhtable):
    #SPLIT
    thetas = tf.squeeze(tf.slice(dhtable, [0,0], [-1, 1]))
    alphas = tf.squeeze(tf.slice(dhtable, [0,1], [-1, 1]))
    rs = tf.squeeze(tf.slice(dhtable, [0,2], [-1, 1]))
    ds = tf.squeeze(tf.slice(dhtable, [0,3], [-1, 1]))
    
    #SETUP
    transform = tf.eye(4)
    #Precompute one and zero (duh)
    for (theta, alpha, r, d) in zip(tf.unstack(thetas), tf.unstack(alphas), tf.unstack(rs), tf.unstack(ds)):
        #Precompute sin and cos of each angle, to avoid unneccesary repetition
        costheta = K.cos(theta)
        sintheta = K.sin(theta)
        cosalpha = K.cos(alpha)
        sinalpha = K.sin(alpha)
        new = K.stack([
            K.stack([costheta, -sintheta*cosalpha, sintheta*sinalpha, r*costheta]),
            K.stack([sintheta, costheta*cosalpha, -costheta*sinalpha, r*sintheta]),
            K.stack([zero, sinalpha, cosalpha, d]),
            K.stack([zero, zero, zero, one])
        ])
        #Slap it on there
        transform = tf.tensordot(transform, new, axes=1)
    return transform