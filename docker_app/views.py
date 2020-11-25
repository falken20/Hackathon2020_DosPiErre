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

    queryset = BoyItem.objects.all()
    template_name = 'docker_app/users.html'

    return render(request, template_name, {'users': queryset})