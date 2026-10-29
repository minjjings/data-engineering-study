# Day 102. 처리 건수·실패율·최신성 지표

**21주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 101](../day101/README.md) · [Day 103 →](../day103/README.md)

이번 주에는 **로그·지표·모니터링과 장애 대응** 내용을 다룬다. 오늘은 무엇을 측정하는지와 단위를 명시한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 무엇을 측정하는지와 단위를 명시한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

처리 건수는 규모, 실행 시간은 처리 지연, 최신성은 데이터가 얼마나 오래되었는지 알려준다. 실패율은 어떤 실행을 분모로 잡는지에 따라 달라진다. 오늘은 성공·실패 실행 이력을 남기는 작은 지표 표를 만든다.

## 2장. 실습 준비

로그는 기존 배치의 batch_id를 기준으로 연결한다. Day102에서 PostgreSQL ops_lab.pipeline_runs를 만들고 실행 지표를 저장한다. Day103에서 별도 Grafana 환경을 추가해 PostgreSQL을 조회한다. Prometheus 추가는 선택 과제로 두고 이번 주는 하나의 지표 저장 경로를 완성한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 101](../day101/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
CREATE SCHEMA IF NOT EXISTS ops_lab;
CREATE TABLE IF NOT EXISTS ops_lab.pipeline_runs (
    run_id text PRIMARY KEY, batch_id text NOT NULL,
    started_at timestamptz NOT NULL, ended_at timestamptz,
    status text NOT NULL CHECK (status IN ('success', 'failed', 'running')),
    input_rows bigint, output_rows bigint,
    source_max_collected_at timestamptz
);
SELECT status, COUNT(*) FROM ops_lab.pipeline_runs GROUP BY status;
```

**예상 결과와 확인 기준:** 처음에는 빈 표다. 실제 실행을 적재한 뒤 집계 결과가 생긴다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 배치 시작·정상 종료·예외 종료에서 run_id별 상태를 기록한다.
2. 소요 시간과 최신성 초 단위를 SQL로 계산한다.
3. 정상 3회 이상·실패 1회 기록으로 실패율과 건수 기준선을 만든다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day102/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 프로세스가 강제 종료되어 running 상태만 남으면 어떻게 감지할까?

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

[Grafana PostgreSQL 데이터 소스](https://grafana.com/docs/grafana/latest/datasources/postgres/) · [알림](https://grafana.com/docs/grafana/latest/alerting/)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 101](../day101/README.md) · [Day 103 →](../day103/README.md)
