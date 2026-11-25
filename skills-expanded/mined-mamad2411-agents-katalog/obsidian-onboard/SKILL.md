---
name: obsidian-onboard
description: |
  현재 프로젝트의 도메인 지식·아키텍처·용어·진행 상태를 Obsidian vault에 표준화된 6노트 세트로 정리/갱신한다. 다음 AI 세션부터 코드 재탐색 없이 vault 진입점을 먼저 읽어 컨텍스트를 잡을 수 있게 만드는 온보딩 스킬.

  반드시 이 스킬을 사용해야 하는 트리거:
  - "옵시디언 온보딩", "obsidian onboard", "vault 온보딩"
  - "프로젝트를 옵시디언에 정리해줘", "도메인 정리해서 vault에", "프로젝트 위키 만들어줘"
  - "AI Agent가 참고할 문서 구성", "온보딩 문서 만들어줘"
  - "/obsidian-onboard", "/obsidian-onboard --update", "/obsidian-onboard --dry-run" 슬래시 호출
  - 옵시디언/vault/위키 + 프로젝트/도메인/온보딩이 같은 발화에 등장할 때

  init / update / dry-run 3개 모드 지원. 기존 vault에 사람이 작성한 내용은 절대 덮어쓰지 않는다.
---

# Obsidian Onboard

현재 작업 중인 프로젝트의 도메인 지식, 아키텍처, 도메인 용어, 진행 상태를 **Obsidian vault의 표준 6노트 세트**로 정리한다. 다음 AI 세션부터는 vault 진입점 1개를 읽으면 컨텍스트를 잡을 수 있다.

> **이전 시도가 미비했던 이유를 막는 장치**: 명확한 템플릿 + AUTO/HUMAN 마커 분리 + update 모드의 HUMAN 보호.

## 무엇을 만드는가

vault의 `20 Projects/{프로젝트명}/` 디렉토리에 6개 노트:

| 노트 | 답하는 질문 |
|------|-----------|
| `AI_ENTRYPOINT.md` | "지금 작업에서 어떤 노트를 먼저 읽어야 하나?" |
| `Overview.md` | "이 프로젝트가 무엇이고 왜 존재하나?" |
| `Architecture.md` | "이 시스템이 어떻게 조립되어 있나?" |
| `Glossary.md` | "이 프로젝트의 용어가 무엇을 뜻하나?" |
| `Current Work.md` | "지금 어디까지 했고 다음은 무엇인가?" |
| `Open Questions.md` | "확신이 없는 항목이 무엇인가?" |

그리고 프로젝트의 `CLAUDE.md`에 추가할 **vault 연동 스니펫**을 출력한다 (직접 수정 X).

## 트리거 키워드 (description으로 이미 등록됨)

- 슬래시: `/obsidian-onboard`, `/obsidian-onboard --update`, `/obsidian-onboard --dry-run`
- 자연어: "옵시디언 온보딩", "vault에 정리", "프로젝트 위키", "도메인 정리", "AI 참고 문서"

## 모드 결정 트리

```
사용자 발화에 --dry-run? → dry-run 모드
사용자 발화에 --update?  → update 모드
그 외:
  vault의 프로젝트 디렉토리가 이미 존재?
    Yes → update 모드로 자동 전환 (사용자에게 알림)
    No  → init 모드
```

## 워크플로우

### Step 1: vault 경로 결정

다음 순서로 vault 경로를 결정한다.

1. **환경변수** `$env:OBSIDIAN_VAULT_PATH`가 설정되어 있으면 그것
2. **스킬 폴더의 `.vault-path` 파일**이 있으면 그것
3. **기본값**: `C:\Users\youn.wonhee\Documents\Obsidian Vault`
4. 위 경로가 존재하지 않으면 `AskUserQuestion`으로 묻고, 답을 `.vault-path`에 저장

vault 경로 검증:
- 디렉토리 존재 확인
- `.obsidian/` 폴더가 있는지 확인 (정말 Obsidian vault인지 검증)
- 없으면 "이 경로는 Obsidian vault가 아닌 것 같습니다. 진행할까요? (Y/n)"

### Step 2: 프로젝트 식별

