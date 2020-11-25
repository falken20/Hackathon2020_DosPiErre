from django.shortcuts import render

# Create your views here.

import os
import logging
from django.shortcuts import render
from django.utils.timezone import now

from .models import UserItem, CompanyItem


def default_view(request):

    template_name = 'docker_app/default.html'

    return render(request, template_name)


def users_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/users.html'

    return render(request, template_name, {'users': queryset})


def ranking_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/ranking.html'

    return render(request, template_name, {'users': queryset})

def mapa_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/mapa.html'

    return render(request, template_name, {'users': queryset})

def ofertas_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/ofertas.html'

    return render(request, template_name, {'users': queryset})