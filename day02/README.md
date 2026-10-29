# Day 2. 데이터 저장 구조와 SQL 심화

<!-- curriculum-navigation -->
[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 1](../day01/README.md) · [Day 3 →](../day03/README.md)
<!-- /curriculum-navigation -->

**1주 차 · 두 번째 수업 | 약 100~120분**

[Day 1](../day01/README.md)에서는 Python으로 데이터를 정리했다. 오늘은 PostgreSQL에 데이터를 저장하고 **SQL로 빈 값과 중복을 찾는 방법**을 배운다. Docker로 PostgreSQL을 실행하므로 내 컴퓨터에 PostgreSQL을 직접 설치할 필요는 없다.

이 수업의 가격은 모두 학습용 가상 데이터이며 실제 시세가 아니다.

## 오늘의 학습 목표

- 원본 보관용 테이블과 분석용 테이블을 나누는 이유를 설명한다.
- Raw → Staging → Data Mart의 역할을 구분한다.
- Docker로 PostgreSQL을 실행하고 접속한다.
- `IS NULL`, `GROUP BY`, `HAVING`으로 데이터 상태를 확인한다.
- `ROW_NUMBER()`로 같은 종목·날짜의 데이터에 순위를 붙인다.
- 가격이 정상인 데이터를 고르는 SQL을 직접 작성한다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1장 | 저장 단계를 나누는 이유 이해하기 | 15분 |
| 2장 | Docker로 PostgreSQL 준비하기 | 20~30분 |
| 3장 | 테이블과 샘플 데이터 살펴보기 | 15분 |
| 4장 | SQL로 NULL과 중복 확인하기 | 15분 |
| 5장 | 윈도 함수로 최신 데이터 고르기 | 20분 |
| 6장 | 직접 SQL 작성하고 답변 정리하기 | 15~25분 |

## 1장. 왜 원본 테이블과 분석용 테이블을 나눌까?

### Raw → Staging → Data Mart

테이블은 데이터베이스 안에서 데이터를 행과 열로 보관하는 표다. 모든 목적을 하나의 표로 해결하기보다, 데이터가 준비된 정도와 사용하는 목적에 따라 나눌 수 있다.

```text
API에서 받은 데이터
    → Raw: 받은 값을 보관
    → Staging: 형식과 기본 품질을 정리
    → Data Mart: 분석할 목적에 맞게 가공
```

| 단계 | 쉬운 설명 | 가격 데이터 예시 |
| --- | --- | --- |
| Raw | 처음 받은 내용을 확인하는 곳 | 중복, 빈 가격, `"N/A"` 같은 값도 보관 |
| Staging | 사용할 수 있게 기본 정리를 하는 곳 | 가격을 숫자로 변환하고, 중복과 잘못된 값 처리 |
| Data Mart | 분석에 필요한 결과를 모아두는 곳 | 일별 가격, 수익률, 거래량 통계 |

오늘은 Raw 테이블을 만들고 정제용 조회 SQL을 작성한다. Staging과 Data Mart 테이블을 모두 만드는 것은 이후 수업에서 이어간다.

### 원본을 남기면 다시 처리할 수 있다

가격을 정리하는 코드에 실수가 있었다고 생각해보자.

- 원본이 없으면 API를 다시 호출해야 할 수 있다. 과거 데이터를 다시 받지 못할 수도 있다.
- 원본이 있으면 정리 규칙을 고친 뒤 같은 데이터로 다시 작업할 수 있다.

이처럼 보관한 데이터에 처리 과정을 다시 적용하는 것을 **재처리(Reprocessing)**라고 한다. 원본을 다시 흘려보낸다는 의미로 **Replay**라는 표현도 쓴다.

**생각해보기:** 잘못된 데이터를 Raw 테이블에서 바로 삭제하면, 나중에 오류 원인을 확인할 때 무엇이 어려워질까?

## 2장. Docker로 PostgreSQL 준비하기

### Docker와 Docker Compose는 무엇일까?

