from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from binance import Client
from binance.enums import *
from django.template.defaulttags import register
import random

api_key = 'up3qm7ypmC4pQ4fIOt9fukffxv6gCvzMTbtvrfDeCaSQ9nPE0FuHXlz3ORRdBVCM'
api_secret = 'OFrd6x7hBSAxxIP0liVDpfv6v0OBbCKtoaRTWqn8Te3y7gjv7s7Rz8RZVYT9B5A5'

class Home_page(TemplateView):
    template_name = "landing.html"

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]

def Api(request):
    client = Client(api_key, api_secret)
    orders = client.get_all_tickers() 
    s = list(map(lambda x : x['symbol'], orders))
    p = list(map(lambda x : x['price'], orders))
    random.shuffle(s)
    random.shuffle(p)
    context = {
        "symbols": s,
        "prices": p,
    }
    return render(request, "api.html", context)