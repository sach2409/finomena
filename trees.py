# -*- coding: utf-8 -*-
"""
Created on Sat Apr 02 10:19:35 2016

@author: Sachin
"""
import csv
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from math import log
#calculates logloss given a probability  list
def logloss(probs):
    log_loss = 0.0
    for i in range(len(probs)):
        if(probs[i][0]!=1. and probs[i][0]!=0.):
            y = probs[i][1]
            log_loss += y*log(probs[i][0]) + (1-y)*log(1-probs[i][0])
    log_loss = -log_loss/len(probs)
    return log_loss

#brings the data into shape so that trees can be fit to it 
def formater(f,test):
    lisy=[]
    data = []
    first_line = True
    for line in f:    
        line = line.strip().split(',')
        line = [0 if j=='' else j for j in line]
        if(test==0 and not first_line):
        	#fields with value as a single alphabet
            for j in [4,31,32,48,53,67,72,75,76,80,92,108,111,113]:
                line[j] = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(str(line[j]))
            lisy.append(int(line[1]))
            line = [float(line[j]) for j in range(len(line)) if j not in [0,1,23,25,57,114,126]] #disregarding the excluded fields
        if(test==1 and not first_line):
            for (j) in [4,31,32,48,53,67,72,75,76,80,92,108,111,113]:
                line[j-1] = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(str(line[j-1]))
            lisy.append(int(line[0]))
            line = [float(line[j]) for j in range(len(line)) if (j+1) not in [1,23,25,57,114,126]]
        data.append(line)
        if(first_line == True):
            first_line = False
    return data[1:],lisy

##########################################################
#breaking data into train and validation
DATA_SIZE = 90000
datap,datapy = formater(open('train.csv','r'),0)
testp,testpy = formater(open('test.csv','r'),1)
validp,validpy = datap[DATA_SIZE:],datapy[DATA_SIZE:]
datap,datapy = datap[:DATA_SIZE],datapy[:DATA_SIZE]
###########################################################
#balancing the data
zeros_data = [datap[i] for i in range(len(datap)) if datapy[i]==0 ]
ones_data = [datap[i] for i in range(30000) if datapy[i]==1]
sub_datap = zeros_data+ones_data
sub_datapy = [datapy[datap.index(item)] for item in sub_datap]
###########################################################
print "running decision trees"
#COMMENTED CODE TO FIND THE BEST DEPTH
#depth_list = []
#def training(md):
#
dtree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=7)
dtree.fit(sub_datap,sub_datapy)
print "training accuracy: ",
print dtree.score(datap,datapy)*100
print "validation accuracy: ",
print dtree.score(validp,validpy)*100
#depth_list.append([md,train_acc,valid_acc])
#for i in range(5,15):
#    print "current depth: "+str(i)
#    training(i)
#print depth_list
pred_probs = [] #final probabilities for each data point in test
for example in testp:
    pred_probs.append(dtree.predict_proba(example))
pred_probs = [list(elem[0]) for elem in pred_probs]
pred_probs = [elem[1] for elem in pred_probs]
pred_probs = [(max(min(item,1-10**(-15)),10**(-15)),y) for (item,y) in zip(pred_probs,testpy)]
print "log loss: ",logloss(pred_probs)
####################################################################
#writing to file
####################################################################
out = [[x,y] for (y,x) in pred_probs]
out = [['ID','PredictedProb']]+out
wr=csv.writer(open('dtree.csv','wb'),dialect='excel')
wr.writerows(out)
####################################################################
#FINDING THE RIGHT PARAMETERS FOR RANDOM FOREST
#PARAMS: n_estimators, max_depth
#N = [10,15,20,25,30]
#MD = [5,7,9,11,13,15]
#yields 25,15 as best
######further######
#N = [24,25,26]
#MD = [14,15,16,17]
#min_loss = 100000000
#min_atN = 0
#min_atMD = 0
#for n in N:
#    for md in MD:
#        rf = RandomForestClassifier(n_estimators=n,max_depth=md)
#        rf.fit(sub_datap,sub_datapy)
#        print "training accuracy: ",
#        print rf.score(datap,datapy)*100
#        print "validation accuracy: ",
#        print rf.score(validp,validpy)*100
#        pred_probs = []
#        for example in validp:
#            pred_probs.append(rf.predict_proba(example))
#        pred_probs = [list(elem[0]) for elem in pred_probs]
#        pred_probs = [elem[1] for elem in pred_probs]
#        pred_probs = [(max(min(item,1-10**(-15)),10**(-15)),y) for (item,y) in zip(pred_probs,validpy)]
#        log_loss = logloss(pred_probs)
#        print "log loss: ",log_loss
#        if(log_loss<min_loss):        
#            min_loss = log_loss
#            min_atN = n
#            min_atMD = md
#TURNED OUT TO BE n_estimators = 25 & max_depth = 15
rf = RandomForestClassifier(n_estimators=25,max_depth=15)
rf.fit(sub_datap,sub_datapy)
print "training accuracy: ",
print rf.score(datap,datapy)*100
print "validation accuracy: ",
print rf.score(validp,validpy)*100
pred_probs = []
for example in testp:
    pred_probs.append(rf.predict_proba(example))
pred_probs = [list(elem[0]) for elem in pred_probs]
pred_probs = [elem[1] for elem in pred_probs]
pred_probs = [(max(min(item,1-10**(-15)),10**(-15)),y) for (item,y) in zip(pred_probs,testpy)]
####################################################################
#writing to file
####################################################################
out = [[x,y] for (y,x) in pred_probs]
out = [['ID','PredictedProb']]+out
wr=csv.writer(open('rand_forest.csv','wb'),dialect='excel')
wr.writerows(out)