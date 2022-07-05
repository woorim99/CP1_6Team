from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Choice
from django.template import loader
from keras.models import load_model
import tensorflow as tf
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import glob
from django.conf import settings

def index(request):
    MusicList = Choice.objects.all()
    return render(request, 'dancecheck/index.html', {'MusicList': MusicList})

def members(request):
    return render(request, 'dancecheck/members.html')

def display(request, image_id):

    # video_url = settings.MEDIA_URL+'dancecheck/video/'+image_id+'.avi'

    model2000 = load_model('dancecheck/model16000')
    input = './dancecheck/static/dancecheck/image/'+ image_id + '_F_00003140.jpg'  # image_id가 포함된 path 가져오기가 필요함 DB이용? -> 영상으로 해보자

    X_test=[]

    for test_path in tqdm([input]):
        img=tf.io.read_file(test_path)
        img=tf.image.decode_jpeg(img, channels=3)
        img=tf.image.resize(img, [180,320])
        X_test.append(img)

    X_test=tf.stack(X_test, axis=0)

    pred=model2000.predict(X_test)

    pred = pred[0]

    color = (255, 255, 255)
    keypoint = np.zeros((1080, 1920, 3), np.uint8)
    for j in range(0,len(pred),2):
        cv2.line(keypoint, (int(pred[j]*8), int(pred[j+1]*8)), (int(pred[j]*8), int(pred[j+1]*8)), color, 10)

    background = Image.open(input)
    foreground = Image.fromarray(keypoint).convert("1")

    (img_h, img_w) = foreground.size

    resize_back =  background.resize((img_h, img_w))

    resize_back.paste(foreground, (0, 0), foreground)
    resize_back.save('./dancecheck/static/dancecheck/keypoint/' + image_id + '_keypoint.jpg')
            
    return render(request, 'dancecheck/display.html', {'image_id': image_id , 'result': resize_back, 'video_url':None})


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)