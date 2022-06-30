## json 파일로 되어있는 데이터를 csv파일로 변환

import os
import json
import pandas as pd

path = './K-pop 안무 영상/Training'
folder_list = os.listdir(path)
folder_list_py = [file for file in folder_list if file.startswith('[라벨]')]      # Trainig 폴더안에 [라벨]로 시작하는 폴더명들 리스트

folder_list2_py = []

for i in folder_list_py:
    path2 = path + '/'+ i
    folder_list2 = os.listdir(path2)
    folder_list2_py.extend([path + '/' + i + '/' + file for file in folder_list2 if file.endswith('F')])  # F로 끝나는 폴더 리스트

json_file_list = []

for i in folder_list2_py:
    json_file = os.listdir(i)
    json_file_list.extend([i + '/' + file for file in json_file if file.endswith('.json')])     # json파일 리스트

df = pd.DataFrame(columns = ["image", "center_hip_x", "center_hip_y", "left_hip_x", "left_hip_y", "left_knee_x", "left_knee_y", "left_ankle_x", "left_ankle_y", "left_bigtoe_X", "left_bigtoe_y",
                "left_littletoe_x", "left_littletoe_y", "right_hip_x", "right_hip_y", "right_knee_x", "right_knee_y", "right_ankle_x", "right_ankle_y", "right_bigtoe_x", "right_bigtoe_y",
                "right_littletoe_x", "right_littletoe_y", "navel_x", "navel_y", "chest_x", "chest_y", "neck_x", "neck_y", "left_shoulder_x", "left_shoulder_y", "left_elbow_x", "left_elbow_y",
                "left_wrist_x", "left_wrist_y", "left_palm_thumb_x", "left_palm_thumb_y", "left_palm_pinky_x", "left_palm_pinky_y", "right_shoulder_x", "right_shoulder_y", "right_elbow_x", "right_elbow_y",
                "right_wrist_x", "right_wrist_y", "right_palm_thumb_x", "right_palm_thumb_y", "right_palm_pinky_x", "right_palm_pinky_y", "nose_x", "nose_y", "left_eye_x", "left_eye_y",
                "right_eye_x", "right_eye_y", "left_ear_x", "left_ear_y", "right_ear_x", "right_ear_y"])
print(df.columns)


# for i in range(2000): # 데이터 2000개만
for i in range(len(json_file_list)):   #모든 데이터
    a_json = open(json_file_list[i], encoding = 'utf-8')
    a_dict = json.load(a_json)
    a = a_dict["annotations"][0]["keypoints"]
    print(i)
    for j in a:
        if j == 0:
            a.remove(0)
        elif j == 1:
            a.remove(1)
        elif j == 2:
            a.remove(2) 
    a.insert(0, json_file_list[i].replace('json', 'jpg').replace('[라벨]', '[원천]'))
    df.loc[i] = a
    
df.to_csv("train.csv", mode='w')