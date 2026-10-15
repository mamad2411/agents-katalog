---
name: mols-kanban-markdown
description: >
  USE WHEN: managing, creating, initializing, updating, moving, or validating Kanban board items using markdown cards. Target directory initialization (.configs, backlog, active, archive), frontmatter schema validation, card status directory migration, and link correction.
  EXCLUDES: general software development, non-Kanban documentation edits, or raw markdown formatting without Kanban context.
argument-hint: "[<kanban_path>] [initialize | validate | validate-directory | move | --help]"
user-invocable: true
disable-model-invocation: false
compatibility: "Requires Python >=3.13, rumdl, pyromark, pyyaml"
---

# Mols Kanban Markdown

## Goal

Provide standard routing and setup delegation for managing markdown-based Kanban boards.

## Instructions

### Delegation Model

1. **SKILL.md**는 칸반 조작에 대한 상세 지침을 명시하지 않고, 데이터 경로 내에 위치하는 **`AGENTS.md`**로 동작 지침을 완전 위임합니다.
2. **`AGENTS.md`**는 칸반 카드의 프런트매터 구조 및 작성을 **`.configs/config.jsonc`**와 **`.configs/template.md`**에 명시된 규칙으로 위임하여 작동합니다.
3. 세부 스크립트 실행 및 기술적 검증 로직은 **`workflows/`**로 위임합니다.

### Completion

Report verification status, updated card paths, and status transitions.

## Workflow: Router

### Context

#### Parameters

- **Target Path**: Kanban board directory path.
- **Workflow Route**: Sub-workflow file ID selected from `workflows/INDEX.csv` (e.g., `help.md`, `validate.md`, `initialize.md`, `validate-directory.md`, `move.md`).

### Procedure

1. If `--help` or `help` argument/trigger is provided, resolve to `help.md` and load `workflows/help.md`.
2. Otherwise, read `workflows/INDEX.csv` once to evaluate `use_when` conditions.
3. Select the matching workflow file (e.g., `validate.md`).
4. Load `workflows/<id>` and execute its procedure.
