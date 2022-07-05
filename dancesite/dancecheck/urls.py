from django.urls import path

from . import views

urlpatterns = [
    # ex: /dancecheck/
    path('', views.index, name='index'),
    # ex: /dancecheck/members/
    path('members/', views.members, name='members'),
    # ex: /dancecheck/033_D00_001/
    path('<image_id>/', views.display, name='display'),
]