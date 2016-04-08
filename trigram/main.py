from training_set import TrainingSet
from excerpt import Excerpt

train_set = TrainingSet('tweets.txt')
excerpt = Excerpt(train_set)
print " ".join(excerpt.generate(15))
