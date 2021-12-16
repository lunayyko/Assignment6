# Assignment6

원티드x위코드 백엔드 프리온보딩 과제6
- 과제 출제 기업 정보
  - 기업명 : 디어코퍼레이션
    - [디어 사이트](https://web.deering.co/)
    - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/59051)

## Members
| 이름 | github                                    | 담당 기능      |
|-----|--------------------------------------------|------------ |
|김태우 |[jotasic](https://github.com/jotasic)       | 배포, 퀵보드리스트 |
|고유영 |[lunayyko](https://github.com/lunayyko)     | 퀵보드대여     |
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | 퀵보드반납     |
|최신혁 |[shchoi94](https://github.com/shchoi94)     | 퀵보드대여, 반납|
|박세원 |[sw-develop](https://github.com/sw-develop) | 개인사정으로 불참|

## 과제 내용
<details>
<summary>과제내용 보기</summary>
<div markdown="1">
  
### **[필수 포함 사항]**
- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

### 주요 평가 사항
- 주어진 정보를 기술적으로 설계하고 구현할 수 있는 역량
- 확장성을 고려한 시스템 설계 및 구현

### 과제 안내
디어는 사용자의 요금을 계산하기 위해 다양한 상황을 고려합니다. 
- 우선 지역별로 다양한 요금제를 적용하고 있습니다. 예를 들어 건대에서 이용하는 유저는 기본요금 790원에 분당요금 150원, 여수에서 이용하는 유저는 기본요금 300원에 분당요금 70원으로 적용됩니다.
- 할인 조건도 있습니다. 사용자가 파킹존에서 반납하는 경우 요금의 30%를 할인해주며, 사용자가 마지막 이용으로부터 30분 이내에 다시 이용하면 기본요금을 면제해줍니다.
- 벌금 조건도 있습니다. 사용자가 지역 바깥에 반납한 경우 얼마나 멀리 떨어져있는지 거리에 비례하는 벌금을 부과하며, 반납 금지로 지정된 구역에 반납하면 6,000원의 벌금을 요금에 추과로 부과합니다.
- 예외도 있는데, 킥보드가 고장나서 정상적인 이용을 못하는 경우의 유저들을 배려하여 1분 이내의 이용에는 요금을 청구하지 않고 있습니다.

최근에 다양한 할인과 벌금을 사용하여 지자체와 협력하는 경우가 점점 많아지고 있어 요금제에 새로운 할인/벌금 조건을 추가하는 일을 쉽게 만드려고 합니다. 어떻게 하면 앞으로 발생할 수 있는 다양한 할인과 벌금 조건을 기존의 요금제에 쉽게 추가할 수 있는 소프트웨어를 만들 수 있을까요? 

우선은 사용자의 이용에 관한 정보를 알려주면 현재의 요금 정책에 따라 요금을 계산해주는 API를 만들어주세요. 그 다음은, 기능을 유지한 채로 새로운 할인이나 벌금 조건이 쉽게 추가될 수 있게 코드를 개선하여 최종 코드를 만들어주세요.


**다음과 같은 정보들이 도움이 될 것 같아요.**
- 요금제가 사용자 입장에서 합리적이고 이해가 쉬운 요금제라면 좋을 것 같아요.
- 앞으로도 할인과 벌금 조건은 새로운 조건이 굉장히 많이 추가되거나 변경될 것 같아요.
- 가장 최근의 할인/벌금 조건의 변경은 `특정 킥보드는 파킹존에 반납하면 무조건 무료` 였습니다.


**이용에는 다음과 같은 정보들이 있습니다.**
```
use_deer_name (사용자가 이용한 킥보드의 이름)
use_end_lat, use_end_lng (사용자가 이용을 종료할 때 위도 경도)
use_start_at, use_end_at (사용자가 이용을 시작하고 종료한 시간)
```

**데이터베이스에는 킥보드에 대해 다음과 같은 정보들이 있습니다.**
```
deer_name (킥보드의 이름으로 고유한 값)
deer_area_id (킥보드가 현재 위치한 지역의 아이디)
```

**데이터베이스에는 지역에 대해 다음과 같은 정보들이 있습니다.**
```
area_id (지역 아이디로 고유한 값)
area_bounday (지역을 표시하는 MySQL spatial data로 POLYGON)
area_center (지역의 중심점)
area_coords (지역의 경계를 표시하는 위도, 경도로 이루어진 점의 리스트)
```

**데이터베이스에는 파킹존에 대해 다음과 같은 정보들이 있습니다.**

```
parkingzone_id (파킹존 아이디로 고유한 값)
parkingzone_center_lat, parkingzone_center_lng (파킹존 중심 위도, 경도)
parkingzone_radius (파킹존의 반지름)
```

**데이터베이스에는 반납금지구역에 대해 다음과 같은 정보들이 있습니다.**
```
forbidden_area_id (반납금지구역 아이디로 고유한 값)
forbidden_area_boundary (반납금지구역을 표시하는 MySQL spatial data로 POLYGON)
forbidden_area_coords (반납금지구역의 경계를 표시하는 위도, 경도로 이루어진 점의 리스트)
```
</div>
</details>

## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Mysql 8.0-4479A1?style=for-the-badge&logo=Mysql&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>&nbsp;

## 모델링
![image](https://user-images.githubusercontent.com/8219812/142760881-8545f6f7-1068-4fd2-91fe-4ccb76ad9a61.png)


## API
- [Swagger](http://18.188.189.173:8051/docs/swagger/)

## 구현 기능
- 기본 기능인 퀵보드 대여 및 반납 기능만 구현하였고, 추가기능인 할인, 패널티 적용은 구현하지 못하였습니다.

### 퀵보드 대여
- 대여와 반납은 기본적으로 BoardingLog 로그성 데이터이자,   
  유저와 Deer의 관계성 테이블로 데이터를 관리하도록 하였습니다.

### 퀵보드 반납
- 대여와 반납은 기본적으로 BoardingLog 로그성 데이터이자,   
  유저와 Deer의 관계성 테이블로 데이터를 관리하도록 하였습니다.
- 퀵보드 반납 시 입력되는 위도와 경도 정보는 유효성 검사를 통하여 입력됩니다.
- 유저와 Deer의 관계성 테이블에서 사용자와 퀵보드, 현재 사용중인 상태를 True or False의 값으로 지정하여,   
  퀵보드의 반납 가능한 상태를 구분합니다.
- 퀵보드 반납 시 반납가능한 상태가 아니면 에러를 반환합니다.
- 지역별 기본요금과 분별 추가요금을 지정하여 이용시간을 기반으로 이용요금을 계산합니다.

### 퀵보드 List 출력
- limit, offset pagination을 적용하였고, Query String이 입력되지 않아도, limit가 기본적으로 20으로 적용되도록 하였습니다.

## 배포정보
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 |http://18.188.189.173:8051/          |    |


## API TEST 방법
1. 우측 링크를 클릭해서 swagger로 들어갑니다. [링크](http://18.188.189.173:8051/docs/swagger/)

2. 회원가입과 로그인을 진행해서 Access token을 획득합니다.

![image](https://user-images.githubusercontent.com/8219812/142761053-766dfa92-d149-4f86-a744-cb83179b130a.png)


3. 해당 Token을 우측 상단에 있는 `Authorize`버튼을 클릭한 후, 아래 이미지를 참고하여 입력합니다 (Token xxxxxxxxx)

![image](https://user-images.githubusercontent.com/8219812/142761033-67614029-8746-4318-8948-d4664a7b02ce.png)


4. 퀵보드 대여 및 반납 Test를 진행합니다.

![image](https://user-images.githubusercontent.com/8219812/142761079-dd7505f3-cbb3-46dd-972b-e6f2ae063db5.png)


## 설치 및 실행 방법
<details>
<summary>설치 및 실행 방법 자세히 보기</summary>
<div markdown="1">
  
###  Local 개발 및 테스트용

1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    ```bash
    git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment6
    cd Assignment6
    ```

2. 가상 환경을 만들고 프로젝트에 사용한 python package를 받는다.
    ```bash
    conda create --name Assignment6 python=3.8
    conda actvate Assignment6
    pip install -r requirements.txt
    ```

3. db를 table 구조를 최신 model에 맞게 설정한다.
    ```bash
    python manage.py migrate
    ```

4. 서버를 실행한다.
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
  ```bash
  git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment6
  cd Assignment6
  ```
2. docker를 실행해서 서버를 구동한다.
  ```bash
  docker-compose -f ./docker-compose-deploy.yml up --build -d
  ```
</div>
</details>

## 폴더 구조
```bash
📦 Assignment6
 ┣ 📂 area
 ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 0001_initial.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 admin.py
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 tests.py
 ┃ ┗ 📜 views.py
 ┣ 📂 commands
 ┃ ┣ 📂 management
 ┃ ┃ ┣ 📂 commands
 ┃ ┃ ┃ ┣ 📜 __init__.py
 ┃ ┃ ┃ ┗ 📜 wait_for_db.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📜 __init__.py
 ┃ ┗ 📜 apps.py
 ┣ 📂 config
 ┃ ┗ 📂 nginx
 ┃ ┃ ┗ 📜 nginx.conf
 ┣ 📂 deer
 ┃ ┣ 📂 settings
 ┃ ┃ ┣ 📜 base.py
 ┃ ┃ ┣ 📜 deploy.py
 ┃ ┃ ┗ 📜 dev_local.py
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 asgi.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 wsgi.py
 ┣ 📂 user
 ┃ ┣ 📂 migrations
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 admin.py
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 serializers.py
 ┃ ┣ 📜 tests.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 views.py
 ┣ 📂 vehicle
 ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 0001_initial.py
 ┃ ┃ ┣ 📜 0002_auto_20211121_1149.py
 ┃ ┃ ┣ 📜 0003_auto_20211121_1319.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 admin.py
 ┃ ┣ 📜 apps.py
 ┃ ┣ 📜 models.py
 ┃ ┣ 📜 serializers.py
 ┃ ┣ 📜 tests.py
 ┃ ┣ 📜 urls.py
 ┃ ┗ 📜 views.py
 ┣ 📜 .gitignore
 ┣ 📜 Dockerfile-deploy
 ┣ 📜 Dockerfile-dev
 ┣ 📜 README.md
 ┣ 📜 docker-compose-deploy.yml
 ┣ 📜 docker-compose-dev.yml
 ┣ 📜 manage.py
 ┣ 📜 pull_request_template.md
 ┗ 📜 requirements.txt
```


## TIL정리 (Blog)
- 김태우 : https://velog.io/@burnkim61/프리온보딩-과제-6
- 고유영 : https://lunayyko.github.io/wecode/2021/11/22/wantedxwecode-6-deer/

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 디어코퍼레이션에서 출제한 과제를 기반으로 만들었습니다.
