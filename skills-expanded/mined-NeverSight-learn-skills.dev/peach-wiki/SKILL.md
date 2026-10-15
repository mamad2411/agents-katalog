---
name: peach-wiki
description: |
  Karpathy LLM Wiki 패턴 기반 지식 관리 스킬. 코드 프로젝트와 옵시디언 노트 모두 지원.
  Raw Source(코드·문서)를 읽어 docs/wiki/에 누적형 지식베이스를 구축·유지한다.
  "wiki", "위키", "ingest", "인제스트", "wiki 점검", "wiki lint", "wiki 업데이트",
  "문서화해줘", "아키텍처 설명해줘", "어떻게 동작해?" 키워드로 트리거.
  qmd 검색 도구와 연동하여 토큰 절약 + 높은 검색 정확도 제공.
---

# peach-wiki — LLM Wiki 지식 관리

Andrej Karpathy의 LLM Wiki 패턴을 적용한 단일 스킬.
코드 프로젝트와 옵시디언 노트 모두 동일한 구조(`docs/wiki/`)로 관리한다.

---

## 자동 감지 로직

스킬 호출 시 현재 디렉토리를 감지하여 모드를 결정한다.

```
.obsidian 존재 → 옵시디언 모드 (DRIFT 없음)
.git 존재      → code 모드 (DRIFT 활성)
둘 다 존재     → code 모드 우선
둘 다 없음     → 일반 모드 (DRIFT 없음, wiki는 정상 동작)
```

감지 명령:
```bash
ls -d .obsidian 2>/dev/null && echo "OBSIDIAN=true" || echo "OBSIDIAN=false"
ls -d .git 2>/dev/null && echo "GIT=true" || echo "GIT=false"
```

---

## wiki 저장 위치 (모든 프로젝트 동일)

```
[프로젝트 루트 또는 옵시디언 보관소]/
└── docs/wiki/
    ├── WIKI-AGENTS.md       ← 운영 규칙 (세션 시작 시 먼저 읽기)
    ├── wiki-index.md        ← 전체 위키 카탈로그
    ├── wiki-log.md          ← 작업 타임라인 (append-only)
    ├── concepts/            ← 아키텍처 패턴·도메인 개념
    ├── entities/            ← 모듈·서비스·컴포넌트·인물·프로젝트
    ├── synthesis/           ← 데이터 흐름·의사결정·트레이드오프
    ├── sources/             ← 원본 문서 요약 (옵시디언 모드)
    └── diagrams/            ← Mermaid 다이어그램
```

---

## 오퍼레이션 선택

사용자 요청을 보고 아래 5개 중 하나를 실행한다.

---

## INIT — 최초 설정

`docs/wiki/WIKI-AGENTS.md`가 없을 때 실행.

### 1. preflight

```bash
# 모드 감지
ls -d .obsidian 2>/dev/null && echo "MODE=para" || echo "MODE=code"
ls -d .git 2>/dev/null && echo "GIT=true" || echo "GIT=false"

# 프로젝트 인덱스명 확정 (이후 모든 qmd 명령에 사용)
QMD_INDEX=$(basename $(pwd))
echo "QMD_INDEX=$QMD_INDEX"

# qmd 상태 확인 (named index 기준)
qmd --index "$QMD_INDEX" status 2>/dev/null
```

- qmd 미설치 시:
  ```
  qmd가 미설치 상태입니다.
  wiki는 동작하지만 qmd 설치 시 토큰 절약 + 검색 정확도가 크게 향상됩니다.
  설치: npm install -g @tobilu/qmd
  ```
  → 설치 권고 후 wiki 생성은 계속 진행

- qmd 설치됨 → 해당 인덱스의 컬렉션 등록 여부 확인:
  ```bash
  qmd --index "$QMD_INDEX" collection list
  ```

### 2. qmd 컬렉션 등록 (qmd 설치 시)

**`--index "$QMD_INDEX"` 패턴을 항상 사용한다.**
이 플래그는 DB(`~/.cache/qmd/$QMD_INDEX.sqlite`)와 설정(`~/.config/qmd/$QMD_INDEX.yml`)을
기본 인덱스와 완전히 분리하여, 다른 프로젝트·개인 옵시디언 컬렉션을 건드리지 않는다.

미등록 컬렉션이면 등록:
```bash
# code 모드
qmd --index "$QMD_INDEX" collection add . --name "$QMD_INDEX" --mask "**/*.{ts,vue,md,sql,py,go,js}"

# 옵시디언 모드
qmd --index "$QMD_INDEX" collection add . --name "$QMD_INDEX" --mask "**/*.md"

# 컨텍스트 설명 추가 (검색 품질 핵심)
qmd --index "$QMD_INDEX" context add "qmd://$QMD_INDEX/" "프로젝트 한 줄 설명"

# 인덱싱 (해당 인덱스의 컬렉션만 처리됨)
qmd --index "$QMD_INDEX" update && qmd --index "$QMD_INDEX" embed
```

