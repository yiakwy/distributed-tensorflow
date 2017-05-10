import sys
import tensorflow as tf
import ClusterSpec
import threading
try:
    import queue
except:
    import Queue as queue
import contextlib as ctx

class RuntimeErr(Exception):pass


class worker(threading.Thread):
    def __init__(self, tasks):
        threading.Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kw = self.tasks.get()
            try:
                func(*args, **kw)
            except RuntimeErr as e:
                print(e)
            finally:
                self.tasks.task_done()


class Server:
    
    def __init__(self):
        self._cluster = tf.train.ClusterSpec(ClusterSpec.clusters)
        id = next(ClusterSpec.tasks_gen)
        print("job id: %s" % id)
        self._server = tf.train.Server(self._cluster, job_name=ClusterSpec.job_name, task_index=id)

    def run(self):
        print("start server %s" % str(self._server))
        self._server.start()


class ServerPool:

    def __init__(self, max_workers=ClusterSpec.taskPoolSize):
        self.tasks = queue.Queue(max_workers)
        self.max_workers = max_workers
        # for _ in range(max_workers):
            # worker(self.tasks)
    
    def add_task(self, func, *args, **kw):
        self.tasks.put((func, args, kw))

    def wait_completion(self):
        self.tasks.join()

    def run(self):
        for _ in range(self.max_workers):
            self.add_task(Server().run)

if __name__ == "__main__":
    pool = ServerPool()
    pool.run()
    pool.wait_completion()
