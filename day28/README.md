# Day 28. 실행 구간과 날짜 인자 전달

**6주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 27](../day27/README.md) · [Day 29 →](../day29/README.md)

이번 주에는 **Airflow로 배치 예약 실행** 내용을 다룬다. 오늘은 현재 시각 대신 DAG 실행 구간으로 처리한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 현재 시각 대신 DAG 실행 구간으로 처리한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

예약 실행의 논리적 구간은 프로그램이 실제 시작한 시각과 다르다. 하루치 작업이 지연되어 다음 날 실행되어도 원래 처리할 날짜는 같아야 한다. 이 때문에 now() 대신 data interval을 사용한다.

수동 실행과 예약 실행의 구간은 timetable에 따라 다를 수 있다. 날짜만 잘라서 넘기기 전에 타임존과 시작 포함·종료 제외 규칙을 확인한다. 오늘은 UTC 일간 구간을 명시적으로 로깅하고 기존 CLI의 --start·--end에 연결한다.

## 2장. 실습 준비

Airflow 3 계열은 공식 Docker Compose 안내로 별도 `infra/airflow/` 환경을 만든다. 루트 Compose는 PostgreSQL 실습용으로 유지한다. 해당 디렉터리에서 공식 compose 파일을 받고 `docker compose -p de-airflow up airflow-init`, `docker compose -p de-airflow up -d` 순서로 실행한다. 실제 사용 이미지 태그·설정·접속 방법을 기록한다. DAG는 루트 dags에 작성하고 공식 구성의 dags 마운트 경로에 복사한다. 컨테이너 CLI는 `docker compose -p de-airflow exec airflow-scheduler ...`로 실행한다. 아래 Airflow 명령은 그 컨테이너 안 기준이다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 26](../day26/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
from airflow.sdk import get_current_context

# @task 함수 내부에 넣는다.
def report_interval():
    context = get_current_context()
    start = context["data_interval_start"]
    end = context["data_interval_end"]
    print({"start": start.isoformat(), "end": end.isoformat(),
           "run_id": context["run_id"]})
```

**예상 결과와 확인 기준:** Task 로그에 UTC 시작·종료·run_id가 남는다. DAG 정의를 schedule="@daily"로 바꾼 후 예약 구간을 확인한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. start_date를 고정하고 실제 첫 예약 실행이 처리할 구간을 예상한다.
2. 같은 논리 구간을 다시 실행해 입력 파일 경로와 적재 결과가 같은지 확인한다.
3. 수동 실행 구간을 로그에서 확인한 뒤 Day 24 인자로 변환한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day28/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 한국 시각 0시 기준 거래일과 UTC 일간 구간을 그대로 섞으면 어떤 경계 문제가 생길까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 27](../day27/README.md) · [Day 29 →](../day29/README.md)
