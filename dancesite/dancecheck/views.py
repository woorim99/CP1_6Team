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


    model32000 = load_model('dancecheck/model32000')
    input = './dancecheck/static/dancecheck/image/'+ image_id + '_F_00003140.jpg' 

    X_test=[]

    for test_path in tqdm([input]):
        img=tf.io.read_file(test_path)
        img=tf.image.decode_jpeg(img, channels=3)
        img=tf.image.resize(img, [180,320])
        img=img/255
        X_test.append(img)

    X_test=tf.stack(X_test, axis=0)

    pred=mode32000.predict(X_test)

    pred = pred[0]

    color = (255, 255, 255)
    red = (0 ,0 , 255)
    green = (0, 255, 0)
    blue = (255, 0, 0)
    keypoint = np.zeros((1080, 1920, 3), np.uint8)
    pose = np.zeros((1080, 1920, 3), np.uint8)

    for j in range(0,len(pred),2):
        cv2.line(keypoint, (int(pred[j]*5.4), int(pred[j+1]*5.4)), (int(pred[j]*5.4), int(pred[j+1]*5.4)), color, 10)
        cv2.line(pose, (int(pred[j]*5.4), int(pred[j+1]*5.4)), (int(pred[j]*5.4), int(pred[j+1]*5.4)), color, 30)
    #코부터 엉덩이 R
    cv2.line(pose, (int(pred[48]*5.4), int(pred[49]*5.4)), (int(pred[26]*5.4), int(pred[27]*5.4)), red, 10)
    cv2.line(pose, (int(pred[26]*5.4), int(pred[27]*5.4)), (int(pred[24]*5.4), int(pred[25]*5.4)), red, 10)
    cv2.line(pose, (int(pred[24]*5.4), int(pred[25]*5.4)), (int(pred[22]*5.4), int(pred[23]*5.4)), red, 10)
    cv2.line(pose, (int(pred[22]*5.4), int(pred[23]*5.4)), (int(pred[0]*5.4), int(pred[1]*5.4)), red, 10)
    #오른 어깨부터 오른손 G
    cv2.line(pose, (int(pred[38]*5.4), int(pred[39]*5.4)), (int(pred[40]*5.4), int(pred[41]*5.4)), green, 10)
    cv2.line(pose, (int(pred[40]*5.4), int(pred[41]*5.4)), (int(pred[42]*5.4), int(pred[43]*5.4)), green, 10)
    cv2.line(pose, (int(pred[42]*5.4), int(pred[43]*5.4)), (int(pred[44]*5.4), int(pred[45]*5.4)), green, 10)
    cv2.line(pose, (int(pred[42]*5.4), int(pred[43]*5.4)), (int(pred[46]*5.4), int(pred[47]*5.4)), green, 10)
    #왼 어깨부터 왼손 G
    cv2.line(pose, (int(pred[28]*5.4), int(pred[29]*5.4)), (int(pred[30]*5.4), int(pred[31]*5.4)), green, 10)
    cv2.line(pose, (int(pred[30]*5.4), int(pred[31]*5.4)), (int(pred[32]*5.4), int(pred[33]*5.4)), green, 10)
    cv2.line(pose, (int(pred[32]*5.4), int(pred[33]*5.4)), (int(pred[34]*5.4), int(pred[35]*5.4)), green, 10)
    cv2.line(pose, (int(pred[32]*5.4), int(pred[33]*5.4)), (int(pred[36]*5.4), int(pred[37]*5.4)), green, 10)
    #오른쪽 엉덩이 부터 오른 발목 B
    cv2.line(pose, (int(pred[12]*5.4), int(pred[13]*5.4)), (int(pred[14]*5.4), int(pred[15]*5.4)), blue, 10)
    cv2.line(pose, (int(pred[14]*5.4), int(pred[15]*5.4)), (int(pred[16]*5.4), int(pred[17]*5.4)), blue, 10)
    #왼쪽 엉덩이 부터 왼쪽 발목 B
    cv2.line(pose, (int(pred[2]*5.4), int(pred[3]*5.4)), (int(pred[4]*5.4), int(pred[5]*5.4)), blue, 10)
    cv2.line(pose, (int(pred[4]*5.4), int(pred[5]*5.4)), (int(pred[6]*5.4), int(pred[7]*5.4)), blue, 10)

    background = Image.open(input)
    foreground1 = Image.fromarray(keypoint).convert("1")

    (img_h, img_w) = foreground1.size

    resize_back1 =  background.resize((img_h, img_w))

    resize_back1.paste(foreground1, (0, 0), foreground1)
    resize_back1.save('./dancecheck/static/dancecheck/keypoint/' + image_id + '_keypoint.jpg')

    foreground2 = Image.fromarray(pose).convert("RGBA")

    (img_h, img_w) = foreground2.size

    resize_back2 =  background.resize((img_h, img_w))

    resize_back2.paste(foreground2, (0, 0), foreground2)

    resize_back2.save('./dancecheck/static/dancecheck/pose/' + image_id + '_pose.jpg')

    return render(request, 'dancecheck/display.html', {'image_id': image_id})
