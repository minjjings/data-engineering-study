# Day 57. Glue 가격 정제와 결과 저장

**12주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 56](../day56/README.md) · [Day 58 →](../day58/README.md)

이번 주에는 **Glue ETL과 데이터 웨어하우스** 내용을 다룬다. 오늘은 무효값을 분리하고 업무 키별 한 행을 저장한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 무효값을 분리하고 업무 키별 한 행을 저장한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

관리형 환경에서도 품질 규칙은 직접 정해야 한다. 이번에는 유한한 양수 가격만 남기고 동일 키의 첫 정상값을 선택한다. 입력에 수집 시각이 없으므로 이 선택을 최신값이라고 부르지 않는다.

## 2장. 실습 준비

S3·Catalog·로컬 PostgreSQL을 사용한다. Glue Python shell 작업을 작은 JSON Lines로 한 번 실행한다. 실습용 역할에 입력·스크립트 읽기, 출력 prefix 쓰기, 로그 권한을 부여한다. Python 런타임·타임아웃·실행 용량을 기록한다. Redshift는 역할 비교까지 필수이며 생성은 선택 과제다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 56](../day56/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
import json
from decimal import Decimal, InvalidOperation
clean = {}
for line in body.decode("utf-8").splitlines():
    row = json.loads(line)
    try:
        price = Decimal(str(row["close_price"]))
        if not price.is_finite() or price <= 0:
            continue
    except InvalidOperation:
        continue
    clean.setdefault((row["symbol"], row["trade_date"]), row)
payload = "".join(json.dumps(row) + "\n" for row in clean.values())
boto3.client("s3").put_object(Bucket=bucket,
    Key="curated/market/batch=2026-10-29/prices.jsonl", Body=payload.encode("utf-8"))
print({"clean_keys": len(clean)})
```

**예상 결과와 확인 기준:** QQQ·SPY 두 행이 출력되고 clean_keys=2다. 가격 문자열은 유지하며 Parquet 변환은 Spark 주차에서 배운다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 원본 4·정상 3·무효 1·중복 1·최종 2건을 로그로 남긴다.
2. 결과를 내려받아 Day 1 정제 결과의 키·가격과 비교한다.
3. 작업을 다시 실행해 같은 출력 키와 내용인지 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day57/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 재실행마다 같은 prefix에 파일을 추가하면 어떤 중복이 생길까?

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

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 56](../day56/README.md) · [Day 58 →](../day58/README.md)
