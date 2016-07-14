class Batchify:
  def __init__(self, items, max_batches_count):
    self.items = items
    self.max_batches_count = max_batches_count

  def results(self):
    parallelize_on = self.parallelizeOn()
    for index in self.getBatchIndexes(parallelize_on):
      items = self.items.copy()
      items[parallelize_on['key']] = parallelize_on['items'][index['from']:index['to']]
      yield items

  def parallelizeOn(self):
    key = max(self.items, key=lambda arg: len(self.items[arg]))
    return {
      'key': key,
      'items': self.items[key],
      'length': len(self.items[key])
    }

  def getBatchesCount(self, parallelize_on):
    if parallelize_on['length'] > self.max_batches_count:
      return self.max_batches_count

    return parallelize_on['length']

  def getBatchIndexes(self, parallelize_on):
    batches_count = self.getBatchesCount(parallelize_on)
    min_size = parallelize_on['length']/batches_count
    remainder = parallelize_on['length']%batches_count
    for batch_index in range(batches_count):
      offset = 0 if batch_index<(remainder) else remainder
      size = min_size+(1 if batch_index<(remainder) else 0)
      yield {'from': ((batch_index*size)+offset), 'to': ((batch_index*size)+size+offset)}