
import nltk
import io
import pickle
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[:3]': word[:3],
        #'word[-3:]': word[-3:],
        'word[-3:]': word[-3:],
        #'word[-2:]': word[-2:],
        #'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        #'word.isdigit()': word.isdigit(),
        #'postag': postag,
        #'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word[:3]': word1[:3],
            '-1:word[-3:]': word1[-3:],
            #'-1:word.isupper()': word1.isupper(),
            #'-1:postag': postag1,
            #'-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word[:3]': word1[:3],
            '+1:word[-3:]': word1[-3:],
            #'+1:word.isupper()': word1.isupper(),
            #'+1:postag': postag1,
            #'+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]



class Classifier(object):

    def __init__(self, path):
        self.crf = self._load(path)
        self.featured_text = None
        self.text = None
        self.labels = None
        
    def _load(self, path):
        with io.open(path, 'rb') as handle:
             return pickle.load(handle)
            
    def _prepare_test(self, string):
        
        sents=nltk.sent_tokenize(string)
        l=[]
        self.text=[]
        for i in sents:
            tokens = nltk.tokenize.word_tokenize(i)
            self.text.append(tokens)
            l2 = []
            for j in tokens:
                l2.append([j,'',''])
            l.append(l2)
        
       
        self.featured_text = [sent2features(s) for s in l]

    def _predict(self):
        if self.featured_text is not None:
            
            self.labels = self.crf.predict(self.featured_text)
            #return self.crf.predict(self.featured_text)
            
        else:
            return

    def gui_repr(self, string):

        self._prepare_test(string)
        self._predict()
        if self.labels is not None:
            rep = []
            for i in xrange(len(self.text)):
                for j in xrange(len(self.text[i])):
                    rep.append([self.text[i][j],self.labels[i][j]])
            #print rep
            return rep
            


