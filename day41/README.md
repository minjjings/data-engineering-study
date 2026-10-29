# Day 41. incremental 모델과 unique_key

**9주 차 · 주간 1일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 40](../day40/README.md) · [Day 42 →](../day42/README.md)

이번 주에는 **dbt 증분 모델과 Airflow 연결** 내용을 다룬다. 오늘은 전체 생성과 증분 실행 경로를 분리한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 전체 생성과 증분 실행 경로를 분리한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

증분 모델은 기존 표가 있으면 일부 입력만 반영해 실행 비용을 줄인다. unique_key는 증분 반영 시 같은 행을 판단하는 설정이며 DB에 자동으로 유일 제약을 만든다는 뜻은 아니다. 오늘은 PostgreSQL 어댑터의 delete+insert 전략으로 시작한다.

## 2장. 실습 준비

기존 dbt 프로젝트를 사용하며 `seeds/incremental_input.csv`에 symbol,trade_date,close_price 헤더와 QQQ,2026-10-26,620.50 및 SPY,2026-10-26,680.20 두 행을 준비한다. Day 41~44에서는 이 seed를 바꾸며 실험한다. Airflow 연동은 Worker 이미지 안에도 같은 dbt 어댑터·프로젝트·profile을 배치해야 한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 41](../day41/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
-- models/marts/fct_prices_incremental.sql
{{ config(materialized='incremental',
          unique_key=['symbol', 'trade_date'],
          incremental_strategy='delete+insert') }}
SELECT symbol, trade_date::date AS trade_date,
       close_price::numeric AS close_price
FROM {{ ref('incremental_input') }}
```

**예상 결과와 확인 기준:** dbt seed --select incremental_input 뒤 모델을 두 번 실행해도 목표 표는 2행이다. 현재는 입력 전체를 읽으며 범위 필터는 다음 수업에서 추가한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 어댑터가 delete+insert를 지원하는지 설치 버전 문서에서 확인한다.
2. 동일 입력 2회 실행 후 키·가격·건수를 비교한다.
3. 업무 키의 not_null·복합 유일성 테스트를 연결한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day41/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** unique_key를 설정했는데 입력 자체에 같은 키가 두 번 있으면 안전할까?

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

[증분 모델](https://docs.getdbt.com/docs/build/incremental-models) · [증분 전략](https://docs.getdbt.com/docs/build/incremental-strategy)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 40](../day40/README.md) · [Day 42 →](../day42/README.md)
