# -*- coding: utf-8 -*-
# Create your views here.


from django.http import HttpResponse
# from django.shortcuts import render_to_response
# from django.template import RequestContext
# from django.template import loader
from django.shortcuts import render
from .forms import UploadFileForm
from sklearn.linear_model import LinearRegression

import csv
import matplotlib.pyplot as plt, mpld3


def plot(f):
    data = [[eval(k) for k in row] for row in csv.reader(f.read().splitlines())]
    x = [[row[0]] for row in data]
    y = [row[1] for row in data]

    algorithm = LinearRegression()
    algorithm.fit(x,y)


    m = algorithm.coef_
    b = algorithm.intercept_
    fig = plt.figure()
    plt.scatter(x, y)
    plt.plot([min(x)[0],max(x)[0]], [m*min(x)[0] + b, m*max(x)[0] + b])
    fig_html = mpld3.fig_to_html(fig) # When we have local mpld3 libraries we will need to tweak this
    return fig_html

def index(request):
    return HttpResponse("Hello, world. You're at the cohort index.")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.FILES['file']
            fig_html = plot(name)
            context = {
               "plot": fig_html,
               'name': name
            }
            return render(request,'cohort/success.html', context)
    else:
        form = UploadFileForm()
        
#     template = loader.get_template('cohort/upload.html')
    context = {
               'form': form,
        }
#     return HttpResponse(template.render(context, request))
    return render(request, 'cohort/upload.html', context)

