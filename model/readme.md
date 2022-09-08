keypoint detection 모델링
======================

사용 데어터: https://aihub.or.kr/aidata/34116

## 파일
* **classify_json.py**: json 형식으로 된 파일을 csv로 변환
* **cp1.ipynb**: 우선 2000개의 trainig 데이터로 학습 후 확인
* **cp1_2000_6.ipynb**: 데이터 2000개 / epochs 5
* **cp1_8000_6.ipynb**: 데이터 8000개 / epochs 5
* **cp1_8000.ipynb**: 데이터 8000개 / epochs 10 -> ResNet 적용 실패
* **cp1_16000_6 copy.ipynb**: 데이터 16000개 / epochs 15
* **cp1_32000.ipynb**: 데이터 32000개 / epochs 20 -> 최종모델!


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
