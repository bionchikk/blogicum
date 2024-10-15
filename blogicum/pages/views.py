from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView

class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'
