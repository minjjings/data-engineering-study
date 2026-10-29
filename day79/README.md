# Day 79. Spark 배치와 DW 적재 경계

**16주 차 · 주간 4일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 78](../day78/README.md) · [Day 80 →](../day80/README.md)

이번 주에는 **Spark 실행 계획·성능과 배치 연결** 내용을 다룬다. 오늘은 Spark 결과를 검증한 뒤 DB에 공개하는 경로를 만든다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- Spark 결과를 검증한 뒤 DB에 공개하는 경로를 만든다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

Spark JDBC append를 바로 목표 표에 쓰면 재시도 시 중복될 수 있고 여러 파티션의 DB 쓰기가 한 트랜잭션으로 묶이는 것도 아니다. 먼저 파일·staging으로 저장하고 검증 후 DB 트랜잭션 UPSERT로 공개하는 경계를 둔다.

## 2장. 실습 준비

Python 3.11·Java 17 이상과 별도 .venv-spark 환경에 pyspark==4.0.1을 설치한다. JAVA_HOME을 확인하고 실제 Python·Java·Spark 버전을 기록한다. Windows 파일 쓰기 환경이 어려우면 WSL2 Linux에 같은 버전으로 구성한다. Python 블록은 루트 기준 dayNN/practice.py로 저장해 Spark 환경의 Python으로 실행한다. 예제는 자체 생성한 정상 가격 4행이며 Day 1 Raw 4행과 내용이 다르다. 출력 경로는 해당 day 전용이며 overwrite를 원본 경로에 사용하지 않는다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 76](../day76/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.master("local[2]").appName("market-study").getOrCreate()
df = spark.createDataFrame([
    ("QQQ", "2026-10-26", "620.50", 1),
    ("SPY", "2026-10-26", "680.20", 2),
    ("QQQ", "2026-10-27", "621.00", 3),
    ("SPY", "2026-10-27", "682.00", 4),
], "symbol string, trade_date string, close_price string, source_id long")
clean = df.select("symbol", F.to_date("trade_date").alias("trade_date"),
    F.col("close_price").cast("decimal(12,2)").alias("close_price"))
clean.printSchema()
assert clean.count() == 4
assert clean.groupBy("symbol", "trade_date").count().where("count > 1").count() == 0
clean.write.mode("overwrite").parquet("day79/validated-batch")
print("validated batch ready")
spark.stop()
```

**예상 결과와 확인 기준:** 검증된 4행 Parquet가 만들어진다. 출력 컬럼은 `symbol`(string), `trade_date`(date), `close_price`(decimal(12,2))이며 Day 59의 DW 컬럼과 대응한다. 실습 입력의 `source_id`는 결과에 포함하지 않는다. 아직 DW에 적재된 것은 아니다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 작은 실습에서는 Python으로 4행을 읽고 Day 59의 `(symbol, trade_date, close_price)` UPSERT를 바인딩된 매개변수로 실행해 `dw_lab.fact_price`에 적재한다. `dw_lab.dim_symbol`과 `dw_lab.dim_date`의 종목·날짜 차원을 먼저 준비한다. Day 14의 별도 `lab_upsert.price` 컬럼과 혼용하지 않는다.
2. 대규모 확장용 JDBC staging 경로를 설계하고 드라이버 버전·DB 동시 연결 수를 정한다.
3. 파일 저장 성공·DB 실패에서 같은 배치를 재적재해 4행 상태를 유지한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day79/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** Executor 수만큼 DB 연결을 무제한 늘리면 DB는 어떤 영향을 받을까?

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

[성능 튜닝](https://spark.apache.org/docs/4.0.1/sql-performance-tuning.html) · [JDBC](https://spark.apache.org/docs/4.0.1/sql-data-sources-jdbc.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 78](../day78/README.md) · [Day 80 →](../day80/README.md)
