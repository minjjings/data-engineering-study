# Day 107. GitHub Actions 첫 CI

**22주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 106](../day106/README.md) · [Day 108 →](../day108/README.md)

이번 주에는 **테스트·CI/CD와 재현 가능한 환경** 내용을 다룬다. 오늘은 PR에서 기본 검증이 자동 실행되게 한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- PR에서 기본 검증이 자동 실행되게 한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

CI는 변경마다 같은 검사를 독립 환경에서 수행한다. 로컬DB나 개인 경로를 참조하면 다른 환경에서 재현되지 않는다. 아래 workflow는4주에 작성한 tests와requirements가 있어야 동작한다.

## 2장. 실습 준비

4~5주 src와 tests, dbt 프로젝트가 준비되어 있어야 한다. 루트 requirements.txt에 실제 필요한 패키지와 버전을 정리한다. CI는 GitHub Actions의 독립 PostgreSQL17 서비스를 사용하고 로컬 실습DB·AWS 계정에 연결하지 않는다. workflow는 작성·로컬 확인 후 사용자가 push했을 때 원격 실행 결과를 확인한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 106](../day106/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```yaml
# .github/workflows/ci.yml
name: study-ci
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python -m pip install -r requirements.txt
      - run: python -m unittest discover -s tests
```

**예상 결과와 확인 기준:** push·PR 시 검사하도록 정의한다. 이 교재 작성은 workflow 파일이나 원격 실행을 미리 생성하지 않으며 직접 실습에서 작성한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. workflow를 작성하고 직접 실행할 테스트 개수를 확인한다.
2. 의도적으로 정제 규칙을 깨뜨린 변경과 수정 후 변경의CI결과를 비교한다.
3. 코드 검사 도구를 사용한다면 규칙과 선택 이유를 설명하고CI에 연결한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day107/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

설정 예제는 지정한 파일의 위치에 넣는다. 일부 설정만 보인 경우 기존 키에 병합하고 같은 최상위 키를 중복 작성하지 않는다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 빨간CI를 무시하고도 배포할 수 있다면 어떤 절차가 더 필요할까?

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

[GitHub Actions PostgreSQL 서비스](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers) · [Python CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 106](../day106/README.md) · [Day 108 →](../day108/README.md)
