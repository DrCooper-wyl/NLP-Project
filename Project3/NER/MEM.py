#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# --------------------------------------------------
# Description:
# --------------------------------------------------
# Author: Konfido <konfido.du@outlook.com>
# Created Date : April 4th 2020, 17:45:05
# Last Modified: April 4th 2020, 17:45:05
# --------------------------------------------------
from threading import Thread

import nltk
from nltk.corpus import names
from nltk.classify.maxent import MaxentClassifier
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score,
                             recall_score)
import os
from tqdm import tqdm
import pickle
class FeaturesThread(Thread):
    def __init__(self,data,labels,memm):
        super(FeaturesThread,self).__init__()
        self.data=data
        self.res=[]
        self.labels=labels
        self.memm=memm
    def get_data(self):
        return self.data
    def run(self) -> None:
        for i in tqdm(range(len(self.data))):
            self.res.append(self.memm.features(self.data, self.labels[i], i))

class MEMM():
    def __init__(self):
        self.train_path = "../data/train"
        self.dev_path = "../data/dev"
        self.beta = 0
        self.max_iter = 0
        self.classifier = None
        self.name_lsit=names.words('male.txt')+names.words('female.txt')

    def features(self, words, previous_label, position):
        """
        Note: The previous label of current word is the only visible label.

        :param words: a list of the words in the entire corpus
        :param previous_label: the label for position-1 (or O if it's the start
                of a new sentence)
        :param position: the word you are adding features for
        """

        features = {}
        """ Baseline Features """
        current_word = words[position]
        features['has_(%s)' % current_word] = 1
        features['prev_label'] = 0 if previous_label=='O' else 1
        if current_word[0].isupper():
            features['Titlecase'] = 1

        #===== TODO: Add your features here =======#

        features['is_all_letters']=current_word.isalpha()
        features['previous_.'] = words[position-1]=='.' or position==0
        try:
            if words[position-1].isalpha():
                features['previous_tag']=nltk.pos_tag([words[position-1]])[0][1]
            features['previous'] = words[position - 1]
            features['p_name'] = words[position - 1] in self.name_lsit
        except Exception:
            pass
        try:
            if words[position+1].isalpha():
                features['next_tag']=nltk.pos_tag([words[position+1]])[0][1]
            features['next'] = words[position + 1]
            features['n_name'] = words[position + 1] in self.name_lsit
        except Exception:
            pass
        if current_word.isalpha():
            features['tag']=nltk.pos_tag([current_word])[0][1]
            features['name'] = current_word in self.name_lsit
        try:
            if words[position-2].isalpha():
                features['previous_2_tag']=nltk.pos_tag([words[position-2]])[0][1]
            features['previous_2'] = words[position - 2]
            features['p_2_name'] = words[position - 2] in self.name_lsit
        except Exception:
            pass
        try:
            if words[position+2].isalpha():
                features['next_2_tag']=nltk.pos_tag([words[position+2]])[0][1]
            features['next_2'] = words[position + 2]
            features['n_2_name'] = words[position + 2] in self.name_lsit
        except Exception:
            pass


        #=============== TODO: Done ================#
        return features

    def load_data(self, filename):
        words = []
        labels = []
        for line in open(filename, "r", encoding="utf-8"):
            doublet = line.strip().split("\t")
            if len(doublet) < 2:     # remove emtpy lines
                continue
            words.append(doublet[0])
            labels.append(doublet[1])
        return words, labels

    def get_features(self,words,labels):
        l=len(words)
        res=[]
        threadList=[]
        n=40000
        if l%n==0:
            for i in range(l//n):
                threadList.append(FeaturesThread(words[n*i:n*(i+1)-1],labels[n*i:n*(i+1)-1],self))
        else:
            for i in range(l//n):
                threadList.append(FeaturesThread(words[n*i:n*(i+1)-1],labels[n*i:n*(i+1)-1],self))
            threadList.append(FeaturesThread(words[n * (l//n +1):], labels[n * (l//n +1):], self))
        for t in threadList:
            t.start()
        for t in threadList:
            t.join()
        for t in threadList:
            res+=t.get_data()
        return res

    def train(self):
        print('Training classifier...')
        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        features = []
        print("\tGenerate Features...")
        # features=self.get_features(words,previous_labels)
        for i in tqdm(range(len(words))):
            features.append(self.features(words, previous_labels[i], i))
        # features = [self.features(words, previous_labels[i], i)
        #             for i in range(len(words))]
        train_samples = [(f, l) for (f, l) in zip(features, labels)]
        classifier = MaxentClassifier.train(
            train_samples, max_iter=self.max_iter)
        self.classifier = classifier

    def test(self):
        print('Testing classifier...')
        words, labels = self.load_data(self.dev_path)
        previous_labels = ["O"] + labels
        features=[]
        print("\tGenerate Features...")
        # features = self.get_features(words, previous_labels)
        for i in tqdm(range(len(words))):
            features.append(self.features(words, previous_labels[i], i))
        # features = [self.features(words, previous_labels[i], i)
        #             for i in range(len(words))]
        results = [self.classifier.classify(n) for n in features]

        f_score = fbeta_score(labels, results, average='macro', beta=self.beta)
        precision = precision_score(labels, results, average='macro')
        recall = recall_score(labels, results, average='macro')
        accuracy = accuracy_score(labels, results)

        print("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))

        return True

    def show_samples(self, bound):
        """Show some sample probability distributions.
        """
        words, labels = self.load_data(self.train_path)
        previous_labels = ["O"] + labels
        features = []
        print("\tGenerate Features...")
        # features = self.get_features(words, previous_labels)
        for i in tqdm(range(len(words))):
            features.append(self.features(words, previous_labels[i], i))
        # features = [self.features(words, previous_labels[i], i)
        #             for i in range(len(words))]
        (m, n) = bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
            if label == 'PERSON':
                fmt = '  %-15s *%6.4f   %6.4f'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
            print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))

    def dump_model(self):
        with open('../model.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self):
        with open('../model.pkl', 'rb') as f:
            self.classifier = pickle.load(f)