Docker는 프로그램을 실행하는 데 필요한 환경을 **컨테이너**로 묶어 실행하는 도구다. 오늘은 PostgreSQL이 준비된 이미지를 사용한다. 이미지는 컨테이너를 만들 때 사용하는 실행 환경의 바탕이다.

Docker Compose는 실행할 컨테이너와 설정을 YAML 파일에 적어두고 명령어로 관리하는 도구다. 오늘은 PostgreSQL 하나만 실행한다.

시작 전 Docker Desktop을 설치하고 실행해둔다. 이 문서의 터미널 명령은 모두 **프로젝트 최상위 폴더**에서 실행한다.

### Step 1. 파일 위치 확인하기

이 프로젝트에는 아래 설정 파일이 이미 준비되어 있다. 처음부터 따라 한다면 같은 위치에 파일을 만든다.

```text
 data-engineering-study/
 ├── docker-compose.yml
 ├── day01/
 │   ├── README.md
 │   ├── pipeline.py
 │   └── data/
 └── day02/
     ├── README.md
     └── init.sql
```

[docker-compose.yml](../docker-compose.yml)의 내용:

```yaml
services:
  postgres:
    image: postgres:17
    container_name: de-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: de_user
      POSTGRES_PASSWORD: de_password
      POSTGRES_DB: market_db
    ports:
      - "127.0.0.1:5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./day02/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U de_user -d market_db"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

| 설정 | 의미 |
| --- | --- |
| `postgres:17` | PostgreSQL 17 실행 환경 사용 |
| `container_name: de-postgres` | 컨테이너 이름을 `de-postgres`로 지정 |
| `restart: unless-stopped` | 직접 중지한 경우 등을 제외하고 자동 재시작 |
| `POSTGRES_USER` | 처음 만들 데이터베이스 사용자 |
| `POSTGRES_PASSWORD` | 해당 사용자의 비밀번호 |
| `POSTGRES_DB` | 처음 만들 데이터베이스 이름 |
| `127.0.0.1:5433:5432` | 내 컴퓨터의 5433번 포트를 컨테이너의 5432번 포트에 연결 |
| `postgres_data` | PostgreSQL 데이터를 계속 보관하는 Docker 볼륨 |
| `./day02/init.sql:...:ro` | 내 컴퓨터의 SQL 파일을 컨테이너에 읽기 전용으로 연결 |
| `healthcheck` | PostgreSQL이 연결을 받을 준비가 되었는지 확인 |

이미 내 컴퓨터의 5433번 포트를 사용 중이라면 `127.0.0.1:5434:5432`처럼 왼쪽 포트를 바꾼다. 컨테이너 안의 PostgreSQL 포트는 그대로 5432다.

여기서 `de_password`는 로컬 실습용 비밀번호다. 실제 서비스에서는 환경변수 파일이나 별도의 비밀정보 관리 방식을 사용하고, 실제 비밀번호를 저장소에 올리지 않는다.

### Step 2. 초기화 SQL 확인하기

[init.sql](./init.sql)은 테이블을 만들고 샘플 데이터 5건을 넣는 파일이다. 전체 내용과 설명은 다음 장에서 확인한다.

**최초 실행 시 자동으로 처리되므로, 실행 후 같은 INSERT를 다시 입력하지 않는다.** `CREATE TABLE IF NOT EXISTS`가 있어도 그 아래 `INSERT`는 다시 실행하면 데이터를 추가한다.

이 초기화 파일은 PostgreSQL 데이터 폴더가 비어 있는 최초 초기화 때만 자동 실행된다. 파일을 수정하고 컨테이너를 재시작해도 다시 실행되지 않는다. [PostgreSQL Docker 이미지 공식 안내](https://hub.docker.com/_/postgres)

### Step 3. PostgreSQL 실행하기

```powershell
# 컨테이너를 백그라운드에서 실행
docker compose up -d

