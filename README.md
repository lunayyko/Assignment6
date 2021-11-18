# Assignment6

원티드x위코드 백엔드 프리온보딩 과제6
- 과제 출제 기업 정보
  - 기업명 : 디어코퍼레이션
    - [디어 사이트](https://web.deering.co/)
    - [wanted 채용공고 링크](https://www.wanted.co.kr/wd/59051)

## Members
| 이름 | github                                    | 담당 기능              |
|-----|--------------------------------------------|-------------------------|
|김태우 |[jotasic](https://github.com/jotasic)       | |
|고유영 |[lunayyko](https://github.com/lunayyko)     | |
|박지원 |[jiwon5304](https://github.com/jiwon5304)   | |
|최신혁 |[shchoi94](https://github.com/shchoi94)     | |
|박세원 |[sw-develop](https://github.com/sw-develop) | |

## 과제 내용

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


## 사용 기술 및 tools
> - Back-End :  <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Django 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Mysql 8.0-4479A1?style=for-the-badge&logo=Mysql&logoColor=white"/>
> - Deploy : <img src="https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=Amazon&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Docker-0052CC?style=for-the-badge&logo=Docker&logoColor=white"/>
> - ETC :  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>&nbsp;

## 모델링


## API

## 구현 기능


## 배포정보
---
|구분   |  정보          |비고|
|-------|----------------|----|
|배포플랫폼 | AWS EC2    |    |
|API 주소 |            |    |


## API TEST 방법
1. 우측 링크를 클릭해서 swagger로 들어갑니다. [링크]()


## 설치 및 실행 방법
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

3. 환경 설정 파일 복사하고 해당 디렉토리로 이동해서 내용을 수정한다.


4. db를 table 구조를 최신 model에 맞게 설정한다.
    ```bash
    python manage.py migrate
    ```

5. 서버를 실행한다.
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

###  배포용 
1. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
  ```bash
  git clone https://github.com/Wanted-Preonboarding-Backend-1st-G5/Assignment6
  cd Assignment6
  ```


## 폴더 구조
```bash

```


## TIL정리 (Blog)
- 김태우 :
- 고유영 :
- 박지원 : 
- 최신혁 :
- 박세원 :

# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 디어코퍼레이션에서 출제한 과제를 기반으로 만들었습니다.
