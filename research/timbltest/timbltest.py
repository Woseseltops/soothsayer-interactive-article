from timbl import TimblClassifier

classifier = TimblClassifier('test','-a 0 -k 1')

classifier.append( ('dit','is','een'), 'idee')
classifier.append( ('dat','was','geen'), 'doen')

classifier.train()

r = classifier.classify(('dit','was','geen'))
print(r)