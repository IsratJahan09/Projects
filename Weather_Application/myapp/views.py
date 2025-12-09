from django.shortcuts import render, HttpResponse

# Create your views here.
import requests
import datetime
def home(request):
    if 'city' in request .POST:
        city = request.POST['city']
    else:
        city = 'indore'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=4bdcb3ef3728dba9868d3994d75eff52'
    PARAMS ={
        'unites':'metric',
    }
    return render(request, 'index.html')
