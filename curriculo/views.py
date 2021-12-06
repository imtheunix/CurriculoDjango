from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import User, Room, Message
from .forms import CustomUserCreationForm
from django.views import generic
from binance import Client
from binance.enums import *
from django.template.defaulttags import register
from django import template
import websocket
import json
import talib
import numpy
import random
import csv

RSI_PERIOD = 3
RSI_OVERBOUGHT = 68
RSI_OVERSOLD = 32
rsi, preco, candle, closes = [], [], [], []
cc = 'nanousdt'
i = 0
interval = '1m'
api_key = 'up3qm7ypmC4pQ4fIOt9fukffxv6gCvzMTbtvrfDeCaSQ9nPE0FuHXlz3ORRdBVCM'
api_secret = 'OFrd6x7hBSAxxIP0liVDpfv6v0OBbCKtoaRTWqn8Te3y7gjv7s7Rz8RZVYT9B5A5'
socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class Home_page(TemplateView):
    template_name = "landing.html"


def home(request):
    return render(request, 'home.html')


def Api(request):
    client = Client(api_key, api_secret)
    orders = client.get_all_tickers()
    s = list(map(lambda x: x['symbol'], orders))
    p = list(map(lambda x: x['price'], orders))
    random.shuffle(s)
    random.shuffle(p)
    context = {
        "symbols": s,
        "prices": p,
    }
    return render(request, "api.html", context)


def Robo(request):
    client = Client(api_key, api_secret)
    candles = client.get_klines(symbol='NANOUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
    c1 = candles[1]
    c2 = candles[2]
    c3 = candles[3]
    c4 = candles[4]
    c5 = candles[5]
    c6 = candles[6]
    closes = float(c1[4]), float(c2[4]), float(c3[4]), float(c4[4]), float(c5[4]), float(c6[4])
    average = Average(closes)
    media = float(average)
    np_closes = numpy.array(closes)
    rsi = talib.RSI(np_closes, RSI_PERIOD)
    last_rsi = rsi[-1]
    context = {
        "closes": closes,
        "last_rsi": last_rsi,
        "medias": media
    }
    return render(request, "robo.html", context)

def Average(lst):
        return sum(lst) / len(lst)


def room(request, room):
    if request.user.is_authenticated:
        username = request.user.username
        room = 'publico'
        if Room.objects.exists():
            room_details = Room.objects.get(name=room)
        else:
            Room.objects.create(name='publico')
        return render(request, 'room.html', {
            'username': username,
            'room': room,
            'room_details': room_details
        })
    else:
        return render(request,'registration/signup.html')

def checkview(request):
    room = request.POST['room_name']
    username = request.user.username

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']
    if message == '':
        self.add_error('message', 'Coloque algo na mensagem')
    else:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return HttpResponse('Mensagem enviada com sucesso')

def apagar(request, username):
    Message.objects.filter(user=username).delete()

    return HttpResponse('Mensagens de usuario apagadas')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})