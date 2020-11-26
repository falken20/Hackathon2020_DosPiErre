import base64
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

    try:
        z_code = ''

        if request.POST:
            z_code = request.POST['zip_code']

        if z_code == '':
            queryset = UserItem.objects.all().order_by('-points')
        else:
            queryset = UserItem.objects.all().filter(zip_code=z_code).order_by('-points')

        print('ZIP CODE', z_code)
        q_zip_code = UserItem.objects.all().values('zip_code').distinct().order_by('zip_code')

        template_name = 'docker_app/ranking.html'

        return render(request, template_name, {'ranking': queryset, 'zip_codes': q_zip_code})

    except Exception as err:
        logging.error(f'\nLine: {err.__traceback__.tb_lineno} \n'
                      f'File: {err.__traceback__.tb_frame.f_code.co_filename} \n'
                      f'Type Error: {type(err).__name__} \n'
                      f'Arguments:\n {err.args}')


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
                              zoom_start='14')
        # first, force map to render as HTML, for us to dissect
        
        # HeatMap(location, radius=16).add_to(heat_map)
        for row in queryset:
            print([row.company.latitude, row.company.longitude])
            html_card = f'<div class="card">' \
                        f'<img src="{row.company.logo_url}" class="card-img-top">' \
                        f'<div class="card-body">' \
                        f'<h5 class="card-title">{row.company}</h5>' \
                        f'<p class="card-text">{row.desc_promotion}</p>' \
                        f'<a href="/reto/{row.reto.id_reto}" class="btn btn-primary">Acepta el reto!!</a>' \
                        f' </div>' \
                        f'</div>'
            folium.Marker([row.company.latitude, row.company.longitude],
                          popup=html_card,
                          tooltip='Click me').add_to(heat_map)

        _ = heat_map._repr_html_()

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

    return render(request, template_name, {'users': queryset, 'map': heat_map.get_root()})


def result_view(request):
    template_name = 'docker_app/result.html'

    return render(request, template_name)


def deeplinking_view(request, user='Richi'):
    template_name = 'docker_app/result.html'

    print(base64.b64decode(user))

    request.session['user_name'] = base64.b64decode(user).decode()

    return redirect(default_view)