---
name: team-security
description: "Full security cycle: threat-model refresh → security-audit (code) → dependency-audit → harden (perimeter/containers) → optional pentest of the project's own app → consolidated report and stories. Use before release or after adding auth/payments/uploads/multiplayer."
argument-hint: "[full | pre-release] [--pentest]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Task, Skill, AskUserQuestion
model: opus
---

# Team: Security

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

File writes and any mutation (git, deploy) happen only after an explicit "May I write?" / "Proceed?" — each one `AskUserQuestion` (proceed (Recommended) · show the draft/diff first · not now) → "yes". After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker). A partial report on BLOCKED at any stage is mandatory.

**Consent for delegated work is collected by this skill.** A subagent spawned through `Task` cannot ask the user. Before each `Task` batch, the "Proceed?" question names the agents and the files each will create or change (audit reports, threat-model updates); that answer covers those files. A delegated step that needs to go beyond its brief (another file, a code or configuration change, a production mutation) stops and reports it, and the parent asks.

Commands are `/web-studio:<name>` in plugin mode and `/<name>` in copy mode. **This skill runs the other studio skills through the `Skill` tool**, one after another; each called skill keeps all of its own phases and gates (its "May I write?" and commit gates included), and its verdict comes back as text this skill quotes in Phase 4. `‖` below means one `Task` batch of agents launched together — never two skills at once. Agents are spawned with a studio `subagent_type`: `web-studio:<name>` in plugin mode, `<name>` in copy mode (coordination-rules § Subagents). In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

**Mode** (argument, default `full`): `full` runs every phase; `pre-release` skips the threat-model refresh of Phase 1 step 2 and `/harden` in Phase 2 — it runs `/security-audit quick` → `/dependency-audit` and consolidates for `/release-checklist`, naming the skipped steps in the report; `--pentest` adds Phase 3 in either mode.

## Phase 1: Threat model
1. **Code to audit.** The cycle audits code: source files of the configured stack outside `docs/`, `production/` and `.claude/` (`git ls-files`, technical-preferences → Stack). None — a project still in discovery or specification → stop: `BLOCKED (no code to audit — run /threat-model for the design, /dev-story for the first story)`, nothing written, no audit started. `--pentest` on a project without a running dev/staging environment → the pentest phase is skipped and named in Phase 4, the rest of the cycle runs.
2. `/threat-model` through the `Skill` tool (refresh for new surfaces; it keeps `docs/architecture/threat-model.md`, the kit's one threat-model file); its verdict is quoted. `HIGH RISK (N unmitigated)` counts as at least `CONCERNS` in the Phase 4 verdict — a cycle never ends `PASS` while the threat model names an unmitigated high risk.

## Phase 2: Audits, one after another
Through the `Skill` tool, in this order: `/security-audit full` (it spawns `appsec-engineer`) → `/dependency-audit` → `/harden` (it spawns `network-security-engineer`). Then one `Task`: `graphql-engineer` — GraphQL checklist (if applicable). Each verdict is recorded for Phase 4; a `FAIL` does not stop the sequence — the cycle collects every finding before it consolidates.

## Phase 3: Dynamic (`--pentest`)
`/pentest` through the `Skill` tool, on dev/staging within the agreed scope (the scope is the called skill's own gate).

## Phase 4: Consolidation
1. One deduplicated findings list: the same weakness reported by two audits (same file:line, same CWE or the same dependency) is one row that names both sources — a duplicate is merged, never listed twice and never dropped; priorities; stories for BLOCKING/High (through `/create-stories`, the next step); the threat-model statuses to update; the release-gate verdict.
2. Render the list, then "May I write the consolidated rows into `production/findings.md` and the status updates into `docs/architecture/threat-model.md`?" — one `AskUserQuestion`: write (Recommended) · show the draft/diff first · not now. After the "write" answer: `touch .claude/.write-consent`.
3. **Commit gate** (rule 7 (4), `.claude/docs/git-workflow.md` § Documents), recorded before it is asked — `<hooks>session-state.sh set Gate "/team-security Phase 4: commit?"` — and cleared after the answer (`<hooks>session-state.sh set Gate "—"`), so an open gate survives the next turn; one `AskUserQuestion`: `docs: security cycle YYYY-MM-DD` staging exactly the written files and `.claude/agent-memory/` when the run changed it (git-workflow § Agent memory) — on the default branch when no story work is in progress; when HEAD is a story branch, name it and offer: switch to the default branch and commit there (Recommended — a pipeline-wide document) · commit here (the cycle belongs to this story) · leave uncommitted. Code, configs, workflows and scripts a called skill changed never ride the `docs:` commit — name them and offer the chore lane (git-workflow § Chore / infra). Nothing is committed without the answer.

Verdict: `PASS` | `CONCERNS` | `FAIL` | `BLOCKED (no code to audit — …)`. Next step — one `AskUserQuestion`: `/create-stories` for the fixes (Recommended) · a repeated `/security-audit quick` · report only.
