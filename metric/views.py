# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf  import settings
from django.shortcuts import render
from metric_learn import SDML
from scipy import io
from numpy import linalg as LA

from clustering.views import clusteringAndPCA
import pandas as pd


# Create your views here.
def update(request):
    
    df_label = io.mmread(os.path.join(settings.BASE_DIR, 'data/outcome_labels.mtx')).todense()
    
#     print df_label.
    
    df_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/features_rep.csv')).as_matrix()
    
#     al_selection = request.session['clustering']
#     num_clustering = request.session['num_cluster'] 
    
    print LA.cond(df_label)
    print df_label
    print df_label.shape
    print LA.cond(df_data)
    print df_data.shape
    metric = SDML().fit(df_data, df_label)
#     .transform(df_data)
    
#     clusteringAndPCA(metric,al_selection,num_clustering)
        # context is a dict of html code, containing three types of features representation
    content = {'Title': "Step 7: Clustering Visualization",
               "listId":"li7"} 
    return render(request,'clustering/stp7-clu-visualisation.html',content)


