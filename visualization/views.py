# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
from django.conf  import settings
import pandas as pd

# Create your views here.
def visual(request):
    context = {
            'Title': "Step 7: Cluster Visualization",
            'listId':"li7"     }
    return render(request, 'clustering/stp7-clu-visualisation.html',context)


def explore(request):
    context = {
            'Title': "Step 8: Data Exploration",
            'listId':"li8"
        }
    return render(request, 'visualization/newpage.html',context)


def compare(request):
    context = {
            'Title': "Step 9: Data Labeling",
            'listId':"li9"
        }
    return render(request, 'visualization/comparison.html',context)

def labeling(request):
    
    #get parameters from request
    id1 = request.POST.get("id1")  
    id2 = request.POST.get("id2")
    label = request.POST.get("sim")
    
    print id1, id2, label
    
    if id1 <> None:
    
        df = pd.DataFrame([[id1, id2, label]],columns=['id1','id2','label'])
        
        df_label = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/outcome_labels.csv'))
        
        frame = pd.concat([df_label,df])
        
        frame.to_csv(os.path.join(settings.BASE_DIR, 'data/outcome_labels.csv'), index=False)
      
    context = {
            'Title': "Step 7: Cluster Visualization",
            'listId':"li7",
            'metric':True
        }
    return render(request, 'clustering/stp7-clu-visualisation.html',context)
