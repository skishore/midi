from __future__ import absolute_import, division, print_function

import tensorflow as tf
import numpy as np

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w):
    # NOTE: there is a baked in cost function which performs softmax and cross entropy
    return tf.matmul(X, w)

num_frequencies = 2500
num_notes = 120

X = tf.placeholder("float", [None, num_frequencies]) # create symbolic variables
Y = tf.placeholder("float", [None, num_notes])

w = init_weights([num_frequencies, num_notes])

py_x = model(X, w)

# compute mean cross entropy (softmax is applied internally)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y))
# construct optimizer
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(cost)
# at predict time, evaluate the argmax of the logistic regression
predict_op = tf.argmax(py_x, 1)

# Launch the graph in a session
with tf.Session() as sess:
    # you need to initialize all variables
    tf.initialize_all_variables().run()

    for (frequencies, answer) in something:
        # train
        sess.run(train_op, feed_dict={X: frequencies, Y: answer})

    print(i, np.mean(np.argmax(teY, axis=1) ==
                     sess.run(predict_op, feed_dict={X: teX, Y: teY})))
