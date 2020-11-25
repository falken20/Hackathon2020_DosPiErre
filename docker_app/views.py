from django.shortcuts import render

# Create your views here.

import os
import logging
from django.shortcuts import render
from django.utils.timezone import now

from .models import UserItem, CompanyItem, PromotionItem, RetoItem, QuestionItem, AnswerItem


def default_view(request):

    template_name = 'docker_app/default.html'

    return render(request, template_name)


def users_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/users.html'

    return render(request, template_name, {'users': queryset})


def ranking_view(request):

    queryset = UserItem.objects.all().order_by('-points')
    template_name = 'docker_app/ranking.html'

    return render(request, template_name, {'ranking': queryset})


def mapa_view(request):

    queryset = UserItem.objects.all()
    template_name = 'docker_app/mapa.html'

    return render(request, template_name, {'users': queryset})


def ofertas_view(request):

    queryset = PromotionItem.objects.all()
    template_name = 'docker_app/ofertas.html'

    return render(request, template_name, {'ofertas': queryset})


def reto_view(request, id_reto='R001'):

    queryset = RetoItem.objects.filter(id_reto=id_reto)
    # q2 = QuestionItem.objects.filter(id_reto=id_reto)
    for row in queryset:
        print(row.questions)
    template_name = 'docker_app/reto.html'

    return render(request, template_name, {'reto': queryset})

