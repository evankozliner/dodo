import random
from training_set import TrainingSet
from excerpt import Excerpt

train_set = TrainingSet('tweets.txt')
excerpt = Excerpt(train_set)
for i in xrange(5):
    print " ".join(excerpt.generate(random.randint(5, 30)))
