import tensorflow as tf
import ClusterSpec
try:
    import queue
except:
    import Queue as queue
import threading

def get_ip():
    # setup
    it = iter(ClusterSpec.clusters["docker-local"])

    while True:
        try:
            yield next(it)
        except StopIteration:
            it = iter(ClusterSpec.clusters["docker-local"])

ips = get_ip()

def test_grpc(index):
    print("op")
    op = tf.constant("Hello, distributed Tensorflow! I am Node %s" % index)
    # init = tf.global_variable_initializer()
    print("ip")
    ip = next(ips)
    print("task {} visiting grpc//{ip}".format(index, ip=ip))
    with tf.Session("grpc://{ip}".format(ip=ip), config=tf.ConfigProto(log_device_placement=True)) as sess:
        # ret = sess.run(init)
        print(sess.run(op))

class worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print("waiting ...")
            func, args, kw = self.tasks.get(True, 0.05)
            try:
                print("processing ... taks")
                func(*args, **kw)
                print("done")
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class ServerPool:

    def __init__(self, max_workers=ClusterSpec.taskPoolSize):
        self.tasks = queue.Queue(max_workers)
        self.max_workers = max_workers
        for _ in range(max_workers):
            worker(self.tasks)

    def add_task(self, func, *args, **kw):
        print("add a task")
        # print("add taks: {}, {}, {}".format(str(func), str(args), str(kw))
        self.tasks.put((func, args, kw))

    def wait_completion(self):
        self.tasks.join()

    def run(self):
        for _ in range(self.max_workers):
            self.add_task(Server().run)

if __name__ == "__main__":
    visitors = 20
    pool = ServerPool()
    print("executing jobs...")
    for i in range(visitors):
        print("job %s" % i)
        pool.add_task(test_grpc, i)

    # pool.wait_completion()