# 상태 확인
docker compose ps
```

`postgres` 서비스에 `healthy`가 표시될 때까지 잠시 기다린다. 시작되지 않으면 다음 명령으로 오류 내용을 확인한다.

```powershell
docker compose logs postgres
```

`healthy`는 연결 준비 상태를 확인하는 것이며, 테이블과 샘플 데이터까지 정확한지는 접속 후 별도로 확인한다.

### Step 4. PostgreSQL에 접속하기

```powershell
docker exec -it de-postgres psql -U de_user -d market_db
```

접속하면 다음과 같은 입력 표시가 나온다.

```text
market_db=#
```

이제부터 SQL은 이 화면에 입력한다. SQL 끝에는 `;`를 붙인다. 입력 표시가 `market_db-#`로 바뀌면 문장이 아직 끝나지 않은 경우가 많으니 세미콜론과 따옴표를 확인한다.

나갈 때는 다음을 입력한다.

```text
\q
```

DBeaver 같은 도구를 사용한다면 다음 값으로 연결할 수도 있다.

| 항목 | 값 |
| --- | --- |
| Host | `127.0.0.1` |
| Port | `5433` · 앞에서 바꿨다면 변경한 포트 |
| Database | `market_db` |
| User | `de_user` |
| Password | `de_password` |

## 3장. 테이블과 샘플 데이터 살펴보기

### 원본 테이블 설계와 데이터 삽입

다음은 [init.sql](./init.sql)의 전체 내용이다. **Docker 최초 실행에서 이미 적용되었다면 읽고 확인만 한다.**

```sql
CREATE TABLE IF NOT EXISTS raw_market_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    trade_date DATE,
    close_price VARCHAR(50),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO raw_market_prices
    (symbol, trade_date, close_price)
VALUES
    ('QQQ', '2026-10-26', '620.50'),
    ('SPY', '2026-10-26', '680.20'),
    ('QQQ', '2026-10-26', '620.50'),
    ('SPY', '2026-10-27', NULL),
    ('QQQ', '2026-10-27', 'N/A');
```

### 각 열은 어떤 역할일까?

| 열 | 자료형 | 역할 |
| --- | --- | --- |
| `id` | `BIGSERIAL PRIMARY KEY` | 각 행을 구분하는 자동 증가 번호 |
| `symbol` | `VARCHAR(20)` | 최대 20글자의 종목 코드 |
| `trade_date` | `DATE` | 가격의 기준 날짜인 거래일 |
| `close_price` | `VARCHAR(50)` | 원본 가격을 최대 50글자의 문자열로 보관 |
| `collected_at` | `TIMESTAMP` | 수집 시각. 생략하면 현재 트랜잭션 시작 시각을 기본값으로 기록 |

`id`가 다르다고 서로 다른 가격 데이터인 것은 아니다. 오늘은 **종목과 거래일이 같으면 같은 대상의 데이터**로 본다.

### 왜 가격을 처음부터 숫자로 저장하지 않을까?

Raw에서는 `"620.50"`뿐 아니라 `"N/A"`처럼 숫자가 아닌 값도 일단 기록하려는 목적이 있다. 처음부터 숫자 자료형인 `NUMERIC`을 사용하면 `"N/A"`는 저장할 수 없다.

다만 이 테이블은 원본 응답을 완전히 그대로 보관하는 구조는 아니다. 날짜는 이미 `DATE` 형식이고, 문자열 길이에도 제한이 있다. 전체 응답을 남겨야 한다면 JSONB로 보관하거나 S3 같은 파일 저장소에 원본 파일을 함께 남길 수 있다. JSONB는 PostgreSQL에서 JSON 데이터를 저장하고 조회하는 자료형이다.

### 샘플 데이터 확인하기

```sql
SELECT *
FROM raw_market_prices
ORDER BY id;
```

처음 초기화한 상태라면 다음 5건이 나온다. 아래 표에서는 `collected_at`을 생략했다.

| id | symbol | trade_date | close_price |
| --- | --- | --- | --- |
| 1 | QQQ | 2026-10-26 | `620.50` |
| 2 | SPY | 2026-10-26 | `680.20` |
| 3 | QQQ | 2026-10-26 | `620.50` |
| 4 | SPY | 2026-10-27 | `NULL` |
| 5 | QQQ | 2026-10-27 | `N/A` |

`psql`은 기본적으로 NULL을 빈칸으로 보여준다. NULL이라는 글자가 보이지 않아도 값이 없는 행일 수 있다.

