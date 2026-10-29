# Day 47. S3 버킷·객체·prefix

**10주 차 · 주간 2일차 | 약 90~120분**

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 46](../day46/README.md) · [Day 48 →](../day48/README.md)

이번 주에는 **S3 데이터 레이크와 접근 권한** 내용을 다룬다. 오늘은 비공개 버킷을 만들고 저장 경로를 설계한다.

> 미리 작성한 교재다. 아래 예제·예상 결과는 학습 기준이며 실행을 완료했다는 뜻은 아니다. 과제에서 요구하는 코드·설정·결과는 직접 작성한다. 시장 가격은 가상 데이터다.

## 오늘의 학습 목표

- 비공개 버킷을 만들고 저장 경로를 설계한다.
- 예제의 입력과 결과를 비교하고 처리 기준을 자기 말로 설명한다.
- 직접 작성한 과제와 실행 근거를 남긴다.

| 순서 | 할 일 | 예상 시간 |
| --- | --- | --- |
| 1 | 개념과 준비 항목 확인 | 20분 |
| 2 | 예제 실행·입출력 확인 | 25~35분 |
| 3 | 직접 구현·실패 또는 경계 상황 실험 | 30~45분 |
| 4 | 결과 기록과 리뷰 | 15~20분 |

## 1장. 개념 이해하기

S3는 객체 키와 내용으로 데이터를 저장한다. 폴더처럼 보이는 경로는 키의 prefix이며 파일시스템 폴더와는 다르다. Raw·curated·query-results를 나누면 보관 기간과 권한을 따로 관리하기 쉽다.

## 2장. 실습 준비

AWS 계정·리전·예산 알림과 AWS CLI v2를 준비한다. PowerShell에서 인증한 프로필과 AWS_PROFILE, AWS_DEFAULT_REGION=ap-northeast-2, DE_BUCKET 환경변수를 설정한다. DE_BUCKET에는 본인이 소유한 실습용 버킷 이름을 넣는다. 버킷 이름은 전역에서 유일해야 한다. 실제 AWS 실습은 비용이 발생할 수 있다. 계정이 없다면 로컬 파일·권한 설계까지 진행하고 클라우드 실행은 미완료로 기록한다.

이전 학습일의 과제를 아직 구현하지 않았다면 해당 교재에서 먼저 준비한다. 문서 안의 파일명은 앞으로 작성할 산출물을 포함한다. 첫 사용 환경은 이번 주 첫 교재인 [Day 46](../day46/README.md)의 준비 항목도 확인한다.

## 3장. 예제로 따라 해보기

먼저 예상 결과를 읽고 어떤 입력이 어떤 이유로 남는지 생각한다. 아래 코드가 부분 예제라면 주석에서 지정한 파일·함수·이전 코드에 합친다.

```powershell
# DE_BUCKET은 본인이 정한 유일한 실습 버킷 이름이다.
aws s3api create-bucket --bucket $env:DE_BUCKET --region ap-northeast-2 --create-bucket-configuration LocationConstraint=ap-northeast-2
aws s3api put-public-access-block --bucket $env:DE_BUCKET --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api get-public-access-block --bucket $env:DE_BUCKET
```

**예상 결과와 확인 기준:** 서울 리전에 버킷이 생성되고 공개 접근 차단 네 항목이 true다. 이미 만든 버킷에는 생성 명령을 반복하지 않는다.

화면 출력이나 성공 상태만으로 끝내지 않고, 오늘 목표와 직접 연결되는 건수·키·값·상태를 확인한다.

## 4장. 직접 해볼 실습 과제

1. raw/market/ingest_date=날짜/와 curated/market/trade_date=날짜/ 경로를 설계한다.
2. 공개 차단·암호화·리전을 콘솔과 CLI에서 확인한다.
3. 버킷 목적과 정리 예정일을 기록한다.

작성한 코드·SQL·설정은 이 day 폴더 또는 과제에서 지정한 공통 디렉터리에 저장한다. 실행 기록은 `day47/notes.md`에 남긴다. 원본 예제와 별도 경로를 사용하고, 오류 입력·재실행으로 결과가 달라졌다면 그 이유도 기록한다.

## 5장. 막혔을 때 확인하기

명령은 저장소 루트의 PowerShell에서 실행한다. 환경변수와 컨테이너 상태를 먼저 확인하고 오류 전문을 기록한다.

예상 건수와 다르면 사용한 입력·필터·기존 상태부터 비교한다. 해결하지 못한 오류는 입력과 실행 명령, 오류 메시지를 함께 남긴다.

## 오늘의 완료 기준

- [ ] 핵심 개념을 오늘 예제에 연결해 설명했다.
- [ ] 따라 하기 예제의 실제 결과를 예상 결과와 비교했다.
- [ ] 직접 해볼 과제 세 개를 구현·실행하고 근거를 남겼다.
- [ ] 오류 또는 남은 한계를 기록하고 다음 단계의 선행 조건을 확인했다.

**생각해볼 질문:** 수집일과 거래일을 같은 파티션 키로 쓰면 과거 데이터 재수집을 어떻게 구별할까?

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

[AWS CLI 설치](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) · [S3 공개 접근 차단](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

[전체 계획](../README.md) · [120일 목차](../README.md#day-index) · [← Day 46](../day46/README.md) · [Day 48 →](../day48/README.md)
