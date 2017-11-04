#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms

class UploadFileForm(forms.Form):
    original = forms.NumberInput()
    topic = forms.NumberInput()
    encoder = forms.NumberInput()
