# Day 33. staging에서 가격 정제하기

**7주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 32](../day32/README.md) · [Day 34 →](../day34/README.md)

이번 주에는 **dbt 프로젝트와 계층별 SQL 모델** 내용을 다룬다. 오늘은 원본 보존과 정제 모델의 책임을 분리한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 원본 보존과 정제 모델의 책임을 분리한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

staging은 원천 구조를 분석에 쓸 일관된 이름과 자료형으로 바꾸는 입구다. 업무 집계를 한꺼번에 넣기보다 가격 파싱·날짜·키 정리를 담당하게 하면 규칙을 재사용하기 쉽다. 유효하지 않은 값은 원본에 남기고 별도 검사 대상으로 유지한다.

## 2장. 실습 준비

전용 환경에 dbt-postgres를 설치하고 dbt --version을 기록한다. Day 31에서 dbt/market 프로젝트와 dbt/profiles/profiles.yml을 만든다. 이후 dbt 명령은 dbt/market에서 실행하고 DBT_PROFILES_DIR을 profiles 디렉터리 절대 경로로 설정한다. 가상환경의 dbt 실행 파일을 사용한다. DB는 호스트 127.0.0.1:5433, 원천은 public.raw_market_prices다. SQL 모델은 파일에 저장하며 psql에 Jinja 문법을 직접 입력하지 않는다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 31](../day31/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
-- models/staging/stg_prices.sql
SELECT id, symbol, trade_date, collected_at,
    close_price AS raw_close_price,
    CASE WHEN close_price ~ '^[0-9]+([.][0-9]+)?$'
         THEN close_price::numeric END AS close_price
FROM {{ source('market_raw', 'raw_market_prices') }}
```

**예상 결과와 확인 기준:** 5행을 유지하며 원본 NULL·N/A 두 행의 close_price가 NULL이다. 양수와 중복 선택은 아직 적용하지 않는다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. dbt run --select stg_prices 후 raw_close_price와 close_price를 비교한다.
2. 0·음수·공백 처리 규칙을 명시하고 SQL에서 일관되게 적용한다.
3. staging의 행 수를 원본과 비교하고 차이가 있으면 근거를 기록한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day33/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 파싱 실패를 모두 NULL로 바꾸기만 하면 원인을 어떻게 추적할 수 있을까?

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

[Postgres 연결](https://docs.getdbt.com/docs/local/connect-data-platform/postgres-setup) · [ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 32](../day32/README.md) · [Day 34 →](../day34/README.md)
