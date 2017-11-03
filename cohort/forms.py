'''
Created on 3 Nov 2017

@author: xuepeng
'''

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()