> **격리 원리**: `--index` 지정 시 해당 인덱스에 등록된 컬렉션만 처리된다.
> 기본 `index.sqlite`에 등록된 다른 프로젝트·para 컬렉션은 전혀 영향받지 않는다.
> (공식 문서: "Use separate index for different knowledge base")

> **주의**: `--index` 없이 plain `qmd update/embed`를 실행하면 기본 인덱스의
> 전체 컬렉션(CloudStorage 경로 포함)이 처리된다. 반드시 `--index`를 붙여라.

### 3. 기존 wiki 마이그레이션

기존 위키 폴더 감지:
```bash
ls -d .wiki 2>/dev/null && echo "기존 .wiki/ 발견"
ls -d 5-Wiki 2>/dev/null && echo "기존 5-Wiki/ 발견"
```

발견 시 사용자에게 확인:
```
기존 [.wiki/ 또는 5-Wiki/]가 발견되었습니다.
docs/wiki/로 이동합니까? (기존 폴더는 백업 후 이동)
[Y/n]
```

승인 시:
1. 기존 폴더를 `docs/wiki/`로 복사
2. 기존 폴더 이름에 `.bak` 접미사 추가 (안전 백업)
3. wiki-index.md, WIKI-AGENTS.md 경로 업데이트

### 4. docs/wiki/ 생성

→ `references/WIKI-AGENTS-템플릿.md` 기반으로 WIKI-AGENTS.md 생성
→ wiki-index.md, wiki-log.md 초기화
→ concepts/, entities/, synthesis/, sources/, diagrams/ 폴더 생성

### 5. AGENTS.md에 wiki 참조 규칙 추가

> **`프로젝트명` 자리에 `$QMD_INDEX` 실제 값을 삽입한다.** (예: `tang`, `peach-www`)

대상 프로젝트의 AGENTS.md에 아래 섹션 추가 (`프로젝트명` → 실제 프로젝트명으로 치환):

```
## wiki 참조 (필수)
코드 생성·분석 전 아래 순서를 따른다.
1. `qmd --index 프로젝트명 query "키워드" -c 프로젝트명` 으로 wiki + 소스 통합 검색
2. qmd 미설치 시 `docs/wiki/wiki-index.md` → 관련 페이지 직접 Read
3. `docs/wiki/`도 없으면 기존 방식대로 진행

## qmd 인덱스 (필수)
이 프로젝트의 qmd 인덱스명: `프로젝트명`
모든 qmd 명령에 `--index 프로젝트명`을 붙인다.
plain `qmd update/embed`는 다른 프로젝트 인덱스를 오염시킬 수 있으므로 금지.

    # 검색
    qmd --index 프로젝트명 query "키워드" -c 프로젝트명

    # 인덱스 갱신
    qmd --index 프로젝트명 update && qmd --index 프로젝트명 embed
```

### 6. 프로젝트 개요 페이지 생성

`docs/wiki/entities/project-overview.md` 생성 (프로젝트 구조 파악 후)

### 7. 사람에게 첫 ingest 영역 확인

### 8. wiki-log.md 기록

---

## INGEST — Raw Source → 위키 추가

트리거: "ingest", "wiki에 추가", "문서화해줘", 파일/모듈 언급

### 절차

1. **소스 파악** — qmd 1순위, Read fallback:
   ```bash
   # qmd 사용 가능 시 (1순위) — named index 필수
   qmd --index "$QMD_INDEX" query "모듈명 또는 키워드" -c "$QMD_INDEX"

   # qmd 미사용 시 (fallback)
   # 직접 파일 Read
   ```

2. **요약 확인** — 핵심 3~5줄 요약 후 사람에게 확인

3. **wiki 페이지 생성/업데이트**:
   - code: 모듈 → `entities/module-이름.md`, API → `entities/api-이름.md`, DB → `entities/schema-이름.md`
   - para: 노트 → `sources/YYYY-MM-DD-제목.md`, 인물 → `entities/이름.md`, 프로젝트 → `entities/project-이름.md`

4. **concepts/ 업데이트** — 아키텍처 패턴, 도메인 개념 반영

5. **related_files 경로 검증** (code 모드):
   - qmd URI와 실제 파일 경로가 다를 수 있음 (하이픈 vs dot 등)
   - related_files에 넣기 전 `ls` 또는 `Glob`으로 실제 존재 확인
   - 존재하지 않는 경로는 제외하거나 정확한 경로로 수정

6. **diagrams/ 생성** (필요 시) — Mermaid로 흐름 시각화

7. **wiki-index.md 갱신** + **wiki-log.md 기록**

8. **qmd 반영** (qmd 설치 시):
   - **반드시 `--index "$QMD_INDEX"` 패턴 사용** — 다른 인덱스 오염 방지
   - 새 파일 추가·이동·대량수정:
     ```bash
     qmd --index "$QMD_INDEX" update && qmd --index "$QMD_INDEX" embed
     ```
   - 소규모 텍스트 수정:
     ```bash
     qmd --index "$QMD_INDEX" update
     ```
   - 변경 없으면 실행하지 않음
   - `$QMD_INDEX`가 세션에 없으면: `QMD_INDEX=$(basename $(pwd))`로 재선언

