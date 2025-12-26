from django.urls import path

from . import views

urlpatterns = [
    path('about_view/', views.about_view, name="about_us"),
    path('contact/', views.contact_view, name="contact"),
]

