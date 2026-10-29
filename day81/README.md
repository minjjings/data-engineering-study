# Day 81. Kafka와 KRaft 실행

**17주 차 · 주간 1일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 80](../day80/README.md) · [Day 82 →](../day82/README.md)

이번 주에는 **Kafka 이벤트·Producer·Consumer** 내용을 다룬다. 오늘은 Topic·Partition·Offset을 이해하고 단일 브로커를 띄운다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- Topic·Partition·Offset을 이해하고 단일 브로커를 띄운다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

Kafka는 이벤트를 순서 있는 로그에 보관한다. Topic은 이벤트 묶음, Partition은 병렬 처리 단위, Offset은 파티션 안의 위치다. 이번에는 KRaft 단일 노드로 배우며 복제 계수1은 노드 장애에 대한 내구성을 제공하지 않는다.

## 2장. 실습 준비

Day81에서 infra/kafka/compose.yaml을 만들고 `docker compose -p de-stream -f infra/kafka/compose.yaml up -d`로 실행한다. 호스트 Python·Spark는 localhost:9092, 같은 Compose의 Connect는 kafka:29092를 사용한다. CLI 예제는 PowerShell에서 실행하며 도구 경로는 /opt/kafka/bin/이다. Python 예제는 별도 가상환경에 confluent-kafka를 설치하고 사용 버전을 기록한다. 이 주차에서는 매일 Topic을 지우거나 offset을 초기화하지 않는다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 81](../day81/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```yaml
# infra/kafka/compose.yaml
services:
  kafka:
    image: apache/kafka:4.1.2
    container_name: de-kafka
    ports: ["127.0.0.1:9092:9092"]
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: EXTERNAL://:9092,INTERNAL://:29092,CONTROLLER://:9093
      KAFKA_ADVERTISED_LISTENERS: EXTERNAL://localhost:9092,INTERNAL://kafka:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: EXTERNAL:PLAINTEXT,INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_LOG_DIRS: /tmp/kraft-combined-logs
    volumes: ["kafka_data:/tmp/kraft-combined-logs"]
volumes:
  kafka_data:
```

**예상 결과와 확인 기준:** 기동 로그를 확인하고 아래 과제의Topic 생성·describe가 성공해야 준비된 것이다. 컨테이너 running만으로 판정하지 않는다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 위 Compose를 작성하고 버전·리스너·볼륨 경로를 기록한다.
2. kafka-topics.sh --bootstrap-server localhost:9092 --create --if-not-exists --topic market-prices --partitions 2 --replication-factor 1을 docker exec de-kafka 뒤에서 실행한다.
3. 같은 도구의 --describe --topic market-prices로 파티션2개를 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day81/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

설정 예제는 지정한 파일의 위치에 넣는다. 일부 설정만 보인 경우 기존 키에 병합하고 같은 최상위 키를 중복 작성하지 않는다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** Offset 숫자가 다른 파티션에서도 전역적으로 같은 의미를 가질까?

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

[Kafka 4.1 시작](https://kafka.apache.org/41/getting-started/quickstart/) · [Python 클라이언트](https://docs.confluent.io/kafka-clients/python/current/overview.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 80](../day80/README.md) · [Day 82 →](../day82/README.md)
