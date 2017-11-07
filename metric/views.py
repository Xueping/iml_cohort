# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf  import settings
from django.shortcuts import render
from metric_learn import SDML
from scipy import io
# from numpy import linalg as LA

from clustering.views import clusteringAndTSNE
import pandas as pd
import numpy as np


# Create your views here.
def update(request):
    
    df_label = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_labels.csv'))
    
    df_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv'))
    
    #remove dupicate
    rowIDLIst = pd.concat([df_label.id1,df_label.id2],axis = 0).unique().tolist()
    print rowIDLIst

    cmatrix = np.zeros([len(rowIDLIst),len(rowIDLIst)])
#     print df_label
# #     next(df_label.iterrows())
    for lbl in df_label.as_matrix():
        print lbl
        cmatrix[rowIDLIst.index(lbl[0])][rowIDLIst.index(lbl[1])] = int(lbl[2])
        cmatrix[rowIDLIst.index(lbl[1])][rowIDLIst.index(lbl[0])] = int(lbl[2])
   
    trainedData = []
    
    for rid in rowIDLIst:
        row = df_data.iloc[[rid]]
        trainedData.append(row)
        
    print trainedData.dtpye
    print cmatrix.dtpye
    
    metric = SDML().fit(trainedData, cmatrix)  
    
    newData = metric.transform(df_data) 
    
    al_selection = request.session['clustering']
    num_clustering = request.session['num_cluster'] 

    
#     print LA.cond(df_label)
#     print df_label
#     print df_label.shape
#     print LA.cond(df_data)
#     print df_data.shape
#     metric = SDML().fit(df_data, df_label)
#     .transform(df_data)
    
    clusteringAndTSNE(newData,al_selection,num_clustering)
        # context is a dict of html code, containing three types of features representation
    content = {'Title': "Step 7: Clustering Visualization",
               "listId":"li7"} 
    return render(request,'clustering/stp7-clu-visualisation.html',content)