### 페이지 형식

```yaml
---
tags: [wiki, entities|concepts|synthesis|sources|diagrams]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [소스 파일 경로]
related_files: [직접 연관된 파일] # code 모드
---

# 제목
> 한 줄 요약

## 핵심 내용
## 연결된 위키 페이지
- [[관련 페이지]]
## 원본 소스
- `경로/파일명`
```

---

## QUERY — 위키 기반 질문 답변

트리거: "어떻게 동작해?", "흐름 설명해줘", "~와 ~의 관계", "~에 대해 정리"

> `$QMD_INDEX` 미선언 시: `QMD_INDEX=$(basename $(pwd))`로 재선언

### 절차

1. **qmd 통합 검색** (1순위):
   ```bash
   qmd --index "$QMD_INDEX" query "질문 내용" -c "$QMD_INDEX"
   ```

2. **wiki Read** (fallback 또는 보강):
   - `docs/wiki/wiki-index.md` 읽기 → 관련 페이지 파악
   - 관련 위키 페이지 읽기

3. **인용 포함 답변** — 출처: 파일 경로 (+ 줄 번호)

4. **가치 있는 답변 → 위키에 환류 제안**:
   ```
   이 답변을 docs/wiki/synthesis/YYYY-MM-DD-주제.md로 저장할까요?
   ```

5. **wiki-log.md 기록**

---

## DRIFT — git 변경 감지 후 위키 갱신

트리거: "wiki 업데이트해줘", "변경사항 반영해줘"
**code 모드(.git 존재)에서만 활성화.**

> `$QMD_INDEX` 미선언 시: `QMD_INDEX=$(basename $(pwd))`로 재선언

### 절차

1. **변경 파일 목록 추출**:
   ```bash
   git diff --name-only HEAD~1    # 마지막 커밋
   git diff --name-only           # 미커밋 변경
   ```

2. **영향받은 위키 페이지 파악**:
   - 변경 파일의 `related_files`를 가진 위키 페이지 검색

3. **위키 페이지 업데이트** — 변경 내용 반영, `updated` 날짜 갱신

4. **qmd 반영** (qmd 설치 시):
   ```bash
   qmd --index "$QMD_INDEX" update
   ```

5. **새 모듈 감지** → 자동 INGEST 제안

6. **wiki-log.md 기록**

---

## LINT — 위키 점검

트리거: "wiki 점검", "lint", "문서 정합성 확인"

### 점검 항목

1. **드리프트 탐지** (code 모드): git log vs wiki updated 날짜 비교
2. **고아 페이지**: wiki-index.md에 없는 페이지
3. **깨진 소스 링크**: 삭제된 파일 참조 여부
4. **모순**: 같은 주제에 대해 다른 설명
5. **미문서화 항목**: 소스에는 있는데 위키 페이지 없는 것
6. **템플릿 드리프트**: WIKI-AGENTS.md가 최신 템플릿과 차이 여부

### 리포트 형식
```
## [YYYY-MM-DD] lint | [프로젝트명]
- 드리프트 위험: N개 페이지
- 고아 페이지: N개
- 깨진 링크: N개
- 미문서화: [목록]
- 권고: [조치 목록]
```

---

## 핵심 원칙

- **Raw Source는 절대 수정 금지** — 읽기만 (코드, 옵시디언 노트 모두)
- **`docs/wiki/` 하위에만 쓰기** — LLM 전용 공간
- **qmd 1순위**: 설치되어 있으면 항상 qmd query로 먼저 검색 (토큰 절약)
- **복리 효과**: Ingest할수록 교차참조가 깊어지고 Query 품질이 높아짐
- **언어**: 한국어 (코드·기술 용어는 영어 유지)
- **링크**: `[[파일명]]` Obsidian 형식 (para), 파일 경로 (code)

---

## qmd 주요 명령 참조

> **모든 명령에 `--index "$QMD_INDEX"`를 붙인다.**
> `QMD_INDEX=$(basename $(pwd))`로 세션 시작 시 선언.

```bash
# 상태 확인
qmd --index "$QMD_INDEX" status
qmd --index "$QMD_INDEX" collection list

# 하이브리드 검색 (권장)
qmd --index "$QMD_INDEX" query "키워드" -c "$QMD_INDEX"

# 키워드 검색
qmd --index "$QMD_INDEX" search "키워드" -c "$QMD_INDEX"

# 파일 경로만 출력
qmd --index "$QMD_INDEX" query "키워드" -c "$QMD_INDEX" --files

# 특정 파일 읽기
qmd --index "$QMD_INDEX" get "qmd://$QMD_INDEX/경로/파일.md"

# 인덱스 갱신 (대량 변경)
qmd --index "$QMD_INDEX" update && qmd --index "$QMD_INDEX" embed

# 인덱스 갱신 (소규모 수정)
qmd --index "$QMD_INDEX" update
```
