"""
  This program determines the similarity between pairs in a list of documents.
  The similarity is calculated by counting the number of words shared
  between the two documents and dividing it by the length of the shortest
  document.
  
"""


import re
import string

results = 5

def clean(data):
  data = data.lower()
  data = data.translate(None, string.punctuation)
  data = re.sub("(\s)\s+", r"\1", data)
  return data


files = [ "alice.txt", "montecristo.txt", "lesmis.txt",
          "dracula.txt", "huckfinn.txt", "sherlockholmes.txt",
          "taleoftwocities.txt", "phantom.txt",
          "ladysusan.txt", "prideandprejudice.txt", "senseandsensibility.txt",
          "persuasion.txt"]

# Read data from files, clean it, and reduce to a set of unique words
filedata = {}
for filename in files:
  f = open(filename, 'r')
  data = f.read()
  f.close()
  data = clean(data)
  filedata[filename] = set(re.split("\s+", data))


# Take the Cartesian Product of the filenames with themselves
# Insert the intersection of filename pairs into "out"
out = {}
for x in files:
  for y in files:
    if x != y and (y, x) not in out:
      out[(x, y)] = filedata[x].intersection(filedata[y])


# Calculate the number of similar words for a pair as well as each
# pair's similarity (determined by number of similar words divided
# by the length of the shortest book)
similar = []
for keys in out:
  minlength = min(len(filedata[keys[0]]), len(filedata[keys[1]]))
  num_similar_words = len(out[keys])
  similarity = 1.0 * num_similar_words / minlength
  similar.append([keys, num_similar_words, similarity])


print "Sorted by percent similarity (to the shortest text):"
for entry in sorted(similar, key=lambda x: -1 * x[2])[:results]:
  print ("{0} and {1} have {2} words in common and are {3:.2%} "
         "similar.".format(entry[0][0], entry[0][1], entry[1], entry[2]))

print
print "Sorted by words in common:"
for entry in sorted(similar, key=lambda x: -1 * x[1])[:results]:
  print ("{0} and {1} have {2} words in common and are {3:.2%} "
         "similar.".format(entry[0][0], entry[0][1], entry[1], entry[2]))
