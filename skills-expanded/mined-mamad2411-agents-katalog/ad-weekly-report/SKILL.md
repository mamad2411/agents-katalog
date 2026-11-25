---
name: ad-weekly-report
description: "Use when the user invokes $ad-weekly-report, ad weekly report, /ad:weekly-report, or asks for a DEV2 weekly work report."
---

# `$ad-weekly-report`

`/ad:weekly-report`의 Codex `$` alias다. 실제 절차의 source of truth는 team2 하네스 command 파일이다.

## 실행 절차

1. `TEAM2_HARNESS_PATH="${TEAM2_HARNESS_PATH:-/Users/jm/Documents/workspace/team2}"`로 기준 경로를 잡는다.
2. 반드시 `$TEAM2_HARNESS_PATH/.claude/commands/ad/weekly-report.md`를 먼저 읽고 그 절차와 운영 기준을 따른다. 포맷·일정정보 방향·핵심목표 취합 규칙은 그 파일과 `docs/sprint/weekly-report-guide.md`가 SoT다 — 여기 복제하면 한쪽이 낡는다.
3. command 파일이 참조하는 스프린트, 주간업무, YouTrack, 로컬 위키 컨텍스트만 추가로 확인한다.
4. 보고서 작성은 자동으로 할 수 있으나 YouTrack 티켓/지식베이스(KB)/로컬 위키 변경은 사용자 승인 후 실행한다.

## 기록 대상 필터

대상 선별은 SoT를 읽기 전에도 이 표를 따른다. 아래는 command 파일에서 생성된 블록이다 — 직접 고치지 말고 SoT를 고친 뒤 `python3 tools/lint_harness_rules.py --sync-generated`.

<!-- generated:weekly-report-filter source=.claude/commands/ad/weekly-report.md -->
| 항목 | 포함 여부 |
|------|----------|
| Type=Feature/Epic, 개발자 담당, 대상 월 스프린트 일치 | 포함 |
| Type=Feature/Epic, 기획자/디자이너 담당, 개발자 하위 Task 있음 | 부모는 컨텍스트로 포함, 개발자 Task만 본문 표기 |
| Type=Feature/Epic, 기획자/디자이너 담당, 개발자 하위 Task 없음 | 제외 |
| Type=Feature/Epic, Backlog | 제외 |
| Type=Feature/Epic, 대상 월 스프린트 불일치 | 제외 |
| Type=Feature, 사업부 작성 운영 (예: 멀티캠퍼스 IF) | 개발자 담당 + 대상 월 스프린트 일치 시 검토 후 포함 |
| Type=Task, 사업부 단발 운영 요청 | 제외 |
| Type=Bug, 단발 장애/점검 | 제외 |
<!-- /generated:weekly-report-filter -->
