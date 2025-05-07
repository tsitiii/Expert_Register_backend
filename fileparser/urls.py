from django.urls import path
from . import views

urlpatterns = [
    path('cv/', views.home, name="home_page"),
    path('upload_resume/', views.upload_resume, name="upload_resume"),
    path('person/', views.index),
    path('add/', views.add_person),
    path('show/', views.get_all_person)
]