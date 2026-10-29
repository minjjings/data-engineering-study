# Day 26. DAG·Task와 첫 실행

**6주 차 · 주간 1일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 25](../day25/README.md) · [Day 27 →](../day27/README.md)

이번 주에는 **Airflow로 배치 예약 실행** 내용을 다룬다. 오늘은 의존성을 가진 작은 DAG를 등록하고 실행한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 의존성을 가진 작은 DAG를 등록하고 실행한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

DAG는 작업의 선후 관계를 나타낸다. Airflow는 큰 데이터를 직접 옮기는 저장소가 아니라 언제 어떤 작업을 실행할지 관리하는 도구다. 작업이 실패하면 그 상태를 남기고 후속 작업을 막거나 재시도할 수 있다.

DAG 파일을 읽는 시점과 Task를 실행하는 시점은 다르다. 파일의 최상위에서 다운로드나 DB 쿼리를 실행하면 스케줄러가 읽을 때마다 부작용이 생길 수 있으므로 실제 작업은 Task 안에 둔다.

## 2장. 실습 준비

Airflow 3 계열은 공식 Docker Compose 안내로 별도 `infra/airflow/` 환경을 만든다. 루트 Compose는 PostgreSQL 실습용으로 유지한다. 해당 디렉터리에서 공식 compose 파일을 받고 `docker compose -p de-airflow up airflow-init`, `docker compose -p de-airflow up -d` 순서로 실행한다. 실제 사용 이미지 태그·설정·접속 방법을 기록한다. DAG는 루트 dags에 작성하고 공식 구성의 dags 마운트 경로에 복사한다. 컨테이너 CLI는 `docker compose -p de-airflow exec airflow-scheduler ...`로 실행한다. 아래 Airflow 명령은 그 컨테이너 안 기준이다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 26](../day26/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

### 환경을 처음 만드는 순서

저장소 루트에서 다음을 실행한다. [공식 Compose 안내](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)를 기준으로 Airflow 3.3.2를 사용한다.

```powershell
New-Item -ItemType Directory -Force infra/airflow | Out-Null
Set-Location infra/airflow
Invoke-WebRequest -Uri https://airflow.apache.org/docs/apache-airflow/3.3.2/docker-compose.yaml -OutFile compose.yaml
New-Item -ItemType Directory -Force dags,logs,plugins,config | Out-Null
Set-Content -Encoding ascii .env 'AIRFLOW_UID=50000'
docker compose -p de-airflow -f compose.yaml config --quiet
docker compose -p de-airflow -f compose.yaml up airflow-init
docker compose -p de-airflow -f compose.yaml up -d
docker compose -p de-airflow -f compose.yaml ps
Set-Location ../..
```

이후 DAG 원본은 루트 `dags/`에 작성하고 `infra/airflow/dags/`로 복사한다. 예를 들어 `Copy-Item dags/market_demo.py infra/airflow/dags/market_demo.py`로 반영한다. UI는 `http://localhost:8080`이며 초기 계정은 공식 Compose의 `airflow` / `airflow`다. 다른 서비스가 8080을 사용하면 Compose의 호스트 포트를 바꾼다.

루트에서 CLI를 실행할 때는 `docker compose -p de-airflow -f infra/airflow/compose.yaml exec airflow-scheduler airflow dags list-import-errors`처럼 파일 경로를 포함한다. 실습 종료는 같은 경로를 지정한 `down`을 사용하고 볼륨은 유지한다.

### 첫 DAG 작성

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
from airflow.sdk import dag, task
import pendulum

@dag(schedule=None, start_date=pendulum.datetime(2026, 10, 26, tz="UTC"),
     catchup=False)
def market_demo():
    @task
    def collect():
        return {"path": "/tmp/sample.json", "count": 4}
    @task
    def validate(metadata):
        assert metadata["count"] == 4
        print(metadata)
    validate(collect())

market_demo()
```

**예상 결과와 확인 기준:** dags/market_demo.py로 저장·복사하면 market_demo에 collect → validate 두 Task가 나타난다. 수동 실행은 4건 메타데이터를 전달하며 실제 파일은 아직 만들지 않는다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 공식 환경의 이미지 버전·메모리·UI 접속 절차를 기록한다.
2. airflow dags list-import-errors로 import 오류가 없는지 확인한다.
3. UI에서 수동 실행하고 각 Task 로그와 상태를 저장한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day26/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** Task 바깥에서 파일을 저장하면 스케줄러 재탐색 때 어떤 문제가 생길까?

## 리뷰 기록 양식

```text
날짜 / 사용 시간:
작성한 코드·SQL·설정 경로:
실행 명령과 입력:
예상 결과 / 실제 결과:
실패·경계 상황 또는 재실행 결과:
오늘 개념을 내 말로 설명:
오류 메시지 / 해결 과정 / 남은 질문:
완료한 항목과 근거 / 다음에 보완할 항목:
```

## 참고 자료와 다음 학습

[Docker Compose 환경](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) · [첫 DAG](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/fundamentals.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 25](../day25/README.md) · [Day 27 →](../day27/README.md)
