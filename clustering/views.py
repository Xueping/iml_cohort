# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
# Create your views here.
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
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
 
    if request.method == 'POST':
        #get parameters from request
        al_selection = request.POST.get("clusteringModel")  # get the number of topics
        num_clustering = int(request.POST.get("clu_num"))  # get the dimension of encoded features
        
        #put clustering parameters to sessions
        request.session['clustering'] = al_selection
        request.session['num_cluster'] = num_clustering

        #read previous step's data
        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv'))
        
        #execute clustering and dimension reduction 
        clusteringAndTSNE(data,al_selection,num_clustering)
        
        #return results to new page
        content = {'Title': "Step 7: Clustering Visualization","listId":"li7"}
        return render(request,'clustering/stp7-clu-visualisation.html',content)
    else:
        content = {'Title': "Step 6: Cohort Model Selection",
                   "listId":"li6"} 
        return render(request, 'clustering/stp6-clu-selection.html',content)

# do clustering algorithm
def clusteringAndPCA(X, al_selection,num_clustering):
   
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
    visualData.to_csv(os.path.join(settings.BASE_DIR, 'static/data/outcome_visual.csv'), index=False) 
    
    
# do clustering algorithm
def clusteringAndTSNE(X, al_selection,num_clustering):
   
    #get Cluster ID for each record
    y_pred = select_algorithm(al_selection,num_clustering,X)
    
    #add cluster into a new column
    X['cluster'] = y_pred  
    #write to a csv file  
    X.to_csv(os.path.join(settings.BASE_DIR, 'data/clustering_results.csv'), index=False) 
  
    #PCA processing
    del X['cluster']
    # export json file and transform num_classes to 2 dim by pca
    pca = TSNE(n_components=num_pca)
    X_trans = pca.fit_transform(X)
    
    x_trans = pd.DataFrame(data=X_trans,columns=['x','y'])
    
    diag_dict = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_diags_desc.csv'))
    frames = [x_trans,  diag_dict ]  
    visualData =  pd.concat(frames, axis=1)
    visualData['cluster'] = y_pred  
    
    visualData = visualData.rename(columns = {'Unnamed: 0':'id'})    
    visualData.to_csv(os.path.join(settings.BASE_DIR, 'static/data/outcome_visual.csv'), index=False) 
    
    