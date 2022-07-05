from django.urls import path

from . import views

urlpatterns = [
    # ex: /dancecheck/
    path('', views.index, name='index'),
    # ex: /dancecheck/members/
    path('members/', views.members, name='members'),
    # ex: /dancecheck/033_D00_001/
    path('<image_id>/', views.display, name='display'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]