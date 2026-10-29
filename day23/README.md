# Day 23. Python 트랜잭션과 적재 실패

**5주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 22](../day22/README.md) · [Day 24 →](../day24/README.md)

이번 주에는 **Python에서 PostgreSQL로 안정적으로 적재** 내용을 다룬다. 오늘은 실패 시 롤백하고 성공한 실행만 반영한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 실패 시 롤백하고 성공한 실행만 반영한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

psycopg 연결 컨텍스트는 정상 종료 시 커밋하고 예외가 빠져나오면 롤백한다. 예외를 컨텍스트 안에서 삼키면 의도와 다른 커밋 경로가 될 수 있으므로 실패를 명확히 전달해야 한다.

검증 실패도 저장 실패와 같은 배치 실패로 볼 수 있다. 목표 표 적재 뒤 품질 검사를 통과해야 커밋하도록 설계하면 잘못된 결과의 공개를 막을 수 있다. 로그 기록이나 외부 파일 생성은 DB 트랜잭션과 별개다.

## 2장. 실습 준비

4주 차 가상환경에 `.\.venv\Scripts\python.exe -m pip install "psycopg[binary]"`로 드라이버를 설치한다. PowerShell에서 `$env:DE_DSN="host=127.0.0.1 port=5433 dbname=market_db user=de_user password=de_password"`를 설정한다. 로컬 전용 연결값이며 실제 비밀값은 저장하지 않는다. Python 블록은 dayNN/practice.py로 저장해 가상환경 Python으로 실행한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 21](../day21/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
import os
import psycopg

with psycopg.connect(os.environ["DE_DSN"], autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TEMP TABLE tx_demo(id integer PRIMARY KEY)")
    try:
        with conn.transaction():
            conn.execute("INSERT INTO tx_demo VALUES (1)")
            conn.execute("INSERT INTO tx_demo VALUES (1)")
    except psycopg.errors.UniqueViolation:
        print("rolled back")
    print(conn.execute("SELECT count(*) FROM tx_demo").fetchone()[0])
```

**예상 결과와 확인 기준:** rolled back 뒤에 0이 출력된다. 실패한 트랜잭션의 첫 INSERT도 취소된다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 두 번째 id를 2로 바꿔 정상 커밋 2건과 비교한다.
2. 가격 적재 뒤 양수 검사 실패를 예외로 전달하고 목표 표 상태를 비교한다.
3. 성공·실패 시 연결 종료와 로그·상태 갱신 순서를 문서화한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day23/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** DB 커밋 성공 직후 프로세스가 종료되면 재실행에서 무엇을 확인해야 할까?

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

[Psycopg 매개변수](https://www.psycopg.org/psycopg3/docs/basic/params.html) · [트랜잭션](https://www.psycopg.org/psycopg3/docs/basic/transactions.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 22](../day22/README.md) · [Day 24 →](../day24/README.md)
