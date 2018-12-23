from django.shortcuts import render, render_to_response
from django.conf import settings

# Create your views here.

def index(request):
    str_title = 'Reactor Center'
    return render(request, 'index/index.html', locals())