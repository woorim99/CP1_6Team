# ***※간단 설명※***

프로젝트 이름: dancesite

앱 이름: dancecheck

DB: 임시로 데이터를 2개 넣고 만든 sqlite3

구현한 기능: 홈화면, 노래 선택, 이미지보여주기, 팀구성 및 역할 화면

<br/>
<br/>

# ***※추가 설명※***

노래 선택 후 결과는 임의로 고른 이미지 1장 나오게 했습니다.

결과에 이미지 3개가 나오는데 위에서부터 원본,원본 + 키포인트, 스켈레톤 순으로 보여줍니다.

코드에서 주석부분은 참고용으로 적어둔 것입니다.

<br/>
<br/>

# ***※사용 설명※***

터미널에서 실행 코드: python manage.py runserver
(※manage.py가 있는 dancesite 위치에서 실행)

기본 url에 /dancecheck/를 붙여주시면 됩니다.

상단에 SM로고, Home, display, members이 있고 그밑에 Learn more과 music choice가 있습니다.

시간상 display와 Learn more은 미구현 상태여서 누르시면 에러가 뜹니다.

SM로고와 Home을 누르면 Home화면으로 갑니다.

members를 누르면 팀 구성과 역할이 나옵니다.

music choice에서 노래를 선택하시면 이미지 3개가 나옵니다.

이미지에 대한 설명은 추가 설명과 같습니다.

<br/>
<br/>

# ***※주의사항※***
model을 develop하실 분은 develop한 model를 부호화 하신 뒤 dancecheck폴더 안에 넣고 dancecheck폴더 안에 있는 view.py에서 load_model('dancecheck/model32000')부분을 수정하시면 됩니다.

<br/>
<br/>
