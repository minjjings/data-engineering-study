# 실습 컬럼 기준과 단계별 매핑

각 단계의 입력·출력 이름과 타입을 아래 기준으로 연결한다. Day 1 파일과 Day 2 테이블은 처음부터 서로 다른 이름을 사용한다. 변환은 출력 쿼리나 새 파일에서 명시하며, 기존 원본 컬럼을 일괄 변경하는 방식으로 맞추지 않는다.

## 원본 기준

| 의미 | Day 1 JSON | Day 2 PostgreSQL `public.raw_market_prices` |
| --- | --- | --- |
| 종목 | `symbol`: 문자열 | `symbol`: varchar(20) |
| 거래일 | `date`: 날짜 문자열 | `trade_date`: date |
| 가격 | `close`: 문자열 또는 null | `close_price`: varchar(50), NULL 허용 |
| 수집 행 식별자 | 없음 | `id`: bigserial 기본 키 |
| 수집 시각 | 없음 | `collected_at`: timestamp, 기본값 CURRENT_TIMESTAMP |

- Day 1 `raw.json`은 4행, `clean.json`은 2행이다. 정제 파일도 `symbol`, `date`, `close`를 사용하며 가격은 문자열이다.
- Day 2 초기화 SQL은 `N/A` 가격 1행을 추가한 5행이다. Day 1 JSON을 자동 적재한 결과가 아니라 별도 SQL 샘플이다.
- Day 1 도입부의 `volume`은 API 설명용이다. 실제 Python 실습과 Day 2 테이블에는 없다.

## 정제 SQL과 dbt

| 단계 | 출력 컬럼 | 입력과의 차이 |
| --- | --- | --- |
| [Day 5](./day05/README.md) 정제 SELECT | `symbol`, `trade_date`, `close_price` | CTE의 숫자형 `price`를 최종 SELECT에서 `close_price`로 명명 |
| [Day 10](./day10/README.md) `public.clean_market_prices` view | `symbol`, `trade_date`, `close_price` | Day 5 SELECT를 view로 정의; 가격은 numeric |
| [Day 33](./day33/README.md) `stg_prices` | `id`, `symbol`, `trade_date`, `collected_at`, `raw_close_price`, `close_price` | 원문은 `raw_close_price`, 변환한 숫자는 `close_price` |
| [Day 34](./day34/README.md) `int_latest_prices` | `symbol`, `trade_date`, `close_price` | 정상 가격의 업무 키별 한 행; 수집 메타데이터는 최종 출력에서 제외 |
| [Day 35](./day35/README.md) `mart_symbol_prices` | `symbol`, `observed_days`, `first_day`, `last_day`, `avg_close_price` | 종목 단위 집계 결과로 별도 출력 컬럼 생성 |
| [Day 41](./day41/README.md) `fct_prices_incremental` | `symbol`, `trade_date`, `close_price` | 같은 이름의 seed 컬럼을 date·numeric으로 변환 |

[Day 96 데이터 계약](./day96/README.md)은 Day 10 view의 세 컬럼을 검사한다. 이 view에는 `collected_at`이 없으므로 최신성은 **원천 `public.raw_market_prices.collected_at`**을 기준으로 검사한다.

## S3·Athena·Glue

| 단계 | 컬럼과 타입 | 매핑 위치 |
| --- | --- | --- |
| [Day 48](./day48/README.md) 새 JSON Lines | `symbol`, `trade_date`, `close_price`: 문자열, 가격 null 허용 | `row["date"]` → `trade_date`, `row["close"]` → `close_price` |
| [Day 51](./day51/README.md) Athena `market_lab.raw_prices` | 위 세 필드는 string, 파티션 `ingest_date`도 string | `ingest_date`는 S3 경로와 파티션 등록에서 제공 |
| [Day 57](./day57/README.md) Glue 정제 JSON Lines | `symbol`, `trade_date`, `close_price` | 검증·중복 제거 후에도 가격 문자열 유지 |

Day 48 파일에는 DB 전용 `id`, `collected_at`이 없다. Athena의 파티션 컬럼 `ingest_date`도 JSON 본문에 있다고 가정하지 않는다.

## Spark와 DW 적재

| 단계 | 컬럼과 타입 | 주의할 연결 |
| --- | --- | --- |
| Day 61~80의 자체 생성 입력 `df` | `symbol` string, `trade_date` string, `close_price` string, `source_id` long | Day 1 파일·Day 2 DB와 구분되는 별도 고정 샘플 |
| [Day 79](./day79/README.md) DW 적재용 Parquet | `symbol` string, `trade_date` date, `close_price` decimal(12,2) | 날짜·가격을 명시적으로 변환하고 `source_id` 제외 |
| [Day 58~59](./day59/README.md) `dw_lab.fact_price` | `symbol` text, `trade_date` date, `close_price` numeric(12,2) | 키는 `(symbol, trade_date)`; 종목·날짜 차원을 먼저 적재 |

`source_id`는 Spark 실습에서 생성한 입력 순번이다. DB가 생성한 `raw_market_prices.id`와 같은 값이라고 가정하지 않는다. 두 값을 연결하려면 별도의 원천 식별 규칙이 필요하다.

Day 58의 TEMP 테이블은 같은 psql 연결에서만 사용할 수 있다. Day 59의 영구 DW 과제는 동일한 컬럼 정의로 `dw_lab` 스키마에 별도로 작성한다.

## 이벤트·CDC·운영 메타데이터

- [Day 82](./day82/README.md) Kafka 이벤트: `event_id`, `symbol`, `trade_date`, `close_price`, `event_time`. Day 87에서는 `event_time` 문자열을 timestamp로 파싱한다.
- [Day 91](./day91/README.md) CDC 전용 DB의 `public.prices`: `id` integer, `symbol` text, `price` numeric. 이 별도 예제는 의도적으로 `price`를 사용한다. Day 93의 변경 SQL과 Day 94의 `cdc_target`도 이 구조에 맞춘다.
- [Day 102](./day102/README.md) `ops_lab.pipeline_runs`: `run_id`, `batch_id`, `started_at`, `ended_at`, `status`, `input_rows`, `output_rows`, `source_max_collected_at`. Day 103~104의 대시보드 SQL은 이 표를 읽는다.

`event_id`·`source_id`·DB의 `id`는 서로 다른 식별자다. `event_time`·`trade_date`·`collected_at`도 각각 사건 시각·거래일·수집 시각을 뜻한다.

## 임시 별칭과 저장 컬럼 구분하기

Day 8의 `parsed.price`, Day 14의 별도 `lab_upsert.price`, Day 63의 `price`, Day 97의 CTE `prices.price`는 각각 해당 예제에서 직접 선언한 값이다. `raw_market_prices`에 `price`라는 원본 컬럼이 있다는 뜻이 아니다.

검사할 때는 같은 글자를 일괄 치환하지 말고 아래 순서로 확인한다.

1. `FROM`·`source`·`ref`·파일 경로로 실제 입력을 찾는다.
2. DDL·JSON 키·DataFrame 스키마에 참조할 컬럼이 있는지 확인한다.
3. `AS`·`alias`·딕셔너리 매핑으로 출력 이름이 어떻게 바뀌는지 확인한다.
4. 다음 단계가 그 출력 이름과 타입을 사용하는지 비교한다.

[전체 학습 계획으로 돌아가기](./README.md)
