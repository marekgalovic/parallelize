from threading import Thread
import Queue

class Parallelize:
  def __init__(self, threads=1):
    self.config = {'threads': int(threads)}
    self.queue = Queue.Queue()
    self.threads = []

  def getConfig(self, parameter):
    return self.config[parameter]

  def run(self, func, **kwargs):
    kwargs['queue'] = self.queue
    print kwargs
    for thread_index in range(self.config['threads']):
      self.thread(func, **kwargs)

  def thread(self, func, **kwargs):
    thread = Thread(target=func, kwargs=kwargs)
    thread.start()
    self.threads.append(thread)

  def queueResult(self, result):
    self.queue.put(result)
    self.queue.task_done()

  def join(self):
    self.queue.join()
    for thread in self.threads:
      thread.join()

  def results(self):
    while not self.queue.empty():
      yield self.queue.get()
