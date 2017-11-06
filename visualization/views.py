# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
from django.conf  import settings

# Create your views here.
def visual(request):
    context = {
            'Title': "Step 7: Cluster Visualization",
            'listId':"li7",
            'vData':os.path.join(settings.BASE_DIR, 'data/outcome_visual.csv')
        }
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
