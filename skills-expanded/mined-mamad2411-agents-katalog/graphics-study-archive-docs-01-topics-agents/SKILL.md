# Topics Guidelines

## 적용 범위

이 규칙은 `Docs/01_Topics/` 아래 문서에 적용한다.

## 책임

- 여러 예제를 관통하는 graphics concept를 설명한다.
- 예제 하나의 구현 설명은 대상 코드 폴더 README로 링크한다.
- build/run/capture 사실 상태는 `Docs/02_Verification`으로 링크하고, 구현 흐름과 시각 결과는 `Docs/03_Demos`로 링크한다.
- publication 판단은 `Docs/05_Publication`으로 링크한다.
- raw/reference 원문, source comment, GitHub draft, 개인 메모는 이 폴더에 두지 않는다.

## 작성 단위

- Topic group마다 `README.md`와 `topic-index.md`를 둔다.
- P0 Topic은 별도 문서로 승격한다.
- P1/P2 Topic은 먼저 `topic-index.md`에 후보로 둔다.
- 예제별 문서와 중복되는 내용은 링크로 처리한다.

## 상세 Topic 구조

- `## 목적`, `## 책임 범위`, `## 핵심 개념`, `## 한계`, `## 관련 문서` 순서를 유지한다.
- Topic별 개념 전개에는 `처리 단계`, `수학적 배경`, `Pipeline 위치`처럼 내용에 맞는 선택 섹션을 사용할 수 있다.
- `## 핵심 개념`은 최소 2개 `###` 소제목으로 구성한다.
- 예제 고유 코드 탐색은 Example README로, 구현 흐름과 시각 결과는 `Docs/03_Demos`로 위임한다.
- build/run/capture 상태는 `Docs/02_Verification`으로 위임한다.
- `## 관련 문서`에서 Example README, Verification, Demo 정본을 연결한다.

## 품질 검증

```powershell
powershell -ExecutionPolicy Bypass -File Docs/98_Tools/validators/validate-topic-doc-quality.ps1
```

## 문체

- 평서형 현재형을 사용한다.
- 존댓말, 대화체, 감상문체를 사용하지 않는다.
- technical keywords, folder names, API names는 영어를 유지한다.
