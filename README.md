# Parallelize
A python library that supports executing stuff in parallel.

This library provides a set of APIs around python's native threading API. In addition, there is a support for splitting large iterative tasks into smaller batches which are then executed in parallel.

### Parallelize a function
Run `test_func` once in each of four available threads. Parameter `queue` is passed automatically by parallelize. You can specify your own named parameters when calling `run` method.
```
from parallelize import Parallelize

def test_func(queue, foo):
  queue.put(foo)
  queue.task_done()

runner = Parallelize(threads=4)
runner.run(func=test_func, foo="Bar")

print list(runner.results())
>>> ['Bar', 'Bar', 'Bar', 'Bar']
```
**Note**

Don't forget to call `queue.task_done()` after `queue.put()` otherwise you will wait forever. `results()` method is a generator, so if you want to get result as an array you need to call it inside `list()`.

### Batchify parameters
Batchify will find the longest item (based on value length) and split the dataset. This allows you to easily create batches of data that can be then processed in parallel.
```
from parallelize import Parallelize
from parallelize.batchify import Batchify

data = {
  'colors': range(100),
  'variations': ['a', 'b']
}

batchify = Batchify(data, 4)
for batch in batchify.results():
  print batch
  
>>> {'colors': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], 'variations': ['a', 'b']}
>>> {'colors': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49], 'variations': ['a', 'b']}
>>> {'colors': [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74], 'variations': ['a', 'b']}
>>> {'colors': [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], 'variations': ['a', 'b']}
```
**Note**

`results()` method is a generator, so if you want to get result as an array you need to call it inside `list()`.

### Parallelizing iterative tasks
This library is meant to ease and speed up testing of hyperparameter combinations. ModelEvaluator allows you to create big iterative task which is then splitted into smaller chunks and executed in parallel. Under the hood, iterable attributes are converted into nested loops. In this case, total number of iterations will be 6090 (2x29x105) because three iterable parameters `impurity`, `depth`, `bins` are specified.
```
from parallelize import Parallelize
from parallelize.model_evaluator import ModelEvaluator

def test_func(depth, impurity, bins, foo):
  return (depth, impurity, bins)

evaluator = ModelEvaluator(Parallelize(4))
evaluator.run(
  func = test_func,
  impurity = ['gini', 'entropy'],
  depth=range(2, 31),
  bins=range(10, 1051, 10),
  foo='bar'
  )

evaluator.statistics()
```
Output of `evaluator.statistics()`
```
STATISTICS
--------------------
QUEUE: #queue size
size: 6090 items
DURATION: #duration of the task in us, ms, s
us: 107513
ms: 107
s: 0
---------------------
```
You can also call `evaluator.results()` which will return objects stored in the queue. This method a generator as well, so you need to call it inside a `list()` if you want to get results as an array.

```
results = list(evaluator.results())
print results[903:908]

>>> [(6, 'gini', 760), (6, 'gini', 770), (6, 'gini', 780), (6, 'gini', 790), (6, 'entropy', 540)]
```

### Roadmap
- Add support for distibuted task processing.
