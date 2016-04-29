# -*- coding: utf-8 -*-
"""
Created on Sat Apr 02 10:19:35 2016

@author: Sachin
"""
from sklearn import tree
def formater(f,test):
    lisy=[]
    data = []
    first_line = True
    for line in f:    
        line = line.strip().split(',')
        line = [0 if j=='' else j for j in line]
        if(test==0 and not first_line):
            lisy.append(int(line[1]))
            line = [float(line[j]) for j in range(len(line)) if j not in [0,1,4,23,25,31,32,48,53,57,67,72,75,76,80,92,108,111,113,114,126]]
        if(test==1 and not first_line):
            lisy.append(int(line[0]))
            line = [float(line[j]) for j in range(len(line)) if (j+1) not in [1,4,23,25,31,32,48,53,57,67,72,75,76,80,92,108,111,113,114,126]]
        data.append(line)
        if(first_line == True):
            first_line = False
    return data[1:],lisy
    
datap,datapy = formater(open('train.csv','r'),0)
testp,testpy = formater(open('test.csv','r'),1)
validp,validpy = datap[90000:],datapy[90000:]
datap,datapy = datap[:90000],datapy[:90000]

#depth_list = []
#def training(md):
dtree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=7)
dtree = dtree.fit(datap,datapy)
print "training accuracy: ",
print dtree.score(datap,datapy)*100
print "validation accuracy: ",
print dtree.score(validp,validpy)*100
#depth_list.append([md,train_acc,valid_acc])
    

#for i in range(5,15):
#    print "current depth: "+str(i)
#    training(i)
#print depth_list
pred_probs = []
for example in testp:
    pred_probs.append(dtree.predict_proba(example))
pred_probs = [elem[1] for elem in pred_probs]
import csv
out = [[x,y] for (x,y) in zip(testpy,pred_probs)]
out = [['ID','PredictedProb']]+out
wr=csv.writer(open('2013CS50296.csv','wb'),dialect='excel')
wr.writerows(out)