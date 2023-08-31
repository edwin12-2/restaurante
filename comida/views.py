from django.http import HttpResponse
from django.shortcuts import render

def index(re):
    return render(re, 'index.html')
