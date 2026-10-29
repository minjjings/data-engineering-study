# Day 91. WAL·논리 복제와 CDC용 DB

**19주 차 · 주간 1일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 90](../day90/README.md) · [Day 92 →](../day92/README.md)

이번 주에는 **PostgreSQL CDC와 Debezium** 내용을 다룬다. 오늘은 원천 변경을 읽을 수 있는 독립 DB를 준비한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 원천 변경을 읽을 수 있는 독립 DB를 준비한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

CDC는 추가·수정·삭제를 변경 이벤트로 전달한다. PostgreSQL 커넥터는 논리 복제로 WAL 변경을 읽는다. 복제 슬롯이 지연되면 WAL이 쌓일 수 있어 동작 원리와 정리 책임을 함께 알아야 한다.

## 2장. 실습 준비

시장 DB와 분리한 CDC용 PostgreSQL을 Day 91에서 만든다. Kafka는 Day 81의 동일 Compose 네트워크를 사용하고 Connect는 kafka:29092로 접속한다. 공식 튜토리얼과 맞는 Debezium Connect 이미지 태그를 고정한다. localhost:8083은 호스트에서 보는 Connect REST 주소다. JSON에는 학습용 로컬 비밀번호만 사용한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 91](../day91/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```yaml
# infra/kafka/compose.yaml의 services에 추가한다.
  cdc-postgres:
    image: postgres:17
    container_name: de-cdc-postgres
    command: ["postgres", "-c", "wal_level=logical", "-c", "max_replication_slots=4", "-c", "max_wal_senders=4"]
    environment:
      POSTGRES_USER: cdc_lab
      POSTGRES_PASSWORD: cdc_local_only
      POSTGRES_DB: cdc_db
    ports: ["127.0.0.1:5434:5432"]
    volumes: ["cdc_data:/var/lib/postgresql/data"]
```

**예상 결과와 확인 기준:** SHOW wal_level은 logical이다. 기존 market_db의 설정과 데이터는 유지한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 예제를 기존 services에 합치고 volumes에 cdc_data를 추가한 뒤 config --quiet로 검사한다.
2. CDC DB에 public.prices(id integer PRIMARY KEY, symbol text, price numeric)를 만든다.
3. id 1 QQQ 620.50과 id 2 SPY 680.20을 넣고 wal_level·PK·슬롯 목록을 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day91/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

설정 예제는 지정한 파일의 위치에 넣는다. 일부 설정만 보인 경우 기존 키에 병합하고 같은 최상위 키를 중복 작성하지 않는다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** PK 없는 테이블의 수정·삭제는 대상 행을 어떻게 식별할까?

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

[PostgreSQL 커넥터](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) · [튜토리얼](https://debezium.io/documentation/reference/stable/kc-tutorial.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 90](../day90/README.md) · [Day 92 →](../day92/README.md)
