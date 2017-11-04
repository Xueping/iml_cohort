# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
from django.shortcuts import render
# Create your views here.
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
import csv
import json

from django.conf  import settings
import os
'''
These are the param users need to choose
    :param al_selection: 
al_selection is to input a number between 0-3, where each number represents a clustering algorithm
0: KMeans
1: MiniBatchKMeans
2: Birch
3: AgglomerativeClustering
    :param num_clustering: 
num_clustering is a param for the number of classes for a clustering
    :param num_pca: 
num_pca is a param for the number of classes for a pca. the default is 2
'''

al_selection = 3
num_clustering = 4
num_pca = 2

def select_algorithm(selection,num_clus ,X):
    if selection == 0:
        print "using kmeans"
        return KMeans(n_clusters=num_clus).fit_predict(X)
    if selection == 1:
        print "using minibatch"
        return MiniBatchKMeans(n_clusters=num_clus).fit_predict(X)
    if selection == 2:
        print "using birch"
        return Birch(n_clusters=num_clus).fit_predict(X)
    if selection == 3:
        print "using agglo"
        return AgglomerativeClustering(n_clusters=num_clus).fit_predict(X)
    else:
        print "please input a number: 0/1/2/3"
        
def clusteringMethod(request):
    """
    Features representation of original, topics, and auto encoder features
    :param request: request from the form in feature_representation/features.html
    :return: render the representation of features in feature_representation/results.html
    """
    if request.method == 'POST':
        num_topics = int(request.POST.get("num_topics", ""))  # get the number of topics
        num_dim = int(request.POST.get("num_dim", ""))  # get the dimension of encoded features
        clusteringAndPCA()
        # context is a dict of html code, containing three types of features representation
        
        return render(request,'clustering/results.html')
    else:
        return render(request, 'clustering/features.html')

# do clustering algorithm
def clusteringAndPCA():
    X = []
    with codecs.open(os.path.join(settings.BASE_DIR, 'data/demo_test_data.csv'), 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(','))
        for line in spamreader:
            X.append([float(ele) for ele in line][:])
        # do clustering
        X = np.array(X,dtype='float32')
        y_pred = select_algorithm(al_selection,num_clustering,X)
    
    #export csv file for the clustering result
    with codecs.open(os.path.join(settings.BASE_DIR, 'data/demo_test_data.csv'), 'r', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(','))
        with codecs.open(os.path.join(settings.BASE_DIR, 'data/test_data.csv'), 'w', encoding='utf-8') as csvoutputfile:
            index = 0
            for line in spamreader:
                writer = csv.writer(csvoutputfile)
                writer.writerow(line + [y_pred[index]])
                index +=1
    
    
    # export json file and transform num_classes to 2 dim by pca
    pca = PCA(n_components=num_pca)
    pca.fit(X)
    X_trans = pca.transform(X)
    
    
    num_attr = len(X[0])
    dict_out = {}
    list_tmp = []
    for sample_num in range(len(X)):
        dict_in = {}
        for attr_num in range(num_pca+num_attr):
    
            if attr_num < num_pca:
                dict_in[str(attr_num)] = str(X_trans[sample_num][attr_num])
            else:
                dict_in[str(attr_num)] = str(X[sample_num][attr_num-num_attr])
        dict_in['label'] = str(y_pred[sample_num])
        list_tmp.append(dict_in)
    
    dict_out['nodes'] = list_tmp
    
    # create a json file for all the original attr and PCA attr
    with open(os.path.join(settings.BASE_DIR, 'data/clustering_pca.json'),'w') as output:
        #a = np.asarray(dict_out).tolist()
        json.dump(dict_out,output)


'''
The format of the dictionary is in the form: {key: value}, the meaning of the key and the corresponding value is as follows:

0:pca attr1
1:pca attr2
3:original attrX 
... (until the last original feature)
label:label value

Here is an example of the relationship:
1: demo_test_data.csv (original feature file):
[[ 1.  2.  3.]
 [ 2.  3.  4.]
 [ 3.  4.  6.]
 [ 4.  5.  1.]]

2: PCA attributes:
[[-0.66509402  2.07548809]
 [-0.79295802  0.34816322]
 [-1.77771211 -1.89466071]
 [ 3.23576403 -0.52899051]]

Output clustering_pca.json:
{
"nodes": 
[{"label": "3", "1": "2.07549", "0": "-0.665094", "3": "1.0", "2": "3.0", "4": "2.0"}, 
{"label": "1", "1": "0.348163", "0": "-0.792958", "3": "2.0", "2": "4.0", "4": "3.0"}, 
{"label": "2", "1": "-1.89466", "0": "-1.77771", "3": "3.0", "2": "6.0", "4": "4.0"}, 
{"label": "0", "1": "-0.528991", "0": "3.23576", "3": "4.0", "2": "1.0", "4": "5.0"}]
}55
'''
# create a json file for all the original attr and PCA attr
# with open(os.path.join(settings.BASE_DIR, 'data/clustering_pca.json'),'w') as output:
#     #a = np.asarray(dict_out).tolist()
#     json.dump(dict_out,output)