- `PROJECT_NAME`: `git remote get-url origin`에서 repo명 추출 → kebab-case
  - 실패 시 현재 디렉토리명 사용
- `PROJECT_PATH`: 현재 작업 디렉토리 절대 경로
- vault 안 프로젝트 폴더 경로: `{VAULT_PATH}\20 Projects\{PROJECT_NAME}\`

### Step 3: 모드 분기

#### 3-A. init 모드

1. vault 프로젝트 폴더가 이미 존재하면 → **update 모드로 자동 전환** + 사용자 알림
   ```
   vault에 이미 {PROJECT_NAME} 프로젝트가 있습니다. update 모드로 진행합니다.
   처음부터 새로 만들려면: 폴더 삭제 후 재실행
   ```
2. 정보 추출 (Step 4) → 6개 노트 생성 → CLAUDE.md 스니펫 출력

#### 3-B. update 모드

1. vault 프로젝트 폴더가 없으면 → **init 모드로 자동 전환** + 알림
2. 백업: 각 노트를 `~/.claude/skills/productivity/obsidian-onboard/backups/{PROJECT_NAME}/{타임스탬프}/`에 복사
3. 정보 추출 (Step 4)
4. 각 노트의 AUTO 영역만 갱신 ([`references/update-merge-policy.md`](references/update-merge-policy.md) 참조)
5. 변경된 AUTO 영역에 `<!-- NEW {날짜} -->` 마커 추가
6. HUMAN 영역은 절대 건드리지 않음

#### 3-C. dry-run 모드

1. 정보 추출 (Step 4)만 수행
2. 어떤 노트가 생성/수정/유지될지 보고
3. **파일은 일절 작성하지 않음**

### Step 4: 정보 추출

[`references/extraction-rules.md`](references/extraction-rules.md)의 규칙에 따라 다음을 추출:

1. **프로젝트 메타** — name, path, last updated
2. **한 줄 요약** — CLAUDE.md → README → package.json description
3. **Tech stack** — package.json/build.gradle/pom.xml 등의 신호
4. **폴더 구조** — Glob depth 2, 표준 제외 패턴 적용
5. **진입점** — main 함수, @SpringBootApplication, package.json main 등
6. **외부 의존성** — dependencies 중 외부 시스템 클라이언트, docker-compose service
7. **컴포넌트 지도** — src/controllers, src/services 등 표준 폴더 패턴
8. **ADR 요약** — `.claude/docs/adr/`, `docs/adr/`, `decisions/` 스캔
9. **도메인 용어** — `.claude/CONTEXT.md` 우선 → 도메인 클래스명 → 자동 stub
10. **Live 상태** — git branch, git log -5, 변경 파일 수, Active Track

**추출 실패 처리**: 빈 값을 두지 않는다. 다음 중 하나로 대응:
- "TBD — (왜 추출 안 됐는지)" 표시 + [`Open_Questions.md.tmpl`](assets/Open_Questions.md.tmpl)에 자동 질문 등록
- 또는 "(자동 추출 안 됨 — 사람이 보강 필요)" 명시

### Step 5: 노트 작성 (init/update 시)

각 노트는 [`assets/`](assets/) 폴더의 `.tmpl` 파일을 기반으로 작성한다.

placeholder 치환 규칙:
- `{{PROJECT_NAME}}` → 추출된 프로젝트명
- `{{ONE_LINER}}` → 한 줄 요약
- `{{TECH_STACK_TABLE}}` → 마크다운 표
- ... 등등 (각 placeholder는 [`references/extraction-rules.md`](references/extraction-rules.md) 참조)

작성 순서:
1. `Overview.md` (기본 정보 먼저)
2. `Architecture.md` (Overview 작성한 정보 일부 재활용)
3. `Glossary.md` (도메인 용어 정리)
4. `Current Work.md` (live 상태)
5. `Open Questions.md` (자동 감지 질문 포함)
6. `AI_ENTRYPOINT.md` (다른 노트가 다 만들어진 후 인덱스 생성)

### Step 6: 결과 보고 + CLAUDE.md 스니펫 출력

사용자에게 다음을 출력:

```
## Obsidian Onboard 완료 ({모드명})

