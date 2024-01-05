from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime

def datetime_view(request):
    if request.method == 'GET':
        data = datetime.now()
        return HttpResponse(data)