# Day 3. JOIN과 데이터 모델링 첫걸음

**1주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 2](../day02/README.md) · [Day 4 →](../day04/README.md)

이번 주에는 **파이프라인의 역할과 SQL 입문** 내용을 다룬다. 오늘은 종목 정보를 별도 테이블로 나누고 가격과 연결한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 종목 정보를 별도 테이블로 나누고 가격과 연결한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

가격 행마다 종목 이름을 반복 저장하면 이름을 바꿀 때 여러 행을 수정해야 한다. 종목은 종목 표에, 가격은 가격 표에 저장하고 `symbol`로 연결하면 정보의 책임이 분명해진다. 테이블을 어떻게 나눌지 정하는 작업이 데이터 모델링이다.

JOIN은 두 표에서 연결 조건이 맞는 행을 조합한다. LEFT JOIN은 왼쪽 가격을 모두 보존하므로 기준 정보가 없는 종목도 확인할 수 있다. 오른쪽에 같은 symbol이 여러 개면 가격 행이 늘어날 수 있으므로 종목 키의 유일성도 검사해야 한다.

## 2장. 실습 준비

Day 2의 PostgreSQL 환경을 사용한다. 저장소 최상위 PowerShell에서 `docker compose up -d` 후 `docker exec -it de-postgres psql -U de_user -d market_db`로 접속한다. DBeaver·IntelliJ의 SQL 편집기를 사용한다면 `market_db`에 연결한다. 원본 5건을 유지하며, 먼저 CTE로 기준 정보를 정의한 한 문장짜리 JOIN을 실행한다. TEMP 테이블 방식은 뒤에서 별도로 비교한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 1](../day01/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

아래 `WITH`부터 마지막 세미콜론까지 **전체를 한 번에 실행**한다. `WITH`는 다음 SELECT에서만 사용할 기준 정보를 정의한다. 별도의 CREATE·INSERT나 이전 연결의 임시 테이블이 필요하지 않다.

```sql
WITH day03_symbols (symbol, name) AS (
    VALUES ('QQQ', '가상 기술 ETF')
)
SELECT p.id, p.symbol, s.name, p.close_price
FROM public.raw_market_prices AS p
LEFT JOIN day03_symbols AS s ON p.symbol = s.symbol
ORDER BY p.id;
```

**예상 결과와 확인 기준:** Day 2 원본이 5건이면 결과도 5건이다. QQQ의 이름은 표시되고 SPY의 이름은 NULL이다. 같은 SQL 전체를 다시 실행해도 같은 결과가 나온다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

### TEMP 테이블 방식과 비교하기

TEMP 테이블은 생성한 DB 연결에서만 사용할 수 있고 연결이 끝나면 사라진다. 아래 세 문장은 **같은 연결에서 CREATE → INSERT → SELECT 순서로** 실행해야 한다. SQL 편집기에서는 마지막 SELECT만 실행하지 말고 세 문장을 모두 선택해 스크립트로 실행한다. 같은 편집기라도 재접속하거나 실행마다 연결을 새로 여는 설정이면 TEMP 테이블이 유지되지 않을 수 있다.

```sql
CREATE TEMP TABLE day03_symbols (
    symbol text PRIMARY KEY, name text NOT NULL
);
INSERT INTO day03_symbols (symbol, name) VALUES ('QQQ', '가상 기술 ETF');
SELECT p.id, p.symbol, s.name, p.close_price
FROM public.raw_market_prices AS p
LEFT JOIN day03_symbols AS s ON p.symbol = s.symbol
ORDER BY p.id;
```

처음 생성한 연결에서는 CREATE·INSERT를 한 번 실행하고 이후에는 SELECT만 반복한다. 같은 연결에서 CREATE를 다시 실행하면 테이블이 이미 존재한다는 오류가, INSERT를 다시 실행하면 기본 키 중복 오류가 날 수 있다. 연결 상태와 무관하게 JOIN을 연습하려면 위의 CTE SQL 전체를 실행한다. CTE는 실제 TEMP 테이블을 만들거나 변경하지 않는다.

## 4장. 직접 해볼 실습 과제

1. LEFT JOIN을 INNER JOIN으로 바꾸고 5건이 3건으로 줄어드는 이유를 적는다.
2. CTE의 VALUES에 `('SPY', '가상 시장 ETF')` 행을 쉼표로 추가하고 LEFT JOIN 결과의 NULL 이름이 0건인지 확인한다. TEMP 방식이라면 같은 연결의 종목 표에 SPY를 INSERT한다.
3. 종목·가격 두 테이블을 그려 키와 연결 조건을 표시해 `day03/model.md`에 저장한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day03/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

`SQLSTATE 42P01: relation "day03_symbols" does not exist`는 현재 SQL에서 해당 이름을 찾을 수 없다는 뜻이다. TEMP 방식에서는 CREATE의 실행 성공 여부와 생성·조회에 사용한 연결이 같은지 확인한다. CTE 방식에서는 SELECT만 떼어 실행하지 말고 `WITH`부터 전체를 실행한다.

현재 연결과 테이블 상태는 다음으로 확인할 수 있다. TEMP 방식의 CREATE 이후 `visible_symbols`가 NULL이면 현재 연결에서 임시 테이블이 보이지 않는 상태다. CTE는 한 문장 안에서만 존재하므로 실행 후 여기에서 NULL이 나오는 것이 정상이다.

```sql
SELECT current_database(), pg_backend_pid(),
       to_regclass('pg_temp.day03_symbols') AS visible_symbols,
       to_regclass('public.raw_market_prices') AS raw_table;
```

`raw_table`이 NULL이면 Day 2의 테이블이 없는 DB에 연결했거나 초기화가 적용되지 않았는지 확인한다. 이때는 `day03_symbols`와 별개의 문제다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 가격이 없는 종목까지 보여주려면 JOIN의 왼쪽에 어떤 표를 두어야 할까?

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

[PostgreSQL 입문](https://www.postgresql.org/docs/17/tutorial.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 2](../day02/README.md) · [Day 4 →](../day04/README.md)
