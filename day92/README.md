# Day 92. Kafka Connect와 커넥터 등록

**19주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 91](../day91/README.md) · [Day 93 →](../day93/README.md)

이번 주에는 **PostgreSQL CDC와 Debezium** 내용을 다룬다. 오늘은 DB와 Kafka 사이의 변경 수집 경로를 연결한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- DB와 Kafka 사이의 변경 수집 경로를 연결한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

Connect는 커넥터 설정과 실행 상태를 관리한다. Worker 기동과 PostgreSQL 커넥터 실행은 다른 단계다. plugin 목록·connector 상태·task 상태를 각각 확인하고 내부 네트워크 주소를 사용한다.

## 2장. 실습 준비

시장 DB와 분리한 CDC용 PostgreSQL을 Day 91에서 만든다. Kafka는 Day 81의 동일 Compose 네트워크를 사용하고 Connect는 kafka:29092로 접속한다. 공식 튜토리얼과 맞는 Debezium Connect 이미지 태그를 고정한다. localhost:8083은 호스트에서 보는 Connect REST 주소다. JSON에는 학습용 로컬 비밀번호만 사용한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 91](../day91/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

### Connect 서비스 추가

Day 81의 `infra/kafka/compose.yaml`에서 기존 `services` 아래에 합친다. [공식 Connect 튜토리얼](https://debezium.io/documentation/reference/stable/kc-tutorial.html)의 Debezium 3.7 이미지를 사용하며, PostgreSQL 커넥터 설정은 뒤의 JSON을 사용한다.

```yaml
  connect:
    image: quay.io/debezium/connect:3.7
    ports: ["127.0.0.1:8083:8083"]
    environment:
      BOOTSTRAP_SERVERS: kafka:29092
      GROUP_ID: market-connect
      CONFIG_STORAGE_TOPIC: market_connect_configs
      OFFSET_STORAGE_TOPIC: market_connect_offsets
      STATUS_STORAGE_TOPIC: market_connect_statuses
      CONFIG_STORAGE_REPLICATION_FACTOR: 1
      OFFSET_STORAGE_REPLICATION_FACTOR: 1
      STATUS_STORAGE_REPLICATION_FACTOR: 1
    depends_on: [kafka, cdc-postgres]
```

루트 PowerShell에서 시작하고 plugin 목록을 확인한다. 목록에 `io.debezium.connector.postgresql.PostgresConnector`가 있어야 한다.

```powershell
docker compose -p de-stream -f infra/kafka/compose.yaml up -d
Invoke-RestMethod http://localhost:8083/connector-plugins
```

### 커넥터 설정 작성과 등록

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```json
{
  "name": "market-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "cdc-postgres", "database.port": "5432",
    "database.user": "cdc_lab", "database.password": "cdc_local_only",
    "database.dbname": "cdc_db", "topic.prefix": "marketcdc",
    "plugin.name": "pgoutput", "slot.name": "market_slot",
    "publication.name": "market_publication",
    "table.include.list": "public.prices", "snapshot.mode": "initial"
  }
}
```

**예상 결과와 확인 기준:** Connect 준비 후 등록하면 connector와 task가 RUNNING이어야 한다. DB 주소는 localhost가 아닌 Compose 서비스명이다.

JSON을 `day92/connector.json`에 저장하고 최초 한 번 등록한다. 이미 등록되어 있다면 POST를 반복하지 말고 기존 설정·상태를 확인한다.

```powershell
$connectorBody = Get-Content -Raw -Encoding UTF8 day92/connector.json
Invoke-RestMethod -Method Post -Uri http://localhost:8083/connectors -ContentType application/json -Body $connectorBody
Invoke-RestMethod http://localhost:8083/connectors/market-cdc/status | ConvertTo-Json -Depth 10
```

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 공식 Connect 이미지를 같은 Compose에 추가하고 BOOTSTRAP_SERVERS=kafka:29092, GROUP_ID, CONFIG_STORAGE_TOPIC, OFFSET_STORAGE_TOPIC, STATUS_STORAGE_TOPIC을 설정한다.
2. 단일 브로커의 내부 토픽 복제 계수를 1로 두고 8083 포트를 로컬에 연다.
3. JSON을 day92/connector.json으로 저장해 Invoke-RestMethod로 POST /connectors에 등록하고 GET /connectors/market-cdc/status를 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day92/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

YOUR_BUCKET 같은 예시 이름을 본인의 실습 환경 값으로 바꾼다. JSON 작성과 실제 서비스 적용·검증을 구분한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** Connect에서 database.hostname=localhost는 어느 DB를 가리킬까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 91](../day91/README.md) · [Day 93 →](../day93/README.md)
