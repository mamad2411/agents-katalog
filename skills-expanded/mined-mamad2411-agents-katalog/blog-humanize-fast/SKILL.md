---
name: blog-humanize-fast
description: >
  블로그 초안/최종 원고를 빠르게 보수 윤문하는 병렬 strict 워크플로. humanize-korean
  --strict의 검증 분리(fidelity, naturalness, 잔존 S1/S2 탐지)는 유지하면서 청크
  병렬화로 속도를 줄인다. 트리거: "블로그 최종 윤문", "윤문 빠르게",
  "blog-humanize-fast", "humanize-korean strict 너무 느려", "병렬 strict 윤문",
  "AI 티 줄이되 의미는 건드리지 마", "최종 교열 후 윤문". 아닌 것(negative scope):
  초안 대필·내용 추가/삭제·사실 수정이 아니다 — 문체·리듬·표현만 의미 불변으로
  손본다. 라우팅: 새 글 집필은 blog-prep, 더 깊은 검증·낮은 등급 재검증이 필요하면
  humanize-korean --strict, 맞춤법·오탈자만이면 직접 교정으로 보낸다.
user-invocable: true
---

# Blog Humanize Fast

블로그 최종 원고를 `meaning-preserving` 방식으로 윤문한다. 이 스킬은 초안 작성
스킬이 아니다. 이미 저자가 쓴 한국어 블로그 본문에서 번역투, 기계적 병렬,
관용구, 접속사 남발, 리듬 균일성 같은 AI 티를 보수적으로 줄인다.

## 입력

- 파일 경로: `.md`, `.mdx`, `.txt` 본문 파일.
- 붙여넣은 텍스트: 8,000자 이하 권장.
- frontmatter가 있는 MDX는 가능하면 frontmatter를 제외한 임시 본문 파일을 만들어
  실행한다. frontmatter 필드값은 윤문 대상이 아니다.

## 실행

1. 이 스킬 디렉터리의 `references/quick-rules.md`를 룰북으로 사용한다.
2. Workflow 도구가 있으면 `workflows/blog-humanize-fast.js`를 실행한다.
   - `workflowPath`: `{SKILL_DIR}/workflows/blog-humanize-fast.js`
   - `args`: `{ inputPath, genre: "블로그", intensity: "보수", quickRulesPath: "{SKILL_DIR}/references/quick-rules.md" }`
3. Workflow 도구가 없으면(Codex 등 다른 런타임 포함) 이 스킬은 실행할 수 없다.
   사용자에게 Claude Code에서 실행하라고 명시하고, 현재 런타임에 `humanize-korean`
   스킬이 있으면 그 Fast Path를 대안으로 안내한다. 일반 채팅 답변으로 윤문을
   흉내 내지 않는다.

## 동작 계약

- 의미 불변이 최상위 규칙이다. 사실, 주장, 수치, 날짜, 금액, 고유명사, 직접
  인용, 코드, URL, 마크다운 구조, JSX 태그/속성은 수정하지 않는다.
- YAML frontmatter, 코드펜스(```·~~~), 4칸 이상 들여쓴 indented code 블록은
  보호 청크로 격리해 byte-identical로 보존한다. 청크 사이 원본 개행은 그대로
  두어 재조립이 무변경 시 원문과 동일해야 한다(무결성 게이트).
- 청크별 fidelity 검증이 실패하면 1회만 재시도하고, 다시 실패하면 해당 청크는
  원문으로 롤백한다. 청크 변경률이 50%를 넘으면 fidelity와 무관하게 롤백하고,
  전체 변경률이 30%를 넘으면 경고를 남긴다.
- 전역 naturalness와 잔존 S1/S2 탐지는 별도 축으로 수행한다.
- 표적 수정은 지적 span만 대상으로 1라운드만 수행하고, 수정본은 fidelity
  게이트를 통과할 때만 채택한다(실패 시 수정 전 본문 유지).
- 결과는 자동 반영하지 않는다. 최종본, 변경 통계, residual count를 보고하고
  사용자가 수락할 때만 원문 파일에 반영한다.

## 폴백

- Workflow 실행 실패, quick-rules 읽기 실패, 모델 subcall 실패 원인은 그대로
  보고한다.
- 사용자가 더 정밀한 검증을 요구하거나 결과 등급이 낮으면 `humanize-korean
  --strict`로 재검증하라고 안내한다.
