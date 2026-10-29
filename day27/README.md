# Day 27. XCom과 실제 수집·적재 연결

**6주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 26](../day26/README.md) · [Day 28 →](../day28/README.md)

이번 주에는 **Airflow로 배치 예약 실행** 내용을 다룬다. 오늘은 작업 사이에는 작은 메타데이터를 전달한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 작업 사이에는 작은 메타데이터를 전달한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

XCom은 Task 사이에 작은 값을 전달하는 기능이다. 전체 원본을 넣기보다 공유 저장소 경로·batch_id·건수를 넘기면 메타데이터 DB 부담을 줄일 수 있다. 경로를 넘겼다고 다른 컨테이너에서 파일이 보이는 것은 아니다.

Task가 별도 프로세스·컨테이너에서 실행될 수 있으므로 /tmp 같은 로컬 경로는 공유를 보장하지 않는다. 학습 환경에서는 공통 볼륨 경로를 사용하고 나중에는 S3 객체 경로로 확장한다. DB 연결은 컨테이너에서 접근 가능한 주소로 설정한다.

## 2장. 실습 준비

Airflow 3 계열은 공식 Docker Compose 안내로 별도 `infra/airflow/` 환경을 만든다. 루트 Compose는 PostgreSQL 실습용으로 유지한다. 해당 디렉터리에서 공식 compose 파일을 받고 `docker compose -p de-airflow up airflow-init`, `docker compose -p de-airflow up -d` 순서로 실행한다. 실제 사용 이미지 태그·설정·접속 방법을 기록한다. DAG는 루트 dags에 작성하고 공식 구성의 dags 마운트 경로에 복사한다. 컨테이너 CLI는 `docker compose -p de-airflow exec airflow-scheduler ...`로 실행한다. 아래 Airflow 명령은 그 컨테이너 안 기준이다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 26](../day26/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
from pathlib import Path
import json

# collect Task 안에서 실행할 코드. 공유 볼륨 /opt/airflow/data를 먼저 연결한다.
batch_id = "2026-10-26"
path = Path("/opt/airflow/data") / batch_id / "raw.json"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps([{"symbol": "QQQ", "close": "620.50"}]), encoding="utf-8")
metadata = {"path": str(path), "batch_id": batch_id, "count": 1}
print(metadata)
```

**예상 결과와 확인 기준:** 공유 볼륨에 Raw 한 건이 저장되고 메타데이터만 출력된다. 다른 Task에서 같은 경로를 실제 읽어야 전달 검증이 끝난다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. Day 26 collect에 예제를 넣고 validate가 파일을 다시 읽도록 바꾼다.
2. Day 5주 적재 함수를 세 번째 Task로 연결하고 컨테이너용 DSN을 설정한다.
3. 원본 본문 대신 경로·batch_id·건수만 XCom에 남는지 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day27/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** Worker가 다른 컴퓨터로 이동해도 현재 공유 경로는 유효할까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 26](../day26/README.md) · [Day 28 →](../day28/README.md)
