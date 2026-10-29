# Day 34. ref와 intermediate 모델 의존성

**7주 차 · 주간 4일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 33](../day33/README.md) · [Day 35 →](../day35/README.md)

이번 주에는 **dbt 프로젝트와 계층별 SQL 모델** 내용을 다룬다. 오늘은 정제와 중복 제거를 연결하고 실행 순서를 자동으로 만든다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 정제와 중복 제거를 연결하고 실행 순서를 자동으로 만든다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

ref는 다른 모델을 가리키며 의존 관계를 만든다. DB의 실제 생성 이름을 코드에 고정하지 않아 환경별 스키마 변경에 대응하기 쉽다. 중복 제거 정책은 모델 이름·설명·SQL에 함께 드러나야 한다.

## 2장. 실습 준비

전용 환경에 dbt-postgres를 설치하고 dbt --version을 기록한다. Day 31에서 dbt/market 프로젝트와 dbt/profiles/profiles.yml을 만든다. 이후 dbt 명령은 dbt/market에서 실행하고 DBT_PROFILES_DIR을 profiles 디렉터리 절대 경로로 설정한다. 가상환경의 dbt 실행 파일을 사용한다. DB는 호스트 127.0.0.1:5433, 원천은 public.raw_market_prices다. SQL 모델은 파일에 저장하며 psql에 Jinja 문법을 직접 입력하지 않는다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 31](../day31/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
-- models/intermediate/int_latest_prices.sql
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY symbol, trade_date
        ORDER BY collected_at DESC, id DESC
    ) AS rn
    FROM {{ ref('stg_prices') }}
    WHERE close_price > 0 AND symbol IS NOT NULL AND trade_date IS NOT NULL
)
SELECT symbol, trade_date, close_price FROM ranked WHERE rn = 1
```

**예상 결과와 확인 기준:** dbt run --select +int_latest_prices는 선행 모델을 포함해 실행하며 최초 샘플 결과는 2행이다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 동일한 collected_at에서 id를 보조 정렬로 쓰는 이유를 설명한다.
2. ref를 쓴 모델의 compiled SQL을 target에서 확인한다.
3. 최신 원본 우선 정책으로 바꾼 별도 실험과 결과 차이를 기록한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day34/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** dbt run --select int_latest_prices만 실행할 때 선행 표가 없으면 어떻게 될까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 33](../day33/README.md) · [Day 35 →](../day35/README.md)
