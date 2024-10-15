from django.contrib import admin
from django.urls import path,include

from . import views
app_name = 'pages'
urlpatterns = [
    path('about/',views.AboutPage.as_view(), name = "about"),
    path('rules/',views.RulesPage.as_view(), name = "rules"),
    
]
