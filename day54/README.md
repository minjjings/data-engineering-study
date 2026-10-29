# Day 54. Athena 정제 건수와 스캔량 검증

**11주 차 · 주간 4일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 53](../day53/README.md) · [Day 55 →](../day55/README.md)

이번 주에는 **Glue Data Catalog와 Athena SQL** 내용을 다룬다. 오늘은 원본·정상 행·정상 키를 나누어 계산한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 원본·정상 행·정상 키를 나누어 계산한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

반환 행 수와 스캔량은 다른 지표다. LIMIT로 적게 표시해도 읽는 파일이 같은 비율로 줄어들지는 않는다. 파티션 조건 전후의 결과와 실행 통계를 함께 확인한다.

## 2장. 실습 준비

Day 48·50의 S3 JSON Lines 두 파티션을 사용한다. Athena SQL 워크그룹에 본인 버킷의 query-results/를 결과 경로로 지정하고 스캔량 제한을 설정한다. SQL은 Athena 콘솔에서 실행한다. YOUR_BUCKET을 실제 버킷 이름으로 바꾸고 Catalog DB는 market_lab을 사용한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 51](../day51/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
WITH parsed AS (
    SELECT symbol, trade_date,
           TRY_CAST(close_price AS DECIMAL(12,2)) AS price
    FROM market_lab.raw_prices WHERE ingest_date='2026-10-29'
)
SELECT COUNT(*) AS raw_rows,
       COUNT_IF(price > 0) AS valid_rows,
       COUNT(DISTINCT CASE WHEN price > 0
             THEN symbol || ':' || trade_date END) AS valid_keys
FROM parsed;
```

**예상 결과와 확인 기준:** Day 1 입력 기준 raw_rows=4, valid_rows=3, valid_keys=2다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 파티션 조건 유무에 따른 건수·스캔량·시간을 기록한다.
2. 작은 입력에서 차이가 작으면 그 사실도 그대로 남긴다.
3. PostgreSQL 원본 5행과 차이가 나는 이유를 입력 데이터로 설명한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day54/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** JSON과 Parquet에서 필요한 컬럼만 SELECT하는 효과는 어떻게 다를까?

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

[Athena 개요](https://docs.aws.amazon.com/athena/latest/ug/what-is.html) · [파티션](https://docs.aws.amazon.com/athena/latest/ug/partitions.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 53](../day53/README.md) · [Day 55 →](../day55/README.md)
