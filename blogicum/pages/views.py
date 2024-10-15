from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound

from django.views.generic import TemplateView

class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'core/404.html',status=404)


def csrf_failure(request, reason = ''):
    return render(request, 'core/403csrf.html',status=403)