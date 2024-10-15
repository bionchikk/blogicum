from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def about(request):
    template = 'pages/about.html'
    return render(request,template)

def rules(request):
    template = 'pages/rules.html'
    return render(request,template)
