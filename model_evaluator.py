import math
from datetime import datetime
from batchify import Batchify

class ModelEvaluator:
  def __init__(self, parallelize):
    self.parallelize = parallelize

  def run(self, func, **kwargs):
    self.func = func
    self.arguments = kwargs
    self.startTime = datetime.now()
    self.batchify = Batchify(kwargs, self.parallelize.getConfig('threads'))
    self.runThreads()

  def runThreads(self):
    for arguments in self.batchify.results():
      self.parallelize.thread(self.nestedIterator, **arguments)
    self.parallelize.join()

  def nestedIterator(self, **arguments):
    iterables = filter(lambda arg: hasattr(arguments[arg], '__iter__'), arguments)
    if(len(iterables) > 0):
      iterable = iterables[0]
      for value in arguments[iterable]:
        arguments[iterable] = value
        self.nestedIterator(**arguments)
    else:
      self.parallelize.queueResult(self.func(**arguments))

  def statistics(self):
    duration = datetime.now() - self.startTime
    print "STATISTICS\n--------------------"
    print "QUEUE:"
    print "size:", self.parallelize.queue.qsize(), "items"
    print "DURATION:"
    print "us:", duration.microseconds
    print "ms:", duration.microseconds/1000
    print "s:", duration.seconds
    print "---------------------"

  def results(self, func):
    return self.parallelize.results()

