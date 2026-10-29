# Day 93. 초기 snapshot과 변경 이벤트

**19주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 92](../day92/README.md) · [Day 94 →](../day94/README.md)

이번 주에는 **PostgreSQL CDC와 Debezium** 내용을 다룬다. 오늘은 원본 상태와 추가·수정·삭제 이벤트를 비교한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 원본 상태와 추가·수정·삭제 이벤트를 비교한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

초기 snapshot은 현재 행을 읽고 이후 변경 스트림을 이어간다. op·before·after·source는 이벤트 의미와 위치를 해석하는 단서다. converter 설정에 따라 payload 껍질 유무가 달라지므로 실제 이벤트 구조를 확인한다.

## 2장. 실습 준비

시장 DB와 분리한 CDC용 PostgreSQL을 Day 91에서 만든다. Kafka는 Day 81의 동일 Compose 네트워크를 사용하고 Connect는 kafka:29092로 접속한다. 공식 튜토리얼과 맞는 Debezium Connect 이미지 태그를 고정한다. localhost:8083은 호스트에서 보는 Connect REST 주소다. JSON에는 학습용 로컬 비밀번호만 사용한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 91](../day91/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```sql
-- CDC용DB의psql에서실행한다.
INSERT INTO public.prices VALUES (3, 'TEST', 100.00);
UPDATE public.prices SET price=621.00 WHERE id=1;
DELETE FROM public.prices WHERE id=2;
SELECT * FROM public.prices ORDER BY id;
```

**예상 결과와 확인 기준:** 원본 최종 상태는 id 1·3이다. Kafka에서 snapshot r, 추가 c, 수정 u, 삭제 d를 확인한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. marketcdc.public.prices에서 초기 두 행 snapshot을 보관한다.
2. SQL을 한 문장씩 실행하며 이벤트와 대조한다.
3. 삭제 이벤트와 뒤따르는 null tombstone을 구분한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day93/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

SQL 실행 위치를 확인한다. 일반 PostgreSQL SQL은 psql에서, Athena SQL은 Athena에서, Jinja가 있는 모델 SQL은 dbt 모델 파일에서 실행한다. TEMP 테이블은 생성한 연결에서만 보인다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** after가 NULL이라는 이유로 삭제 이벤트를 무시하면 대상 표는 어떻게 될까?

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

[PostgreSQL 커넥터](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) · [튜토리얼](https://debezium.io/documentation/reference/stable/kc-tutorial.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 92](../day92/README.md) · [Day 94 →](../day94/README.md)
