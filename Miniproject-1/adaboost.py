from sklearn import ensemble
from sklearn import tree
import sklearn_classifier

for i in range(300, 1500, 100):
    print 'adaboost, i = ', i
    clf = ensemble.AdaBoostClassifier(n_estimators=i)
    sklearn_classifier.classify(clf, 'adaboost/adaboost-%d' % i)
    sklearn_classifier.kfold_classify(clf, 'adaboost/adaboost-%d' % i)
