# Day 31. dbt 설치와 첫 모델

**7주 차 · 주간 1일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 30](../day30/README.md) · [Day 32 →](../day32/README.md)

이번 주에는 **dbt 프로젝트와 계층별 SQL 모델** 내용을 다룬다. 오늘은 SQL을 파일과 의존성으로 관리하는 프로젝트를 만든다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- SQL을 파일과 의존성으로 관리하는 프로젝트를 만든다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

dbt는 DB 안에서 SQL 변환을 실행한다. Python 수집이나 원본 다운로드를 대신하지 않는다. project에는 모델·테스트를, profile에는 연결 설정을 두며 비밀번호는 환경변수로 전달한다. dbt debug의 연결 성공과 모델 결과의 정확성은 별개다.

## 2장. 실습 준비

전용 환경에 dbt-postgres를 설치하고 dbt --version을 기록한다. Day 31에서 dbt/market 프로젝트와 dbt/profiles/profiles.yml을 만든다. 이후 dbt 명령은 dbt/market에서 실행하고 DBT_PROFILES_DIR을 profiles 디렉터리 절대 경로로 설정한다. 가상환경의 dbt 실행 파일을 사용한다. DB는 호스트 127.0.0.1:5433, 원천은 public.raw_market_prices다. SQL 모델은 파일에 저장하며 psql에 Jinja 문법을 직접 입력하지 않는다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 31](../day31/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

### 전용 환경과 프로젝트 준비

루트 PowerShell에서 실행한다. 아래 명령의 `dbt`는 전용 가상환경에 설치된 실행 파일이다. 이후 교재에서는 간단히 `dbt`라고 표기하므로 이 절대 경로를 사용한다.

```powershell
python -m venv .venv-dbt
.\.venv-dbt\Scripts\python.exe -m pip install dbt-postgres
$dbtExecutable = (Resolve-Path .\.venv-dbt\Scripts\dbt.exe).Path
New-Item -ItemType Directory -Force dbt/profiles | Out-Null
$env:DBT_PROFILES_DIR = (Resolve-Path dbt/profiles).Path
$env:DE_DB_PASSWORD = 'de_password'
Set-Location dbt
& $dbtExecutable init market --skip-profile-setup
Set-Location market
& $dbtExecutable --version
```

새 PowerShell에서는 `$dbtExecutable`, `DBT_PROFILES_DIR`, `DE_DB_PASSWORD`를 다시 설정한다. 아래 profile을 저장한 뒤 `dbt_project.yml`의 `profile: market`을 확인하고 `& $dbtExecutable debug`를 실행한다. 예제의 로컬 비밀번호는 환경변수로만 전달한다.

### 연결 profile 작성

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```yaml
# dbt/profiles/profiles.yml
market:
  target: dev
  outputs:
    dev:
      type: postgres
      host: 127.0.0.1
      port: 5433
      user: de_user
      password: "{{ env_var('DE_DB_PASSWORD') }}"
      dbname: market_db
      schema: analytics
      threads: 1
```

**예상 결과와 확인 기준:** DE_DB_PASSWORD에 로컬 암호를 설정하고 profile이 market인 프로젝트에서 dbt debug를 실행하면 연결 검사를 통과한다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. dbt init market으로 dbt/market을 생성하고 dbt_project.yml의 profile을 market으로 맞춘다.
2. models/example 기본 모델을 확인한 뒤 models/hello.sql에 SELECT 1 AS id를 작성하고 dbt run --select hello를 실행한다.
3. 버전·profile 경로·실제 생성 스키마와 hello 결과 1행을 기록한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day31/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

설정 예제는 지정한 파일의 위치에 넣는다. 일부 설정만 보인 경우 기존 키에 병합하고 같은 최상위 키를 중복 작성하지 않는다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** dbt가 연결한 DB와 실제 원본이 저장된 DB가 다르면 어떤 오류가 날까?

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

[Postgres 연결](https://docs.getdbt.com/docs/local/connect-data-platform/postgres-setup) · [ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 30](../day30/README.md) · [Day 32 →](../day32/README.md)
