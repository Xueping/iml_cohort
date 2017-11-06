# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
import json
import pandas as pd

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

# al_selection = 3
# num_clustering = 4
num_pca = 2

def select_algorithm(selection,num_clus ,X):
    if selection == "KMeans":
        print "using kmeans"
        return KMeans(n_clusters=num_clus).fit_predict(X)
    if selection == "MiniBatchKMeans":
        print "using minibatch"
        return MiniBatchKMeans(n_clusters=num_clus).fit_predict(X)
    if selection == "Birch":
        print "using birch"
        return Birch(n_clusters=num_clus).fit_predict(X)
    if selection == "AgglomerativeClustering":
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
        al_selection = request.POST.get("clusteringModel")  # get the number of topics
        num_clustering = int(request.POST.get("clu_num"))  # get the dimension of encoded features
        print num_clustering
        clusteringAndPCA(al_selection,num_clustering)
        # context is a dict of html code, containing three types of features representation
        
        return render(request,'clustering/stp7-clu-visualisation.html')
    else:
        return render(request, 'clustering/stp6-clu-selection.html')

# do clustering algorithm
def clusteringAndPCA(al_selection,num_clustering):

    #read previous step's data
    X = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv'))
    #get Cluster ID for each record
    y_pred = select_algorithm(al_selection,num_clustering,X)
    
    #add cluster into a new column
    X['cluster'] = y_pred  
    #write to a csv file  
    X.to_csv(os.path.join(settings.BASE_DIR, 'data/clustering_results.csv'), index=False) 
  
    #PCA processing
    del X['cluster']
    # export json file and transform num_classes to 2 dim by pca
    pca = PCA(n_components=num_pca)
    pca.fit(X)
    X_trans = pca.transform(X)
    
    x_trans = pd.DataFrame(data=X_trans,columns=['x','y'])
    
    diag_dict = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_diags_desc.csv'))
    frames = [x_trans,  diag_dict ]  
    visualData =  pd.concat(frames, axis=1)
    visualData['cluster'] = y_pred  
    
    visualData = visualData.rename(columns = {'Unnamed: 0':'id'})
    
    visualData.to_csv(os.path.join(settings.BASE_DIR, 'data/outcome_visual.csv'), index=False) 
    
    
    
#     num_attr = X.shape[1]
#     
#     dict_out = {}
#     list_tmp = []
#     for sample_num in range(len(X)):
#         dict_in = {}
#         for attr_num in range(num_pca+num_attr):
#             dict_in['id'] = str(sample_num)
#             if attr_num < num_pca:
#                 dict_in['dim_'+str(attr_num+1)] = str(X_trans[sample_num][attr_num])
#             else:
#                 dict_in['feature_'+str(attr_num-num_pca+1)] = str(X.iloc[sample_num,attr_num-num_pca])
# #                 print X.iloc[sample_num,attr_num-num_pca]
#         dict_in['label'] = str(y_pred[sample_num])
#         list_tmp.append(dict_in)
#     
#     dict_out['nodes'] = list_tmp
#     
#     # create a json file for all the original attr and PCA attr
#     with open(os.path.join(settings.BASE_DIR, 'data/clustering_pca.json'),'w') as output:
#         #a = np.asarray(dict_out).tolist()
#         json.dump(dict_out,output)


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
