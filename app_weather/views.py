from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import weather_api


def my_view(request):
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if lat and lon:
            data = weather_api.current_weather(lat=lat, lon=lon)
        else:
            data = weather_api.current_weather(55.75, 37.61)
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def my_view_second(request):
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        if lat and lon:
            data = {'result': weather_api.api_weather(lat=lat, lon=lon)}
        else:
            data = {'result': weather_api.api_weather(54.92, 43.34)}
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})