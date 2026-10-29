# 데이터 엔지니어링 독학 기록

Python·SQL 기초부터 AWS 배치 파이프라인, Spark, Kafka·CDC, 운영 자동화까지 연결하는 **24주 독학 로드맵**입니다. 기존 Day 1·Day 2 실습의 시장 가격 예제를 단계적으로 확장해, 마지막에는 재실행과 장애 복구가 가능한 데이터 파이프라인을 만듭니다. 예제 가격과 거래량은 학습용 가상 데이터입니다.

**학습 기준: 주 5일, 하루 90~120분** · 주 7.5~10시간 · 전체 약 180~240시간

> 이 문서는 학습 계획입니다. 파일이 있거나 수업을 진행했다는 사실만으로 완료 처리하지 않습니다. 현재 진도는 확인되지 않았으며 모든 체크박스를 미완료로 시작합니다. SQL·코드·실행 결과·개념 설명을 직접 확인한 뒤 해당 항목을 체크합니다. Day 2의 SQL과 개념 설명도 제출·검토 전까지 미확인 상태입니다.

## 목차

- [학습 방식과 완료 기준](#learning-guide)
- [기존 교재와 저장소 구성](#repository)
- [로컬 Docker 실습 시작하기](#local-start)
- [24주 학습 목차](#roadmap)
  - [1~3주: 데이터 엔지니어링 기초와 SQL](#phase-1)
  - [4~6주: Python·PostgreSQL·Airflow](#phase-2)
  - [7~9주: dbt](#phase-3)
  - [10~12주: AWS S3·Athena·Glue·DW](#phase-4)
  - [13~16주: PySpark·Parquet](#phase-5)
  - [17~19주: Kafka·CDC](#phase-6)
  - [20~22주: 데이터 품질·모니터링·CI/CD](#phase-7)
  - [23~24주: 통합 프로젝트](#phase-8)
- [학습 기록과 리뷰 양식](#study-log)
- [공식 문서](#references)

<a id="learning-guide"></a>
## 학습 방식과 완료 기준

개념과 실습을 함께 진행합니다. 각 주는 아래 5일 흐름을 기본으로 삼고, 막힌 내용이 있으면 다음 주로 넘어가기 전에 보완합니다. 주차는 권장 순서이며 달력상의 날짜나 알림 횟수가 완료 여부를 결정하지 않습니다.

| 요일 대신 사용할 학습일 | 할 일 |
| --- | --- |
| Day 1 | 핵심 개념 정리, 작은 예제 실행, 이번 주 목표 설정 |
| Day 2 | 기본 실습 구현 및 입력·출력 확인 |
| Day 3 | 예외 데이터와 실패 상황을 넣어 실습 확장 |
| Day 4 | 재실행·복구 확인, 검증 쿼리 또는 필요한 테스트 작성 |
| Day 5 | 산출물 정리, 개념 설명, 리뷰와 부족한 부분 보완 |

하루 시간은 **개념 20분 + 실습 55~80분 + 결과 정리 15~20분 = 90~120분**으로 나눕니다. 초과하는 선택 과제는 다음 학습일로 넘깁니다.

각 주의 체크박스는 다음 기준으로 확인합니다.

- 핵심 주제: 용어를 외우는 데서 그치지 않고, 이 예제에서 왜 필요한지 자기 말로 설명한다.
- 실습: 직접 실행하고 정상 입력·오류 입력·재실행 결과를 확인한다.
- 산출물: 코드와 함께 실행 방법, 예상·실제 결과, 처리 기준과 남은 문제를 기록한다.

도구는 배우는 주차에 순서대로 추가합니다. 로컬 실습은 PostgreSQL부터 시작하며, Airflow·dbt·Spark·Kafka 환경은 해당 주차에 구성합니다. 버전과 의존성은 추가할 때 기록합니다.

<a id="repository"></a>
## 기존 교재와 저장소 구성

기존 교재, 코드, 샘플 데이터와 Docker 설정을 유지하고 이 README를 전체 학습의 입구로 사용합니다.

| 기존 자료 | 내용 | 로드맵 연결 |
| --- | --- | --- |
| [Day 1 교재](./day01/README.md) | 데이터 파이프라인, ETL·ELT, Raw·정제 데이터 | 1주 |
| [Day 1 Python 코드](./day01/pipeline.py) | JSON 저장, 가격 검증, 중복 제거 | 1주 → 4주 확장 |
| [Raw 샘플](./day01/data/raw.json) · [정제 샘플](./day01/data/clean.json) | 입력과 출력 비교 | 1주 |
| [Day 2 교재](./day02/README.md) | Docker·PostgreSQL, NULL·중복 검사, 윈도 함수 | 1~2주 |
| [초기화 SQL](./day02/init.sql) | `raw_market_prices` 생성, 샘플 5건 삽입 | 1~2주 |
| [Docker Compose 설정](./docker-compose.yml) | PostgreSQL 17, 데이터 볼륨, 상태 확인 | 로컬 실습 공통 |

```text
data-engineering-study/
├── README.md
├── docker-compose.yml
├── day01/
│   ├── README.md
│   ├── pipeline.py
│   └── data/
│       ├── raw.json
│       └── clean.json
└── day02/
    ├── README.md
    └── init.sql
```

아래 로드맵의 추가 산출물은 **앞으로 만들 파일**입니다. 예를 들어 `notes/week01.md`, `sql/week02/`, `src/`, `dags/`, `dbt/`, `spark/`, `streaming/`, `tests/`, `docs/`를 필요할 때 생성합니다. 기존 `day01/`, `day02/`는 그대로 연결해 사용합니다.

<a id="local-start"></a>
## 로컬 Docker 실습 시작하기

### 1. 준비와 저장소 이동

Git과 Docker Desktop을 설치하고 Docker Desktop을 실행합니다. Windows에서는 Linux 컨테이너 엔진이 준비된 것을 확인합니다. Day 1 Python 실습에는 별도로 Python 3이 필요합니다.

처음 내려받는 경우 PowerShell에서 실행합니다.

```powershell
git clone https://github.com/minjjings/data-engineering-study.git
Set-Location .\data-engineering-study
```

이미 내려받았다면 기존 프로젝트 폴더로 이동합니다. 이후 명령은 `docker-compose.yml`이 있는 저장소 최상위에서 실행합니다.

```powershell
docker version
docker compose version
docker compose config --quiet
```

`docker version`에서 서버 연결 오류가 나면 Docker Desktop의 엔진 시작 상태부터 확인합니다. `config --quiet`는 설정 문법 확인이며 실제 데이터베이스 실행 확인은 다음 단계에서 합니다.

### 2. PostgreSQL 실행과 접속

```powershell
docker compose up -d
docker compose ps
```

`postgres`가 `healthy`가 될 때까지 기다립니다. 시작에 실패하면 로그를 확인합니다.

```powershell
docker compose logs postgres
```

최초의 빈 데이터 볼륨에서는 `day02/init.sql`이 자동 실행되어 테이블과 샘플 5건을 만듭니다. **기존 볼륨에서는 초기화 SQL이 자동으로 다시 실행되지 않습니다.** 파일을 수정하거나 컨테이너를 재시작한 것만으로 적용되지는 않습니다. [PostgreSQL 이미지 초기화 안내](https://hub.docker.com/_/postgres)

```powershell
docker exec -it de-postgres psql -U de_user -d market_db
```

접속 후 아래 명령을 `psql` 화면에서 실행합니다.

```sql
\dt
SELECT COUNT(*) AS total_count FROM raw_market_prices;
SELECT * FROM raw_market_prices ORDER BY id;
```

새로 초기화한 상태의 예상 건수는 **5건**입니다. `healthy`여도 테이블과 데이터는 따로 확인합니다. 기존 볼륨의 데이터나 INSERT 재실행에 따라 건수가 달라질 수 있습니다. 종료는 `\q`입니다.

| 외부 DB 도구 연결 항목 | 설정값 |
| --- | --- |
| Host / Port | `127.0.0.1` / `5433` |
| Database / User | `market_db` / `de_user` |
| Password | `de_password` · 로컬 실습용 |
| 컨테이너 이름 / 내부 포트 | `de-postgres` / `5432` |

실제 비밀번호나 AWS 자격 증명은 저장소에 올리지 않습니다. 호스트의 5433 포트가 이미 사용 중이면 Compose 파일의 `127.0.0.1:5433:5432`에서 왼쪽 포트를 바꾸고, 외부 DB 도구에도 같은 값을 사용합니다.

### 3. 테이블이 없거나 초기화가 안 된 경우

먼저 로그를 확인하고, `psql`에서 테이블 존재 여부를 조회합니다.

```sql
SELECT to_regclass('public.raw_market_prices');
```

반환값이 NULL이고 초기화가 적용되지 않은 것을 확인한 경우에만, `\q`로 나온 후 PowerShell에서 다음을 실행합니다.

```powershell
docker cp .\day02\init.sql de-postgres:/tmp/init.sql
docker exec -it de-postgres psql -v ON_ERROR_STOP=1 -U de_user -d market_db -f /tmp/init.sql
```

다시 접속해 건수를 확인합니다. **테이블이 이미 있다면 이 파일 전체를 다시 실행하지 않습니다.** `CREATE TABLE IF NOT EXISTS`는 테이블 재생성만 막으며 뒤의 INSERT 중복 삽입을 막지 않습니다. PowerShell에서 `< day02/init.sql` 형태의 입력 리다이렉션 대신 위의 복사와 `-f` 방식을 사용합니다.

### 4. 실습 종료와 재시작

`psql`에서 `\q`로 나온 뒤 실행합니다.

```powershell
# 컨테이너 종료 및 제거, 이름 있는 데이터 볼륨 유지
docker compose down

# 다음 학습일에 재시작
docker compose up -d
```

`docker compose down -v`는 데이터 볼륨을 삭제하므로 일반 종료에 사용하지 않습니다. [Docker Compose 종료 안내](https://docs.docker.com/reference/cli/docker/compose/down/)

<a id="roadmap"></a>
## 24주 학습 목차

각 주의 세 항목을 따로 확인합니다. 아래는 계획한 산출물이며, 체크되지 않은 항목은 미완료 또는 미확인입니다.

<a id="phase-1"></a>
### 1~3주: 데이터 엔지니어링 기초와 SQL

#### 1주 — 파이프라인의 역할과 SQL 입문

- [ ] **핵심 주제:** ETL·ELT, Raw·정제 데이터, 데이터 품질, Docker·PostgreSQL, SELECT·WHERE·NULL을 설명한다.
- [ ] **실습:** 기존 Day 1을 실행해 입력·출력을 비교하고, Day 2 환경에서 테이블·샘플 5건을 확인한 뒤 NULL과 중복을 조회한다.
- [ ] **산출물:** 기존 실습 실행 기록과 `notes/week01.md`에 ETL·ELT 비교, 데이터 처리 흐름, SQL 결과와 남은 질문을 정리한다.

#### 2주 — 집계·JOIN·윈도 함수와 정제 SQL

- [ ] **핵심 주제:** GROUP BY·HAVING, INNER·LEFT JOIN, CTE, ROW_NUMBER, 자료형 변환과 안전한 가격 검증을 설명한다.
- [ ] **실습:** Day 2의 중복·최신 행 조회를 직접 작성하고, 종목 기준 테이블을 만들어 JOIN한다. NULL·N/A·0·음수와 수집 시각 동률을 넣어 정제 기준을 비교한다.
- [ ] **산출물:** `sql/week02/`에 조회·정제 SQL, 입력별 예상·실제 건수, WHERE와 HAVING 및 최신 행 선택 기준의 차이를 기록한다.

#### 3주 — 데이터 모델링·트랜잭션·증분 적재 기초

- [ ] **핵심 주제:** PK·FK·UNIQUE, 정규화, 트랜잭션, 인덱스와 실행 계획, Watermark·멱등성의 의미를 설명한다.
- [ ] **실습:** 종목·가격 테이블을 설계하고 종목·거래일의 유일성 기준을 정한다. UPSERT와 Watermark를 이용한 작은 증분 적재를 같은 입력으로 두 번 실행한다.
- [ ] **산출물:** ERD, DDL·증분 SQL, 재실행 전후 건수와 실행 계획 비교, 지연 도착 데이터 및 Watermark 갱신 시점에 대한 메모를 남긴다.

<a id="phase-2"></a>
### 4~6주: Python·PostgreSQL·Airflow

#### 4주 — Python 수집 코드 구조화

- [ ] **핵심 주제:** 함수·모듈, CSV·JSON, HTTP 요청, 예외 처리, 로깅, 설정 분리와 단위 테스트를 이해한다.
- [ ] **실습:** Day 1 코드를 수집·검증·저장 함수로 나누고 파일 입력과 선택적인 공개 API 입력을 지원한다. 타임아웃·재시도 한도를 정하고 잘못된 행은 사유와 함께 분리한다.
- [ ] **산출물:** `src/`의 실행 가능한 수집 코드, 의존성 목록, 비밀값 없는 설정 예시, 유효·무효 입력 테스트와 실행 안내를 만든다.

#### 5주 — Python에서 PostgreSQL로 안정적으로 적재

- [ ] **핵심 주제:** DB 연결, 매개변수 바인딩, 배치 적재, 커밋·롤백, UPSERT, 증분 상태 관리를 설명한다.
- [ ] **실습:** Python으로 Raw와 정제 데이터를 적재하고 날짜 구간을 인자로 받는다. 적재 실패 시 롤백하고, 성공한 뒤 Watermark를 갱신하며 동일 구간 재실행을 확인한다.
- [ ] **산출물:** 적재 코드·스키마, 정상·실패·재실행 검증 결과, Raw 수집 이력과 정제 테이블의 중복 정책을 정리한다.

#### 6주 — Airflow로 배치 파이프라인 예약 실행

- [ ] **핵심 주제:** DAG·Task·의존성, 실행 구간, 스케줄, 재시도, catchup·backfill과 로그를 이해한다.
- [ ] **실습:** 로컬 Airflow 환경을 추가하고 수집 → 적재 → 검증 DAG를 만든다. 처리 날짜를 전달하고 일부 작업을 의도적으로 실패시킨 뒤 재시도·과거 구간 재처리를 확인한다.
- [ ] **산출물:** `dags/`의 DAG, Airflow 환경 실행 안내와 버전, 성공·실패 로그, 특정 날짜를 재처리하는 절차를 남긴다.

<a id="phase-3"></a>
### 7~9주: dbt

#### 7주 — dbt 프로젝트와 계층별 SQL 모델

- [ ] **핵심 주제:** dbt의 변환 역할, source·ref, staging·intermediate·mart 계층과 모델 의존성을 설명한다.
- [ ] **실습:** PostgreSQL용 dbt 프로젝트를 만들고 Day 2 정제 SQL을 staging 모델로 옮긴다. 종목·일자별 분석 모델을 연결해 실행한다.
- [ ] **산출물:** `dbt/` 프로젝트, source 정의, 계층별 모델, 비밀값을 제외한 연결 설정 예시와 실행 기록을 만든다.

#### 8주 — dbt 테스트와 문서화

- [ ] **핵심 주제:** not_null·unique·relationships·accepted_values, 업무 규칙 테스트, 문서·lineage, source freshness의 의미를 이해한다.
- [ ] **실습:** 종목·거래일 복합 키의 유일성과 양수 가격을 검사하고 잘못된 데이터를 넣어 테스트 실패를 확인한다. 수집 시각 기준 freshness를 설정하고 모델·컬럼 설명을 작성한다.
- [ ] **산출물:** 테스트 SQL·YAML, 실패·수정 후 결과, 생성 문서와 모델 의존성 기록, 품질 규칙 목록을 남긴다.

#### 9주 — dbt 증분 모델과 Airflow 연결

- [ ] **핵심 주제:** incremental 모델, unique_key, full-refresh, 변경·지연 데이터 처리와 실행 순서를 설명한다.
- [ ] **실습:** 사용하는 어댑터가 지원하는 증분 전략을 선택해 변경 가격과 늦게 도착한 데이터를 반영한다. Airflow에서 적재 후 dbt 실행·테스트를 연결하고 동일 구간을 재실행한다.
- [ ] **산출물:** 증분 모델, Airflow 연동 DAG, 전체 재구축과 증분 결과 비교, 재처리 범위와 실패 시 복구 안내를 만든다.

<a id="phase-4"></a>
### 10~12주: AWS S3·Athena·Glue·DW

AWS 실습은 사용할 리전·권한·예산 알림을 먼저 정하고 작은 샘플로 수행합니다. 예산 알림은 자동 비용 차단을 보장하지 않습니다. 실습 뒤 실행 중인 작업과 남은 리소스를 확인하고 정리 내역을 기록합니다.

#### 10주 — S3 기반 데이터 레이크와 접근 권한

- [ ] **핵심 주제:** 객체·버킷·prefix, 날짜별 저장 구조, Raw·정제 영역, IAM 최소 권한과 수명 주기를 이해한다.
- [ ] **실습:** 버킷의 공개 접근을 차단하고 작은 Raw JSON·CSV를 날짜별로 업로드·다운로드한다. 로컬 결과와 비교하고 필요한 읽기·쓰기 권한만 부여한다.
- [ ] **산출물:** S3 경로 설계, 업로드 코드·명령, 비밀값 없는 권한 설정 기록, 예산 확인과 리소스 정리 절차를 남긴다.

#### 11주 — Glue Data Catalog와 Athena SQL

- [ ] **핵심 주제:** 메타데이터 카탈로그, 크롤러와 명시적 스키마, 외부 테이블, 파티션과 스캔량을 설명한다.
- [ ] **실습:** S3 샘플의 스키마를 Glue Data Catalog에 등록하고 Athena로 조회한다. 날짜 파티션 조건 유무에 따른 결과와 스캔량을 비교하고 쿼리 결과 저장 위치를 정한다.
- [ ] **산출물:** 테이블·파티션 정의, Athena SQL, 건수 검증과 스캔량 비교, 스키마 변경 시 확인할 항목을 정리한다.

#### 12주 — Glue ETL과 데이터 웨어하우스 모델링

- [ ] **핵심 주제:** Glue ETL 작업, 데이터 레이크와 DW의 역할, 팩트·차원과 스타 스키마를 이해한다. Spark 코드는 13~16주에 확장한다.
- [ ] **실습:** 작은 샘플로 Glue 변환 작업 1개를 실행해 결과를 검증한다. PostgreSQL에 가격 팩트·종목·날짜 차원과 분석 마트를 만들고 Redshift의 역할을 비교한다. Redshift 생성은 선택 과제로 둔다.
- [ ] **산출물:** Glue 작업과 실행 기록, DW ERD·DDL·집계 SQL, 원천 대비 건수 검증, 비용 확인 및 작업·리소스 정리 기록을 남긴다.

<a id="phase-5"></a>
### 13~16주: PySpark·Parquet

#### 13주 — PySpark DataFrame과 명시적 스키마

- [ ] **핵심 주제:** Spark의 분산 처리 개념, Driver·Executor, 지연 실행, transformation·action과 스키마를 설명한다.
- [ ] **실습:** 버전을 기록한 로컬 PySpark 환경을 만들고 JSON·CSV를 명시적 스키마로 읽는다. 필터·형 변환·NULL 처리·집계를 구현한다.
- [ ] **산출물:** `spark/`의 실행 스크립트, 환경과 실행 안내, 스키마 및 SQL 결과와의 건수·집계 비교를 남긴다.

#### 14주 — JOIN·윈도 함수와 대규모 정제

- [ ] **핵심 주제:** Spark SQL, JOIN, 윈도 함수, shuffle, 결정적인 중복 선택 기준을 이해한다.
- [ ] **실습:** 데이터 규모를 늘린 가상 샘플을 생성하고 종목 JOIN·가격 검증·최신 행 선택을 구현한다. 시각 동률·잘못된 가격 등 동일 입력으로 PostgreSQL 결과와 비교한다.
- [ ] **산출물:** Spark 정제 작업, 샘플 생성 코드, 검증 쿼리와 SQL·Spark 결과 비교표를 만든다.

#### 15주 — Parquet·파티셔닝·파일 크기

- [ ] **핵심 주제:** 컬럼 기반 저장, 압축, 파티션 가지치기, small files 문제와 스키마 변경의 영향을 설명한다.
- [ ] **실습:** 같은 데이터를 CSV와 Parquet으로 저장하고 크기·조회 시간을 비교한다. 거래일별 Parquet을 만들고 선택 컬럼·기간 필터를 적용해 읽는다.
- [ ] **산출물:** Parquet 변환 작업, 디렉터리 구조, 크기·파일 수·실행 조건을 포함한 비교 기록, 파티션 설계 근거를 남긴다.

#### 16주 — Spark 실행 계획과 배치 파이프라인 연결

- [ ] **핵심 주제:** 실행 계획·Spark UI, 파티션 수, repartition·coalesce, cache·broadcast의 적용 조건을 이해한다.
- [ ] **실습:** 같은 입력에서 병목 한 가지를 찾아 변경 전후를 비교한다. Airflow에서 Spark 작업과 검증을 실행하고 날짜별 출력의 안전한 재처리를 확인한다.
- [ ] **산출물:** 개선 전후 측정 기록, 연결 DAG, 재실행 검증과 파티션 복구 절차를 정리한다. 로컬 측정의 한계도 기록한다.

<a id="phase-6"></a>
### 17~19주: Kafka·CDC

#### 17주 — Kafka 메시지 흐름과 기본 클라이언트

- [ ] **핵심 주제:** 브로커·토픽·파티션, key·offset, producer·consumer·consumer group과 파티션 내 순서를 설명한다.
- [ ] **실습:** 로컬 Kafka 환경을 추가하고 가상 가격 이벤트를 발행·소비한다. 종목을 key로 사용하고 소비자를 중지·재시작해 offset과 그룹 동작을 확인한다.
- [ ] **산출물:** `streaming/`의 발행·소비 코드, 실행 환경과 버전, 이벤트 스키마, offset·순서 관찰 기록을 만든다.

#### 18주 — 이벤트 처리·중복·재처리

- [ ] **핵심 주제:** at-least-once 전달, event time·처리 시각, 지연·중복 이벤트, 체크포인트와 처리 보장 범위를 이해한다.
- [ ] **실습:** Kafka 입력을 Spark Structured Streaming으로 읽고 체크포인트를 사용하는 작은 집계를 만든다. event_id와 event_time을 정의하고 중복·지연 이벤트 및 재시작 결과를 비교한다.
- [ ] **산출물:** 스트리밍 작업, 체크포인트 설정, 중복 제거·지연 허용 기준, 재시작 전후 결과와 출력 저장 방식의 제약을 남긴다.

#### 19주 — PostgreSQL CDC와 Debezium

- [ ] **핵심 주제:** WAL·논리 복제, CDC, snapshot과 변경 이벤트, INSERT·UPDATE·DELETE 전달을 설명한다.
- [ ] **실습:** CDC용 PostgreSQL 설정과 Debezium·Kafka Connect를 추가한다. 작은 테이블을 초기 동기화한 뒤 추가·수정·삭제를 전달하고 대상 테이블에 반영한다.
- [ ] **산출물:** 비밀값 없는 커넥터 설정, 변경 이벤트 예시, 최종 상태 일치 검증, 재시작·중복 처리 및 복제 슬롯 관리 절차를 정리한다.

<a id="phase-7"></a>
### 20~22주: 데이터 품질·모니터링·CI/CD

#### 20주 — 데이터 품질 규칙과 실패 처리

- [ ] **핵심 주제:** 완전성·유일성·유효성·참조 무결성·최신성, 데이터 계약, 격리와 작업 중단 기준을 설명한다.
- [ ] **실습:** dbt 테스트와 Python·SQL 검증을 정리해 배치 경계에 배치한다. NULL·중복·스키마 변경·갱신 지연을 주입하고 실패 감지 및 잘못된 데이터 격리를 확인한다.
- [ ] **산출물:** 품질 규칙표, 검증 코드, 실패 사례와 복구 기록, 품질 검사를 통과한 뒤 공개하는 기준을 남긴다.

#### 21주 — 로그·지표·모니터링과 장애 대응

- [ ] **핵심 주제:** 처리 건수·실패율·소요 시간·데이터 최신성·consumer lag, 알림 기준과 운영 절차를 이해한다.
- [ ] **실습:** 한 가지 방식으로 지표를 수집해 Grafana 등에서 확인하고 정상 기준선을 기록한다. 배치 실패 또는 Kafka 적체를 재현해 경고와 복구 확인을 연습한다.
- [ ] **산출물:** 대시보드 설정·화면, 지표 정의, 경고 기준, 원인 확인 → 재처리 → 데이터 검증 순서의 장애 대응 문서를 만든다.

#### 22주 — 테스트·CI/CD와 재현 가능한 환경

- [ ] **핵심 주제:** 코드 검사·단위 테스트·통합 테스트, CI와 CD의 차이, 의존성 고정, 비밀정보 주입을 이해한다.
- [ ] **실습:** GitHub Actions에서 코드 검사와 핵심 테스트·dbt 검증을 실행한다. PR 검증을 통과한 버전의 배포 패키지를 만들고 로컬 또는 분리된 실습 환경에 적용·복구한다.
- [ ] **산출물:** `.github/workflows/` 설정, 필요한 테스트, CI 성공·실패 기록, 배포·되돌리기 절차와 새 환경 재현 안내를 남긴다.

<a id="phase-8"></a>
### 23~24주: 통합 프로젝트

#### 23주 — 최소 배치 경로 완성 및 스트리밍 확장

- [ ] **핵심 주제:** 요구사항·분석 질문, 도구별 책임, 데이터 계보, 처리 주기와 복구 목표를 정한다.
- [ ] **실습:** 가상 시장 데이터를 대상으로 수집 → S3 Raw → Spark 정제·Parquet → PostgreSQL DW → dbt 마트 → 품질 검사 경로를 연결하고 Airflow로 실행한다. Athena로 S3 결과를 교차 확인한다. 배치가 검증되면 PostgreSQL 변경 → Debezium·Kafka → 별도 대상 테이블 경로를 추가한다.
- [ ] **산출물:** 아키텍처 그림, 실행 가능한 최소 배치 경로, 테이블·이벤트 명세, Glue 카탈로그 연결, 구현 범위와 남은 항목을 정리한다.

#### 24주 — 검증·복구·문서화와 최종 리뷰

- [ ] **핵심 주제:** 재현성·멱등성·정합성, 운영과 비용의 균형, 포트폴리오 설명 방법을 정리한다.
- [ ] **실습:** 정상 실행·같은 구간 재실행·과거 데이터 재처리·잘못된 입력·작업 중단 후 복구를 검증한다. 스트리밍을 구현했다면 INSERT·UPDATE·DELETE 최종 상태도 비교한다. 새 환경에서 실행 안내를 따라 재현한다.
- [ ] **산출물:** 프로젝트 실행 안내, 검증 결과표, CI 기록, 모니터링 화면, 장애 대응·AWS 리소스 정리 기록, 설계 선택과 한계를 설명하는 최종 회고를 완성한다.

최종 프로젝트에서는 **배치 경로를 필수 범위**로 삼고 스트리밍은 별도 검증 경로로 확장합니다. 모든 도구를 하나의 처리 단계에 억지로 넣지 않고, 예를 들어 Glue는 카탈로그·관리형 변환, Athena는 S3 조회, PostgreSQL은 로컬 DW, dbt는 DW 내부 SQL 변환의 역할을 맡깁니다. 12주의 Glue ETL과 로컬 Spark 작업을 비교한 기록도 최종 설계 근거로 활용합니다.

<a id="study-log"></a>
## 학습 기록과 리뷰 양식

매 학습일 기록은 `notes/weekXX/dayYY.md` 등에 남깁니다. 날짜·시도·완료·검토 결과를 구분하고, 오류가 있으면 재현에 필요한 입력과 메시지를 함께 보관합니다.

```text
주차 / 학습일 / 날짜:
오늘의 목표와 사용 시간:
직접 실행한 코드·SQL 경로:
입력과 예상 결과:
실제 결과·건수·로그:
처리 기준과 개념 설명:
오류 메시지·시도한 해결 방법:
같은 입력 재실행 결과:
완료를 확인한 항목과 근거:
미완료·미확인 항목:
다음 학습일에 보완할 내용:
```

리뷰를 요청할 때는 작성한 SQL·코드, 실행 결과, 자신의 개념 설명을 함께 공유합니다. **미제출 내용은 완료했다고 가정하지 않습니다.**

<a id="references"></a>
## 공식 문서

- [Docker Compose 실행](https://docs.docker.com/reference/cli/docker/compose/up/) · [종료와 볼륨 옵션](https://docs.docker.com/reference/cli/docker/compose/down/)
- [PostgreSQL Docker 이미지와 초기화](https://hub.docker.com/_/postgres)
- 개념과 상세 실습은 기존 [Day 1](./day01/README.md)·[Day 2](./day02/README.md) 교재의 공식 문서 링크를 함께 참고합니다.