건수도 확인해보자.

```sql
SELECT COUNT(*) AS total_count
FROM raw_market_prices;
```

예상 값은 `5`다. 더 많다면 초기화 SQL이나 INSERT를 여러 번 실행했는지 확인한다. 이미 사용하던 볼륨이라면 이전 실습 데이터가 남아 있을 수도 있다.

## 4장. SQL로 데이터 품질 확인하기

### 4-1. 가격이 없는 행 찾기

```sql
SELECT *
FROM raw_market_prices
WHERE close_price IS NULL;
```

SPY의 2026년 10월 27일 데이터 1건이 나온다.

- `SELECT *`: 모든 열을 보여달라는 뜻이다.
- `FROM`: 조회할 테이블을 정한다.
- `WHERE`: 조건을 만족하는 행만 고른다.
- `IS NULL`: 값이 없는지 확인한다. NULL 검사에는 `= NULL`을 쓰지 않는다.

`'N/A'`는 값이 없는 것이 아니라 **N/A라는 글자가 들어 있는 상태**다. 따라서 `IS NULL`로는 찾을 수 없다. 빈 문자열 `''`도 NULL과 다르다.

### 4-2. 같은 종목과 날짜가 두 번 이상 있는지 확인하기

```sql
SELECT
    symbol,
    trade_date,
    COUNT(*) AS duplicate_count
FROM raw_market_prices
GROUP BY symbol, trade_date
HAVING COUNT(*) > 1;
```

예상 결과:

| symbol | trade_date | duplicate_count |
| --- | --- | --- |
| QQQ | 2026-10-26 | 2 |

순서대로 읽으면 다음과 같다.

1. `GROUP BY symbol, trade_date`: 종목과 날짜가 같은 행을 한 묶음으로 만든다.
2. `COUNT(*)`: 묶음마다 행이 몇 개인지 센다.
3. `HAVING COUNT(*) > 1`: 그중 2개 이상인 묶음만 보여준다.

`WHERE`는 묶기 전의 개별 행을 고르고, `HAVING`은 묶은 결과를 고른다고 생각하면 된다.

여기서 `duplicate_count = 2`는 그 묶음에 총 2행이 있다는 뜻이다. 하나만 남기려면 제외할 행은 1개다.

## 5장. 윈도 함수로 최신 데이터 고르기

### GROUP BY와 무엇이 다를까?

