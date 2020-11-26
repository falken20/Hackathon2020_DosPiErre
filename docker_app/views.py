from django.shortcuts import render
import folium
from folium.plugins import HeatMap

# Create your views here.

import os
import logging
from django.shortcuts import render, redirect
from django.utils.timezone import now

from .models import UserItem, CompanyItem, PromotionItem, RetoItem, QuestionItem, AnswerItem, TopicItem

PATH_MAP = './templates/docker_app/'


def default_view(request):
    queryset = TopicItem.objects.all().order_by('-date')
    template_name = 'docker_app/default.html'

    return render(request, template_name, {'topics': queryset})


def users_view(request):
    queryset = UserItem.objects.all()
    template_name = 'docker_app/users.html'

    return render(request, template_name, {'users': queryset})


def ranking_view(request):
    queryset = UserItem.objects.all().order_by('-points')
    template_name = 'docker_app/ranking.html'

    return render(request, template_name, {'ranking': queryset})


def ofertas_view(request):
    queryset = PromotionItem.objects.all()
    template_name = 'docker_app/ofertas.html'

    return render(request, template_name, {'ofertas': queryset})


def reto_view(request, id_reto='R001'):
    queryset = RetoItem.objects.filter(id_reto=id_reto)
    queryset_questions = queryset[0].questions.all()
    filter = []
    for row in queryset_questions:
        filter.append(row.id_question)
    print(filter)
    queryset_answer = AnswerItem.objects.filter(question__in=filter)

    template_name = 'docker_app/reto.html'

    return render(request, template_name, {'reto': queryset, 'questions': queryset_questions,
                                           'answers': queryset_answer})


def generate_map(queryset):
    try:
        print(f'Creando mapa para coordenadas')
        location_ini = [queryset[0].company.latitude, queryset[0].company.longitude]
        heat_map = folium.Map(location=location_ini,
                              zoom_start='17')

        # HeatMap(location, radius=16).add_to(heat_map)
        for row in queryset:
            print([row.company.latitude, row.company.longitude])
            html_card = f'<div class="card" style="width: 18rem;">' \
                        f'<img src="{row.company.logo_url}" class="card-img-top" ' \
                        f'style="max-height:100px; width: auto;>' \
                        f'<div class="card-body">' \
                        f'<h5 class="card-title">{row.company}</h5>' \
                        f'<p class="card-text">{row.desc_promotion}</p>' \
                        f'<a href="/reto/{row.reto.id_reto}" class="btn btn-primary">Acepta el reto!!</a>' \
                        f' </div>' \
                        f'</div>'
            folium.Marker([row.company.latitude, row.company.longitude],
                          popup=html_card,
                          tooltip='Click me').add_to(heat_map)

    except Exception as err:
        logging.error(f'\nLine: {err.__traceback__.tb_lineno} \n'
                      f'File: {err.__traceback__.tb_frame.f_code.co_filename} \n'
                      f'Type Error: {type(err).__name__} \n'
                      f'Arguments:\n {err.args}')
    
    return heat_map


def mapa_view(request):
    queryset = PromotionItem.objects.all()

    heat_map = generate_map(queryset)

    template_name = 'docker_app/mapa.html'

    return render(request, template_name, {'users': queryset, 'map': heat_map._repr_html_()})


def result_view(request):
    template_name = 'docker_app/result.html'

    return render(request, template_name)


def deeplinking_view(request, user='Richi'):
    template_name = 'docker_app/result.html'

    return redirect(default_view)