import tensorflow as tf

print("op")
op = tf.constant("Hello, distributed Tensorflow!")
with tf.Session("grpc://localhost:4000", config=tf.ConfigProto(log_device_placement=True)) as sess:
    print("visiting <%s>" % "grpc://localhost:4000")
    print(sess.run(op))


