import re
import random
import cPickle as pickle
from collections import defaultdict

def containsAny(string, vals):
  for x in string:
    if x in vals:
      return 1
  return 0

class MarkovGenerator(object):

  def __init__(self, order = 1):
    self.seed = None
    self.punct = ".?!"

    self.order = order # the number of words to use as the model's "key"
    self.openers = []
    self.model = defaultdict(list)


  def _clean(self, data):
    """ Cleans up the text a bit.
        Specifically, removes *()" characters
        and quotes that do not occur in the
        middle of a word.

    """
    def repl(matchobj):
      start, end = matchobj.groups()
      if start is None and end is None:
        return "'"
      elif start is not None:
        return start
      elif end is not None:
        return end
    data = re.sub("(\s|^)?'+(\s|$)?", repl, data)
    return re.sub("[*()\"]", "", data)


  def train(self, data):
    """ Train the generator with provided data.
        Can be called multiple times (with different data)

    """
    data = self._clean(data)
    """ Split the text into words, spaces, and punctuation
        Spaces show up as None in the list, so we remove them in a 
        list comprehension
    """
    words = [x for x in
              re.split("([{0}])?\s*".format(self.punct), data)
                if x is not None]

    opener = True
    for ix in xrange(0, len(words)-self.order):
      if words[ix] in self.punct:
        opener = True
        continue
      key = tuple(words[ix:ix+self.order])

      if not containsAny(key, self.punct):
        if opener:
          """ Mark the first words in a sentence as "openers" to seed the
              generator
          """
          self.openers.append(key)
          opener = False
        self.model[key].append(words[ix + self.order])

  def load_training_data(self, filename):
    """ Loads pickled training data from a file """
    with open(filename, 'r') as f:
      training_data = pickle.load(f)
      self.order, self.openers, self.model = training_data

  def save_training_data(self, filename):
    """ Saves pickled training data to a file """
    with open(filename, 'w') as f:
      pickle.dump((self.order, self.openers, self.model), f)


  def randomize_seed(self):
    """ Picks a random opener to use as the seed for the generator """
    if len(self.openers) > 0:
      self.seed = random.choice(self.openers)
    else:
      raise ValueError("No openers present, cannot seed the generator.")


  def next_word(self):
    """ Using the seed, picks a random word from possible next words """
    if (self.seed is None or
        len(self.seed) != self.order or
        self.seed not in self.model):
      self.randomize_seed()
    
    word = random.choice(self.model[self.seed])
    self.seed = tuple(self.seed[1:] + (word, ))
    return word


  def next_sentence(self, maxlen = 30):
    """ Keeps generating words until it reaches the end of a sentence
        or reaches maxlen words (prevents creating infinitely long sentences)
    
    """
    self.randomize_seed()
    words = list(self.seed)
    word = 'a'
    while len(words) <= maxlen:
      next = self.next_word()
      if next in self.punct:
        """ If punctuation, tack it onto the last word """
        words[-1] += next
        break
      words.append(next)
    return " ".join(words)



if __name__ == "__main__":
  m = MarkovGenerator(1)
  files = ["taoteching.txt"]#["montecristo.txt", "lesmis.txt", "dracula.txt", "huckfinn.txt",
          # "prideandprejudice.txt", "sherlockholmes.txt", "taleoftwocities.txt",
          # "phantom.txt", "alice.txt"]
  for filename in files:
    f = open(filename, 'r')
    data = f.read()
    print "training", filename, "..."
    m.train(data)
    f.close()
  #m.save_training_data("train.pickle")
  #m.load_training_data("train.pickle")
  print "generating output..."
  sents = []
  tot = 0
  while len(sents) < 1000:
    sent = m.next_sentence()
    if sent[-1] in m.punct:
      sents.append(sent)
      tot += len(sent.split())

  print "Average length:", 1.0 * tot / len(sents)
  
  f = open("out.txt", 'w')
  for x in xrange(5000):
    f.write(m.next_sentence())
    f.write("\n")
  f.close()

