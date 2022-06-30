keypoint detection 모델링
======================

사용 데어터: https://aihub.or.kr/aidata/34116

## 파일
* **classify_json.py**: json 형식으로 된 파일을 csv로 변환
* **cp1.ipynb**: 우선 2000개의 trainig 데이터로 학습 후 확인

![image](https://user-images.githubusercontent.com/64140376/176635602-e3d92519-1786-4422-bc56-b0ce74c2626a.png)


## 실행방법
1. conda create -n 가상환경이름 python=3.8
2. conda activate 가상환경이름
3. 아래 명령어 입력(모델 학습중이어서 아직 requirements.txt 못만들었음)
```pip install pandas
pip install matplotlib
pip install opencv-python
pip install tqdm
pip install tensorflow
```

## 진행중
* 전체 Trainig 데이터 사용해서 학습중
