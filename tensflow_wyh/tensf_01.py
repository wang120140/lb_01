import tensorflow as tf
import  os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

a= tf.constant(11.0)
b = tf.constant(20.0)
c= tf.add(a,b)



with tf.compat.v1.Session() as sess:
    c_res = sess.run(c)
print(c)