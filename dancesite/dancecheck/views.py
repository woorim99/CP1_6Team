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


    model2000 = load_model('dancecheck/model16000')
    input = './dancecheck/static/dancecheck/image/'+ image_id + '_F_00003140.jpg' 

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
    pose = np.zeros((1080, 1920, 3), np.uint8)

    for j in range(0,len(pred),2):
        cv2.line(keypoint, (int(pred[j]*8), int(pred[j+1]*8)), (int(pred[j]*8), int(pred[j+1]*8)), color, 10)
        cv2.line(pose, (int(pred[j]*8), int(pred[j+1]*8)), (int(pred[j]*8), int(pred[j+1]*8)), color, 30)
    #코부터 엉덩이 R
    cv2.line(pose, (int(pred[48]*8), int(pred[49]*8)), (int(pred[26]*8), int(pred[27]*8)), red, 10)
    cv2.line(pose, (int(pred[26]*8), int(pred[27]*8)), (int(pred[24]*8), int(pred[25]*8)), red, 10)
    cv2.line(pose, (int(pred[24]*8), int(pred[25]*8)), (int(pred[22]*8), int(pred[23]*8)), red, 10)
    cv2.line(pose, (int(pred[22]*8), int(pred[23]*8)), (int(pred[0]*8), int(pred[1]*8)), red, 10)
    #오른 어깨부터 오른손 G
    cv2.line(pose, (int(pred[38]*8), int(pred[39]*8)), (int(pred[40]*8), int(pred[41]*8)), green, 10)
    cv2.line(pose, (int(pred[40]*8), int(pred[41]*8)), (int(pred[42]*8), int(pred[43]*8)), green, 10)
    cv2.line(pose, (int(pred[42]*8), int(pred[43]*8)), (int(pred[44]*8), int(pred[45]*8)), green, 10)
    cv2.line(pose, (int(pred[42]*8), int(pred[43]*8)), (int(pred[46]*8), int(pred[47]*8)), green, 10)
    #왼 어깨부터 왼손 G
    cv2.line(pose, (int(pred[28]*8), int(pred[29]*8)), (int(pred[30]*8), int(pred[31]*8)), green, 10)
    cv2.line(pose, (int(pred[30]*8), int(pred[31]*8)), (int(pred[32]*8), int(pred[33]*8)), green, 10)
    cv2.line(pose, (int(pred[32]*8), int(pred[33]*8)), (int(pred[34]*8), int(pred[35]*8)), green, 10)
    cv2.line(pose, (int(pred[32]*8), int(pred[33]*8)), (int(pred[36]*8), int(pred[37]*8)), green, 10)
    #오른쪽 엉덩이 부터 오른 발목 B
    cv2.line(pose, (int(pred[12]*8), int(pred[13]*8)), (int(pred[14]*8), int(pred[15]*8)), blue, 10)
    cv2.line(pose, (int(pred[14]*8), int(pred[15]*8)), (int(pred[16]*8), int(pred[17]*8)), blue, 10)
    #왼쪽 엉덩이 부터 왼쪽 발목 B
    cv2.line(pose, (int(pred[2]*8), int(pred[3]*8)), (int(pred[4]*8), int(pred[5]*8)), blue, 10)
    cv2.line(pose, (int(pred[4]*8), int(pred[5]*8)), (int(pred[6]*8), int(pred[7]*8)), blue, 10)

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
