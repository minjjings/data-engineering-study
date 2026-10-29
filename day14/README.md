# Day 14. UPSERT와 증분 상태 저장

**3주 차 · 주간 4일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 13](../day13/README.md) · [Day 15 →](../day15/README.md)

이번 주에는 **데이터 모델링·트랜잭션·증분 적재** 내용을 다룬다. 오늘은 동일 키 수정과 처리 상태 전진을 한 트랜잭션에서 처리한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 동일 키 수정과 처리 상태 전진을 한 트랜잭션에서 처리한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

UPSERT는 키가 없으면 삽입하고 있으면 수정하는 방식이다. ON CONFLICT가 동작하려면 충돌을 판단할 UNIQUE 또는 PK가 필요하다. 같은 입력이 반복되어도 행 수가 늘지 않는 것은 멱등 적재의 출발점이다.

Watermark는 성공한 배치가 읽은 상한까지 전진시킨다. 여러 작업이 동시에 상태를 갱신하면 경쟁이 생기므로 오늘은 단일 작업만 실행한다. 운영에서는 상태 행 잠금, 비교 후 갱신, 원천 변경 로그 등을 검토해야 한다.

## 2장. 실습 준비

Day 2 PostgreSQL을 사용한다. 학습용 테이블은 `lab_` 접두사나 TEMP로 구분하고 Raw는 수정하지 않는다. Day 14~15는 Day 11~12에서 설계한 키·트랜잭션을 확장한다. SQL은 `sql/week03/`에 기록한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 11](../day11/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
CREATE TEMP TABLE lab_upsert (
    symbol text, trade_date date, price numeric,
    PRIMARY KEY (symbol, trade_date)
);
CREATE TEMP TABLE lab_state (name text PRIMARY KEY, last_id bigint);
INSERT INTO lab_state VALUES ('prices', 0);
BEGIN;
INSERT INTO lab_upsert VALUES ('QQQ', '2026-10-26', 621.00)
ON CONFLICT (symbol, trade_date)
DO UPDATE SET price = EXCLUDED.price;
UPDATE lab_state SET last_id = 3 WHERE name = 'prices';
COMMIT;
SELECT * FROM lab_upsert;
SELECT * FROM lab_state;
```

**예상 결과와 확인 기준:** 가격 1건과 last_id 3을 확인한다. BEGIN~COMMIT 블록만 다시 실행해도 가격은 1건이다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 동일 블록을 두 번 실행하고 건수와 값을 비교한다.
2. 트랜잭션 안의 UPSERT 뒤에 오류를 넣어 ROLLBACK하고 가격·상태가 함께 유지되는지 확인한다.
3. lab_upsert·lab_state의 영구 DDL과 범위 상한을 고정하는 적재 SQL을 작성한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day14/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 더 오래된 수정 이벤트가 나중에 들어오면 무조건 UPSERT해도 될까?

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

[트랜잭션](https://www.postgresql.org/docs/17/tutorial-transactions.html) · [INSERT와 ON CONFLICT](https://www.postgresql.org/docs/17/sql-insert.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 13](../day13/README.md) · [Day 15 →](../day15/README.md)
