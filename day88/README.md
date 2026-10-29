# Day 88. Watermark와 지연 이벤트

**18주 차 · 주간 3일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 87](../day87/README.md) · [Day 89 →](../day89/README.md)

이번 주에는 **Spark Structured Streaming과 처리 보장** 내용을 다룬다. 오늘은 상태 정리 기준과 늦은 입력의 처리 범위를 관찰한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 상태 정리 기준과 늦은 입력의 처리 범위를 관찰한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

Streaming Watermark는 배치의 증분 처리 위치와 다른 개념이다. 관측한 event time으로 상태를 언제 정리할지 판단한다. 허용 범위 안의 지연 처리와 범위 밖 이벤트가 항상 폐기된다는 주장은 구분해야 한다.

## 2장. 실습 준비

Day 81 Kafka와 PySpark 4.0.1을 사용한다. spark-submit에 --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1을 붙인다. 호스트에서는 localhost:9092로 접속한다. 각 day에 별도 checkpoint 경로를 쓰고 같은 실험의 재시작에서는 그 경로를 유지한다. Python 블록을 dayNN/practice.py로 저장하고 부분 예제는 명시한 이전 코드에 합친다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 86](../day86/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```python
# Day 87의 events 생성 코드 뒤에 연결하고 기존 console 출력 부분을 대체한다.
counts = (events.withWatermark("event_time", "2 minutes")
    .groupBy(F.window("event_time", "1 minute"), "symbol").count())
q = (counts.writeStream.outputMode("append").format("console")
    .option("checkpointLocation", "day88/checkpoint").start())
q.awaitTermination(60)
q.stop()
spark.stop()
```

**예상 결과와 확인 기준:** append 시간창 결과는 watermark가 창을 지나야 나온다. 고정된 과거 이벤트만 넣고 즉시 결과를 기대하지 않는다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. 09:00·09:01 이벤트 후 09:05 이벤트로 watermark를 전진시킨다.
2. 09:00 지연 이벤트를 전진 전후에 넣고 출력과 폐기 지표를 기록한다.
3. query.lastProgress의 eventTime·stateOperators를 확인한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day88/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

예제에서 지정한 Python 환경·현재 경로·패키지 버전을 확인한다. Task 내부나 이전 코드에 합치는 부분 예제는 주석의 실행 문맥을 먼저 준비한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 새 이벤트 없이 벽시계 시간만 지나도 watermark는 항상 전진할까?

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

[Kafka 연동](https://spark.apache.org/docs/4.0.1/streaming/structured-streaming-kafka-integration.html) · [Streaming API](https://spark.apache.org/docs/4.0.1/streaming/apis-on-dataframes-and-datasets.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 87](../day87/README.md) · [Day 89 →](../day89/README.md)
