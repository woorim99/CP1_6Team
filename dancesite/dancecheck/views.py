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
    red = (0 ,0 , 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    keypoint = np.zeros((1080, 1920, 3), np.uint8)

    for j in range(0,len(pred),2):
        cv2.line(keypoint, (int(pred[j]*8), int(pred[j+1]*8)), (int(pred[j]*8), int(pred[j+1]*8)), color, 30)
    #코부터 엉덩이 R
    cv2.line(keypoint, (int(pred[48]*8), int(pred[49]*8)), (int(pred[26]*8), int(pred[27]*8)), red, 10)
    cv2.line(keypoint, (int(pred[26]*8), int(pred[27]*8)), (int(pred[24]*8), int(pred[25]*8)), red, 10)
    cv2.line(keypoint, (int(pred[24]*8), int(pred[25]*8)), (int(pred[22]*8), int(pred[23]*8)), red, 10)
    cv2.line(keypoint, (int(pred[22]*8), int(pred[23]*8)), (int(pred[0]*8), int(pred[1]*8)), red, 10)
    #오른 어깨부터 오른손 G
    cv2.line(keypoint, (int(pred[38]*8), int(pred[39]*8)), (int(pred[40]*8), int(pred[41]*8)), green, 10)
    cv2.line(keypoint, (int(pred[40]*8), int(pred[41]*8)), (int(pred[42]*8), int(pred[43]*8)), green, 10)
    cv2.line(keypoint, (int(pred[42]*8), int(pred[43]*8)), (int(pred[44]*8), int(pred[45]*8)), green, 10)
    cv2.line(keypoint, (int(pred[42]*8), int(pred[43]*8)), (int(pred[46]*8), int(pred[47]*8)), green, 10)
    #왼 어깨부터 왼손 G
    cv2.line(keypoint, (int(pred[28]*8), int(pred[29]*8)), (int(pred[30]*8), int(pred[31]*8)), green, 10)
    cv2.line(keypoint, (int(pred[30]*8), int(pred[31]*8)), (int(pred[32]*8), int(pred[33]*8)), green, 10)
    cv2.line(keypoint, (int(pred[32]*8), int(pred[33]*8)), (int(pred[34]*8), int(pred[35]*8)), green, 10)
    cv2.line(keypoint, (int(pred[32]*8), int(pred[33]*8)), (int(pred[36]*8), int(pred[37]*8)), green, 10)
    #오른쪽 엉덩이 부터 오른 발목 B
    cv2.line(keypoint, (int(pred[12]*8), int(pred[13]*8)), (int(pred[14]*8), int(pred[15]*8)), blue, 10)
    cv2.line(keypoint, (int(pred[14]*8), int(pred[15]*8)), (int(pred[16]*8), int(pred[17]*8)), blue, 10)
    #왼쪽 엉덩이 부터 왼쪽 발목 B
    cv2.line(keypoint, (int(pred[2]*8), int(pred[3]*8)), (int(pred[4]*8), int(pred[5]*8)), blue, 10)
    cv2.line(keypoint, (int(pred[4]*8), int(pred[5]*8)), (int(pred[6]*8), int(pred[7]*8)), blue, 10)

    background = Image.open(input)
    foreground = Image.fromarray(keypoint).convert("RGBA")

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