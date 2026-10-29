# Day 58. 팩트·차원과 grain

**12주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 57](../day57/README.md) · [Day 59 →](../day59/README.md)

이번 주에는 **Glue ETL과 데이터 웨어하우스** 내용을 다룬다. 오늘은 분석용 스타 스키마를 설계한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 분석용 스타 스키마를 설계한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

팩트는 가격 같은 관측값, 차원은 종목·날짜 같은 분석 축을 표현한다. 먼저 한 행이 무엇을 나타내는지 정한다. 종가는 여러 날짜를 단순 합산할 지표가 아니므로 허용할 집계도 설명한다.

## 2장. 실습 준비

S3·Catalog·로컬 PostgreSQL을 사용한다. Glue Python shell 작업을 작은 JSON Lines로 한 번 실행한다. 실습용 역할에 입력·스크립트 읽기, 출력 prefix 쓰기, 로그 권한을 부여한다. Python 런타임·타임아웃·실행 용량을 기록한다. Redshift는 역할 비교까지 필수이며 생성은 선택 과제다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 56](../day56/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
CREATE TEMP TABLE dim_symbol (symbol text PRIMARY KEY, category text);
CREATE TEMP TABLE dim_date (trade_date date PRIMARY KEY, year integer);
CREATE TEMP TABLE fact_price (
    symbol text REFERENCES dim_symbol,
    trade_date date REFERENCES dim_date,
    close_price numeric(12,2) NOT NULL CHECK (close_price > 0),
    PRIMARY KEY(symbol, trade_date)
);
```

**예상 결과와 확인 기준:** 빈 표 세 개가 만들어지고 가격 팩트의 단위는 종목×거래일이다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 종목·날짜 차원을 먼저 넣고 QQQ·SPY 가격을 적재한다.
2. 카테고리별 관측 건수와 종목별 평균 가격 SQL을 작성한다.
3. ERD에 키·grain·단위·집계 규칙을 명시한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day58/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 일중 가격도 넣으려면 팩트의 키와 grain을 어떻게 바꿀까?

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

[Glue Python shell](https://docs.aws.amazon.com/glue/latest/dg/add-job-python.html) · [DW 설계](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-tables-best-practices.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 57](../day57/README.md) · [Day 59 →](../day59/README.md)