### 생성/갱신된 노트
- ✓ AI_ENTRYPOINT.md (신규 / 갱신 / 변경없음)
- ✓ Overview.md (...)
- ✓ Architecture.md (...)
- ✓ Glossary.md (...)
- ✓ Current Work.md (...)
- ✓ Open Questions.md (...)

### 자동 추출 미흡 영역 (사람 보강 필요)
- Overview.md → business_context (TBD)
- Architecture.md → data_flow, sticky_parts (TBD)
- Glossary.md → 도메인 용어 대부분 — 자동 stub 2개만 추출됨
- Open Questions.md → 자동 등록된 질문 N개

### Vault 열기
- Obsidian: vault 안 [[20 Projects/{PROJECT_NAME}/AI_ENTRYPOINT]] 열기
- 파일 직접: {VAULT_PROJECT_PATH}\AI_ENTRYPOINT.md

### 다음 단계
1. Glossary.md에 핵심 도메인 용어 추가
2. Overview.md의 비즈니스 배경 작성
3. 아래 스니펫을 프로젝트의 CLAUDE.md에 추가 (위치: "설정" 섹션 다음 권장)

[CLAUDE.md 스니펫 — references/claude-md-snippet.md 형식]
```

### Step 7: 안티 패턴 (절대 하지 말 것)

- ❌ HUMAN 영역을 update 모드에서 수정
- ❌ vault 안 다른 프로젝트 노트를 건드림 (현재 프로젝트 폴더만)
- ❌ CLAUDE.md를 자동 수정 (스니펫 출력만)
- ❌ Obsidian 설정(`.obsidian/`)을 건드림
- ❌ 추출 실패를 빈 칸으로 두기 (반드시 TBD + 설명)
- ❌ git add 수행 (사용자 정책: 사용자가 명시적으로 요청할 때만)
- ❌ vault에 없는 폴더 구조 가정 (PARA 외의 vault는 `--vault-layout=...` 인자로 처리, 일단은 PARA 전제)

## 산출물 위치 정리

| 산출물 | 위치 |
|--------|------|
| 6개 노트 | `{VAULT}\20 Projects\{PROJECT_NAME}\*.md` |
| 백업 (update 모드) | `~/.claude/skills/productivity/obsidian-onboard/backups/{PROJECT_NAME}/{타임스탬프}/` |
| vault 경로 캐시 | `~/.claude/skills/productivity/obsidian-onboard/.vault-path` |
| 마지막 실행 상태 | `~/.claude/skills/productivity/obsidian-onboard/.state.json` (선택, 미구현) |

## 참고 파일

| 파일 | 언제 읽나 |
|------|----------|
| [`references/extraction-rules.md`](references/extraction-rules.md) | 정보 추출 단계 (Step 4) |
| [`references/note-spec.md`](references/note-spec.md) | 노트 섹션 명세 검증 시 |
| [`references/claude-md-snippet.md`](references/claude-md-snippet.md) | Step 6 스니펫 출력 시 |
| [`references/update-merge-policy.md`](references/update-merge-policy.md) | update 모드 머지 시 |
| [`assets/*.tmpl`](assets/) | 노트 생성 (Step 5) |

## 멱등성 (Idempotency)

- init 모드를 두 번 실행하면 → 두 번째는 자동으로 update 모드로 전환
- update 모드를 변경 없이 재실행하면 → "변경 없음" 출력 후 종료
- dry-run은 부작용 없음

## 확장 (이번 버전에 포함되지 않은 것)

- 여러 vault 동시 지원 (현재는 단일 vault)
- PARA가 아닌 vault 레이아웃 (Zettelkasten 등)
- vault → 코드 역방향 sync
- Obsidian plugin과의 직접 통합 (Dataview, Templater 등)

## 검증

스킬 작성 후 다음 순서로 검증:

```
1. /obsidian-onboard --dry-run         # TIL 프로젝트에서 추출 정확도 확인
2. /obsidian-onboard                   # 실제 노트 6개 생성
3. Obsidian 열어서 그래프 뷰 + 링크 확인
4. Glossary.md에 도메인 용어 1개 직접 추가
5. /obsidian-onboard --update          # HUMAN 영역이 보존되는지 확인
```
