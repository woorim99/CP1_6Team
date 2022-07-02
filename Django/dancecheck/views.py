from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Choice
from django.template import loader
import pickle


def index(request):
    MusicList = Choice.objects.all()
    return render(request, 'dancecheck/index.html', {'MusicList': MusicList})

def display(request, image_id):
    # model = None
    # with open('model.pkl','rb') as pickle_file:
    #     model = pickle.load(pickle_file)
    # input = None
    # result = model.predict(input)
    result = None
    return render(request, 'dancecheck/display.html', {'image_id': image_id , 'result': result})

# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)