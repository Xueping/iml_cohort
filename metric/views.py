# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf  import settings
from django.shortcuts import render
from metric_learn import SDML

from clustering.views import clusteringAndTSNE
import pandas as pd
import numpy as np


# Create your views here.
def update(request):
    
    df_label = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_labels.csv'))
    
    df_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv'))
    
    #get unique row ids
    rowIDLIst = pd.concat([df_label.id1,df_label.id2],axis = 0).unique().tolist()

    #connectivity graph
    cmatrix = np.zeros([len(rowIDLIst),len(rowIDLIst)])

    for lbl in df_label.as_matrix():
        cmatrix[rowIDLIst.index(lbl[0])][rowIDLIst.index(lbl[1])] = int(lbl[2])
        cmatrix[rowIDLIst.index(lbl[1])][rowIDLIst.index(lbl[0])] = int(lbl[2])
   
    trainedData = []
    
    for rid in rowIDLIst:
        row = df_data.iloc[[rid]]
        trainedData.append(row)
        
    trainedData = pd.concat(trainedData,axis = 0).as_matrix()   

    metric = SDML().fit(trainedData, cmatrix)  
    
    newData = metric.transform(df_data) 
    
    al_selection = request.session['clustering']
    num_clustering = request.session['num_cluster'] 

    
    clusteringAndTSNE(newData,al_selection,num_clustering)
        # context is a dict of html code, containing three types of features representation
    content = {'Title': "Step 7: Clustering Visualization",
               "listId":"li7"} 
    return render(request,'clustering/stp7-clu-visualisation.html',content)


