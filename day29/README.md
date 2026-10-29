# Day 29. 재시도와 실패 재현

**6주 차 · 주간 4일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 28](../day28/README.md) · [Day 30 →](../day30/README.md)

이번 주에는 **Airflow로 배치 예약 실행** 내용을 다룬다. 오늘은 실패 Task만 다시 실행해도 안전한 저장 방식을 만든다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 실패 Task만 다시 실행해도 안전한 저장 방식을 만든다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

Airflow 재시도는 Task 코드를 다시 실행한다. 앞부분에서 이미 저장한 데이터가 있다면 두 번째 실행에서 중복될 수 있다. 따라서 재시도 횟수 설정과 함께 업무 키 UPSERT·원자적 저장을 적용해야 한다.

의도한 실패를 통해 후속 Task가 실행되지 않는지, 로그에 원인이 남는지 확인한다. 실패를 return False로 표현하면 Task 자체는 성공으로 볼 수 있으므로 진행 불가능한 상황에서는 예외를 발생시킨다.

## 2장. 실습 준비

Airflow 3 계열은 공식 Docker Compose 안내로 별도 `infra/airflow/` 환경을 만든다. 루트 Compose는 PostgreSQL 실습용으로 유지한다. 해당 디렉터리에서 공식 compose 파일을 받고 `docker compose -p de-airflow up airflow-init`, `docker compose -p de-airflow up -d` 순서로 실행한다. 실제 사용 이미지 태그·설정·접속 방법을 기록한다. DAG는 루트 dags에 작성하고 공식 구성의 dags 마운트 경로에 복사한다. 컨테이너 CLI는 `docker compose -p de-airflow exec airflow-scheduler ...`로 실행한다. 아래 Airflow 명령은 그 컨테이너 안 기준이다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 26](../day26/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
from datetime import timedelta
from airflow.sdk import task

@task(retries=2, retry_delay=timedelta(seconds=10))
def validate_count(actual, expected):
    if actual != expected:
        raise ValueError(f"row count mismatch: {actual} != {expected}")
    return {"validated": actual}
```

**예상 결과와 확인 기준:** 3과 4를 전달하면 최초 실행과 재시도 2회 모두 실패한다. 4와 4를 전달하면 성공한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. DAG에 검증 Task를 연결하고 실패 시 후속 적재·공개가 차단되는지 확인한다.
2. 수집 성공·DB 적재 실패를 만든 뒤 실패 Task만 재실행한다.
3. 시도 횟수별 로그·최종 DB 행 수·중복 여부를 비교한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day29/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 품질 규칙 위반처럼 같은 입력으로 계속 실패하는 경우도 재시도하는 것이 도움이 될까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 28](../day28/README.md) · [Day 30 →](../day30/README.md)
