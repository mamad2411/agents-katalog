---
name: subagent-mission-brief
description: Control Tower support skill for writing clear operational mission briefs for subagents, temporary mission roles, delegated reviews, verification gates, and scoped implementation handoffs.
user-invocable: true
allowed-tools:
  - Read
  - Bash(git *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(rg *)
  - Bash(jq *)
---

# Skill: Subagent Mission Brief

## Purpose

Use this skill when Control Tower delegates non-trivial work to a subagent and
needs a concise operational assignment instead of a broad prompt.

The brief defines authority, focus, scope, tools, stop conditions, expected
output, and handoff target. It does not create a new workflow stage.

## When to Use

- Architecture, security, backend, frontend, QA, docs, or product analysis
- Large file inspection or broad review
- Independent verifier or reviewer gates
- Scoped implementation with an approved write-set
- Tasks where output is large enough to keep out of the main chat
- Any temporary mission role that needs clear boundaries

## When to Skip

- Trivial local tasks where delegation adds overhead
- One-line checks or simple status commands
- Discussion-only turns
- Tasks already covered by a precise Work Block and no subagent is needed

## Mission Brief Structure

Use this compact structure:

- Base Role:
- Mission Role:
- Skill(s):
- Objective:
- Context:
- Scope:
- Out of scope:
- Inputs / files to read:
- Allowed tools / MCP:
- Approved write-set:
- Side-effect class:
- DB action mode:
- Parallel group:
- Sibling streams:
- Model / reasoning:
- Hard stops:
- Required checks:
- Verification evidence:
- Expected output:
- Acceptance owner:
- Handoff target:

Template: `docs/templates/subagent-mission-brief-template.md`

## Prompting Rules

- Be specific and direct.
- Separate context from instructions.
- Define the output format.
- Give only necessary context.
- Do not ask the model to reveal chain-of-thought.
- Do not overload subagents with unrelated files.
- Give one clear responsibility per subagent.
- Limit tool access to what the task needs.
- Treat subagent completion as evidence, not acceptance.
- Tell the subagent to report only from its assigned base role and mission role.
- Tell the subagent not to infer orchestration mechanics. If asked whether it
  ran through native subagent tooling, fallback, fork, or inline execution, it
  must answer `not assessed` unless Control Tower explicitly provided that fact.
- For DB, deploy, infra, secret, or client-facing tasks, state the
  side-effect class and DB action mode from `AGENTS.md`.
- Inherit model/reasoning by default unless a task-specific override is needed;
  record the reason if you request an override.
- Prefer official or primary sources for external research.
- If a tool, MCP, or external source is unavailable, continue with local
  analysis and report the limitation.

## Temporary Mission Roles

Base role controls authority: Orchestrator, Coder, Reviewer, or Verifier.
Mission role controls focus: Architecture Analyst, Tech Lead, Security Analyst,
Backend Coder, QA Analyst, Docs Analyst, Release Ops, or another task-specific
specialization.

Temporary mission roles do not expand file authority. A `Reviewer / Security
Analyst` remains read-only. A `Coder / Backend Coder` may write only inside the
approved write-set.

## Allowed Tools / MCP

List only tools the subagent needs. Examples:

- Repository reads: `rg`, `sed`, `git diff`, `git status`
- Verification: project check commands from the Work Block
- External docs: official vendor docs, primary GitHub repos/issues/releases
- MCP: only when available and useful for the mission

Tool capability does not grant process authority. Production APIs, credentials,
deploys, live DB migrations, destructive git operations, and real client
communications still require Owner approval.

## Side-Effect and DB Boundaries

Use `AGENTS.md` as the canonical authority source. For any mission touching DB,
infra, deploy, secrets, or real client communications, include:

- `Side-effect class`: one class from `AGENTS.md § Side-Effect Classes`.
- `DB action mode`: one mode from `AGENTS.md § DB Access Matrix`, or `none`.

If the required class or DB mode is unclear, the subagent must stop and report
the ambiguity instead of assuming permission.

## Parallel Context

For non-trivial Work Blocks, link each mission brief to the Stage 0 Parallel
Decomposition Matrix:

- `Parallel group`: e.g. `Gate B review`, `Docs cleanup`, `Backend slice`.
- `Sibling streams`: other agents or local streams running at the same time.
- `Dependencies`: what must finish before this result can be accepted.

If the task is intentionally local or sequential, state why: write conflict,
dependency chain, shared runtime, hard-stop boundary, uncertain scope, or no
delegation value.

## Approved Write-Set

For read-only missions, write:

`Approved write-set: none. Read-only.`

For implementation, list exact paths or path patterns. Use one write-capable
Coder per write-set. Do not delegate broad repo write access.

## Stop Conditions

Tell the subagent to stop and report if:

- Scope expansion is required.
- A hard stop from `AGENTS.md` is reached.
- Required files or tools are unavailable.
- Verification fails in a way that affects acceptance.
- Secrets, credentials, or risky production config are encountered.
- Unrelated dirty files block the task.

## Expected Output

Ask for a compact result that Control Tower can act on:

- Verdict
- Files inspected or changed
- Findings or implementation summary
- Checks run and result
- Verification evidence
- Risks / blockers
- Recommended next action

For reviewers, findings come first and are ordered by severity.

## Acceptance Boundary

A subagent result is not accepted just because the subagent returned `DONE`.
Control Tower accepts the result only after checking:

- scope and write-set compliance
- acceptance criteria coverage
- required evidence/checks
- declared risks and deferred work

Verifier results use the verdict language from `sdd-protocol.md`.

## Subagent Self-Report Boundary

Subagents report their assigned mission only. They must not:

- present themselves as Control Tower unless assigned that base role;
- judge whether orchestration used native `spawn_agent`, fallback, or another
  runtime path;
- infer, speculate about, or self-certify native/fallback execution mode. If
  this appears in the expected output, write `not assessed` unless Control
  Tower explicitly provided the orchestration fact;
- evaluate platform/tool availability outside their mission;
- launch nested external AI CLI tools such as `codex`, `claude`, Gemini,
  DeepSeek, Qwen, or similar reviewers unless explicitly assigned as an
  `External Audit Runner`;
- accept their own output as final project acceptance.

Control Tower owns orchestration mechanics, acceptance, and final consolidation.

## Codex and Claude Code

Use the same mission brief shape for Codex, Claude Code, or a manual fallback
prompt. Runtime mechanics may differ, but the contract stays the same:
authority comes from base role, focus comes from mission role, and hard stops
remain Owner-gated.

## Handoff

- **Success condition**: Control Tower can merge the subagent result into the
  current SDD stage without asking follow-up questions.
- **Next**: Control Tower consolidates results and proceeds through the active
  Work Block.
- **Auto-proceed**: 🟢 YES inside approved scope.
- **Hard stop**: 🔴 YES for `AGENTS.md` hard stops or unavailable required
  authority.

## Examples

### Architect / Tech Lead Discovery

Base Role: Reviewer  
Mission Role: Architecture Analyst / Tech Lead  
Skill(s): `architecture-discovery` if the task needs research  
Objective: Identify the safest architecture boundary for the proposed module.  
Context: Use the active Work Block and existing repo conventions.  
Scope: Relevant docs, routes, schemas, and integration points only.  
Out of scope: Code edits, package changes, migrations, deploys.  
Inputs / files to read: list exact files or directories.  
Allowed tools / MCP: read-only repo tools; official docs if needed.  
Approved write-set: none. Read-only.  
Parallel group: Architecture discovery.  
Sibling streams: none unless Stage 0 matrix says otherwise.  
Model / reasoning: inherit by default; use higher reasoning if available.  
Hard stops: credentials, live APIs, live DB, destructive git, scope expansion.  
Required checks: direct file inspection; cite exact paths.  
Verification evidence: exact files/docs inspected and source links if used.  
Expected output: architecture options, recommended boundary, risks, next Work Block.  
Acceptance owner: Control Tower.  
Handoff target: Control Tower Stage 0.

### Reviewer

Base Role: Reviewer  
Mission Role: Backend Reviewer  
Skill(s): relevant project-local skill if triggered  
Objective: Review the implementation diff against acceptance criteria.  
Context: The Work Block defines scope and expected behavior.  
Scope: Changed files and directly affected contracts.  
Out of scope: New implementation, unrelated refactors, production deploys.  
Inputs / files to read: `git diff`, tasklist, changed source files.  
Allowed tools / MCP: read-only repo tools.  
Approved write-set: none. Read-only.  
Parallel group: Review gate.  
Sibling streams: verifier or docs sync only if independent.  
Model / reasoning: inherit by default.  
Hard stops: missing critical context, unexpected risky files, scope drift.  
Required checks: inspect AC coverage and write-set compliance.  
Verification evidence: file/line findings and diff references.  
Expected output: findings first, severity ordered, with file references.  
Acceptance owner: Control Tower.  
Handoff target: Control Tower Stage 2a.

### Verifier

Base Role: Verifier  
Mission Role: QA Analyst  
Skill(s): verifier or contract skill if triggered  
Objective: Verify that the accepted checks pass and behavior matches the Work Block.  
Context: Use the implementation summary and acceptance criteria.  
Scope: Changed files, required checks, and relevant runtime smoke only.  
Out of scope: Code edits unless explicitly approved, deploys, live migrations.  
Inputs / files to read: tasklist, diff, changed files, check commands.  
Allowed tools / MCP: required verification commands; read-only inspection.  
Approved write-set: none. Read-only.  
Parallel group: Verification gate.  
Sibling streams: none if checks share runtime resources.  
Model / reasoning: inherit by default.  
Hard stops: failing required check, unsafe external side effect, missing required tool.  
Required checks: list exact commands from the Work Block.  
Verification evidence: commands, outputs summarized, and residual risk.  
Expected output: APPROVED / NEEDS_CHANGES / BLOCKED, evidence, residual risks.  
Acceptance owner: Control Tower.  
Handoff target: Control Tower Stage 2b.
