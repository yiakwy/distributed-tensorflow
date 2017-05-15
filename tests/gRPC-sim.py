import tensorflow as tf
import sys

host = sys.argv[1]
port = sys.argv[2]

print("op")
op = tf.constant("Hello, distributed Tensorflow!")
with tf.Session("grpc://{host}:{port}".format(host=host, port=port), config=tf.ConfigProto(log_device_placement=True)) as sess:
    print("visiting <%s>" % "grpc://{host}:{port}".format(host=host, port=port))
    print(sess.run(op))