`GROUP BY`는 여러 행을 묶어서 묶음당 결과를 만든다. **윈도 함수는 각 행을 그대로 두고, 관련된 행들을 참고해 계산할 수 있다.** 오늘은 같은 종목·날짜 안에서 순번을 붙인다. [PostgreSQL 윈도 함수 공식 설명](https://www.postgresql.org/docs/17/tutorial-window.html)

### ROW_NUMBER()로 번호 붙이기

```sql
SELECT
    id,
    symbol,
    trade_date,
    close_price,
    ROW_NUMBER() OVER (
        PARTITION BY symbol, trade_date
        ORDER BY collected_at DESC, id DESC
    ) AS rn
FROM raw_market_prices
ORDER BY symbol, trade_date, rn;
```

| 부분 | 의미 |
| --- | --- |
| `PARTITION BY symbol, trade_date` | 같은 종목과 거래일끼리 나누어 번호를 붙임 |
| `ORDER BY collected_at DESC` | 수집 시각이 더 최근인 행부터 순서를 정함 |
| `id DESC` | 수집 시각이 같으면 ID가 큰 행을 먼저 놓음 |
| `ROW_NUMBER()` | 정해진 순서에 따라 1, 2, 3… 번호를 붙임 |
| `AS rn` | 번호를 보여주는 열의 이름을 `rn`으로 정함 |

윈도 함수 안의 `ORDER BY`는 번호를 붙이는 순서를 정한다. **화면에 나오는 순서는 바깥쪽 `ORDER BY`로 따로 정한다.**

새로 초기화한 샘플의 예상 결과는 다음과 같다.

| id | symbol | trade_date | close_price | rn |
| --- | --- | --- | --- | --- |
| 3 | QQQ | 2026-10-26 | 620.50 | 1 |
| 1 | QQQ | 2026-10-26 | 620.50 | 2 |
| 5 | QQQ | 2026-10-27 | N/A | 1 |
| 2 | SPY | 2026-10-26 | 680.20 | 1 |
| 4 | SPY | 2026-10-27 | NULL | 1 |

샘플 5건은 하나의 INSERT에서 들어가므로 기본 수집 시각이 같다. 그래서 같은 종목·날짜에서는 `id DESC`에 따라 3번 행이 1번 행보다 앞선다. `CURRENT_TIMESTAMP`는 실제로 행마다 새 시각을 만드는 함수가 아니라 현재 트랜잭션 시작 시각을 반환한다. [PostgreSQL 현재 시각 공식 설명](https://www.postgresql.org/docs/17/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT)

### rn = 1인 행만 선택하기

```sql
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY symbol, trade_date
            ORDER BY collected_at DESC, id DESC
        ) AS rn
    FROM raw_market_prices
)
SELECT *
FROM ranked
WHERE rn = 1
ORDER BY symbol, trade_date;
```

`WITH ranked AS (...)`는 괄호 안의 조회 결과에 `ranked`라는 이름을 붙여 다음 조회에서 쓰는 방법이다. 이런 표현을 **CTE**라고 한다. 실제 테이블을 새로 만드는 것은 아니다.

먼저 순번을 계산하고, 바깥 조회에서 `rn = 1`만 남긴다. 샘플에서는 총 4건이 나온다.

**최신 행을 골랐다고 정상 데이터만 남는 것은 아니다.** `N/A`와 NULL인 행도 각 종목·날짜의 유일한 행이어서 `rn = 1`이다. 최신 데이터가 가장 정확한 데이터인지도 별도로 판단해야 한다.

이 SELECT는 결과를 보여줄 뿐 Raw 테이블의 중복 행을 삭제하지 않는다. 같은 패턴은 나중에 dbt 모델에서도 사용할 수 있다.

## 6장. 오늘의 실습 과제

마지막 가격 정제 SQL은 직접 작성해보자. 정답 전체를 따라 쓰기보다 조건을 하나씩 추가하고 결과를 확인하는 것이 목표다.

### 가격이 정상인 데이터만 추출하기

오늘의 정상 가격은 **숫자로 바꿀 수 있고 0보다 큰 가격**으로 정한다. NULL과 `N/A`는 제외해야 한다.

힌트:

- `IS NOT NULL`만으로는 `N/A`를 제외할 수 없다.
- `CAST(close_price AS NUMERIC)`은 숫자로 바꿀 때 쓰지만, `N/A`에 바로 적용하면 오류가 난다.
- 문자열이 정한 숫자 모양인지 확인할 때 PostgreSQL의 정규식 연산자 `~`를 사용할 수 있다. 예를 들어 `'^[0-9]+([.][0-9]+)?$'`는 정수 또는 소수 모양인지 확인하는 학습용 규칙이다. 0도 통과하므로 양수 검사는 별도로 필요하다. 모든 숫자 표현을 허용하는 규칙은 아니다.
- `CASE WHEN ... THEN ... ELSE ... END`로 숫자 모양일 때만 변환하도록 나눠볼 수 있다. `WHERE`에 조건을 적은 순서대로 실행된다고 가정하고 위험한 변환을 넣지는 않는다.

정규식은 “글자가 특정한 모양인지 확인하는 규칙”이다. 자세한 문법은 [PostgreSQL 문자열 패턴 공식 문서](https://www.postgresql.org/docs/17/functions-matching.html)에서 확인할 수 있다.

결과를 확인할 기준:

| 조회 기준 | 샘플에서 나올 건수 |
| --- | --- |
| 원본 전체 | 5건 |
| NULL 가격 | 1건 |
| 중복 그룹 | 1개 그룹 · 그 안에 2행 |
| 종목·날짜별 최신 행 | 4건 · NULL과 N/A 포함 |
| 정상 가격만 선택 · 중복 유지 | 3건 |
| 정상 가격만 선택하고 종목·날짜별 하나만 남기기 | 2건 |

### Day 2 실습 체크리스트

- [ ] PostgreSQL에 `raw_market_prices` 테이블 생성
- [ ] 샘플 데이터 5건 삽입 · Docker 초기화로 자동 삽입했다면 조회로 확인
- [ ] NULL 값이 있는 데이터 조회
- [ ] 종목과 거래일 기준으로 중복된 데이터 찾기
- [ ] `ROW_NUMBER()`를 사용해 최신 행 조회
- [ ] 가격이 정상적인 데이터만 추출하는 SQL 작성

### 생각해볼 질문

1. `rn = 1`을 선택하면 중복 문제가 완전히 해결되는 걸까? 조회 결과와 원본 테이블을 나누어 생각해보자.
2. 같은 종목·날짜의 가격이 각각 620.50과 621.00이라면, 수집 시각이 최신이라는 이유만으로 올바른 가격이라고 할 수 있을까?
3. 최신 행의 가격이 NULL이고 이전 행의 가격이 정상이라면 어떻게 처리하고 싶은가? “최신 행을 고른 뒤 가격 검사”와 “정상 가격만 남긴 뒤 최신 행 선택”은 결과가 같을까?
4. Day 1의 “처음 통과한 데이터 선택”과 오늘의 “최신 수집 행 선택”은 어떤 차이가 있을까?

### 실습 내용 리뷰받기

아래 내용을 작성해 공유하면 SQL과 결과를 함께 검토할 수 있다. 막혔다면 오류 메시지를 그대로 남긴다.

```text
1. 내가 작성한 가격 정제 SQL:

2. 조회 결과와 건수:

3. 중복과 잘못된 가격을 처리한 기준:

4. rn = 1로 모든 문제가 해결되는지에 대한 내 생각:

5. 오류 메시지 또는 궁금한 점:
```

## 실습을 마칠 때와 다시 시작할 때

`psql`에서 `\q`로 나온 뒤 프로젝트 폴더의 터미널에서 실행한다.

```powershell
# 컨테이너 종료 및 제거 · 데이터 볼륨은 유지
docker compose down

# 다음에 다시 시작
docker compose up -d
```

`docker compose down`은 기본적으로 이름 있는 데이터 볼륨을 지우지 않는다. 반면 `docker compose down -v`는 이 프로젝트의 데이터 볼륨까지 제거할 수 있으므로, 데이터를 유지하려면 `-v`를 붙이지 않는다. [Docker Compose 종료 명령 공식 문서](https://docs.docker.com/reference/cli/docker/compose/down/)

`init.sql`을 수정했다고 기존 데이터베이스에 자동 반영되지는 않는다. 수정한 SQL은 필요한 부분만 별도로 적용하고, 데이터를 추가하는 INSERT를 무심코 다시 실행하지 않도록 한다.

## 앞으로의 수업과 연결하기

| 수업 | 이어서 배울 내용 |
| --- | --- |
| Day 3 | JOIN과 데이터 모델링 — 테이블을 어떻게 나누고 연결할까? |
| Day 4 | 증분 적재와 Watermark — 새 데이터만 가져오려면 어디까지 처리했는지 어떻게 기억할까? |
| Day 5 | 데이터 품질과 멱등성 — 같은 작업을 다시 실행해도 결과가 안전할까? |
| 7~9주 차 | 오늘의 SQL을 dbt 모델과 테스트로 옮기기 |

이후 프로젝트에서는 필요할 때 Docker Compose에 도구를 추가한다.

| 도구 | 배울 역할 |
| --- | --- |
| PostgreSQL | 데이터 저장 |
| Airflow | 작업 실행 시점과 순서 관리 |
| dbt | SQL 데이터 변환과 검사 |
| Kafka | 실시간 데이터 수집과 전달 |
| Spark | 대용량 데이터 처리 |
| Grafana | 상태를 보여주는 모니터링 화면 |

오늘은 PostgreSQL 하나로 충분하다. 중요한 것은 **SQL이 저장된 데이터의 상태를 확인하고, 사용할 데이터를 고르는 데 어떻게 쓰이는지** 이해하는 것이다.


