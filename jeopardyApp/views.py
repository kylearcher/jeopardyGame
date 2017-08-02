# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

#load other python file
from main_jeopardy import *
#

def index(request):

    game_dict = start_game_data_re(1)

    test_info = game_dict
    context = {'test_info': test_info}
    return render(request, 'jeopardyApp/index.html', context)

def double(request):
    game_dict = start_game_data_re(2)

    test_info = game_dict
    context = {'test_info': test_info}
    return render(request, 'jeopardyApp/indexdj.html', context)

def final(request):
    game_dict = start_game_data_re(3)

    test_info = game_dict
    context = {'test_info': test_info}
    return render(request, 'jeopardyApp/indexf.html', context)
