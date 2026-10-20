---
name: skill-test
description: "Validates Web Studio skills and agents: `static` (structural linter), `spec` (behavioural spec evaluation), `category` (rubric metrics), `agent` (agent spec evaluation), `audit` (coverage report), using the testing framework (catalog.yaml, rubric, specs) from the kit or a project copy. Run after editing a skill or agent, for 'lint the skills', 'test skill X', 'coverage of the kit'."
argument-hint: "static [name|all] | spec [name] | category [name|all] | agent [name|all] | audit"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Skill Test

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

Tests the studio's own skills and agents (not the project).

- **Framework directory** — the first of these that contains `catalog.yaml`: `./testing` (kit repository),
  `./web-studio-testing` (project copy), the plugin root's `testing/` (from the session-start "Plugin root:" line or
  `claude plugin list --json`). Spec paths come from the catalog's `spec:` field, never guessed; outside the kit repository the
  `testing/` prefix of that path stands for the framework directory.
- **Sources** — skills: `./skills/*/SKILL.md` (kit repo), `.claude/skills/*/SKILL.md` (copy mode) or the plugin root's
  `skills/`; agents likewise (`agents/*.md`, `.claude/agents/*.md`).
- **Catalog gates are recorded** (rule 7): before each "May I update `catalog.yaml`…?" / "May I write the result…?" question below, `<hooks>session-state.sh set Gate "/skill-test Phase 2X: update catalog?"` (`./hooks/` in the kit repository; otherwise `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode), cleared after the answer with `<hooks>session-state.sh set Gate "—"` — one sentence per gate, so a session that resumes with the question open continues here.

| Mode | What | Cost |
|---|---|---|
| `static [name\|all]` | 9 structural checks of SKILL.md | low |
| `spec [name]` | evaluate a skill against its behavioural spec | medium |
| `category [name\|all]` | category rubric metrics | low |
| `agent [name\|all]` | agent static checks + agent spec evaluation | medium |
| `audit` | coverage: who has a spec, last tested, result | low |

## Phase 1: Arguments
1. Parse mode and target; unknown mode → print the usage (the table above) and stop.
2. Find the framework directory. None found and the mode is not `static` → say that only `static` works without a
   framework, name the directory it looks for, and stop without writing anything.
3. Read the framework's `catalog.yaml` (categories, spec paths, dates). `static` without a framework skips this step.

## Phase 2A: static — 9 SKILL.md checks
1. Frontmatter starts on line 1 with `---`; fields `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools` — FAIL if missing.
2. ≥ 2 phases (`## Phase N` or ≥ 2 `##`) — FAIL.
3. A verdict word (`PASS|FAIL|CONCERNS|APPROVED|ACCEPTED|PROPOSED|NEEDS REVISION|NEEDS CHANGES|BLOCKED|COMPLETE|READY|DONE|UPDATED|CLEAN|RELEASED|DEPLOYED|HARDENED|PLAYABLE|COMPLIANT|INITIALISED|RESOLVED|MITIGATED|WITHIN BUDGET|OVER BUDGET|ON TRACK|AT RISK|OFF TRACK|FIXED|IMPROVED|PLANNED`) — FAIL.
4. Ask-before-write: `May I write` (or an explicit gate sentence) when `Write|Edit` is in `allowed-tools` — FAIL; otherwise WARN. A gate that is not an `AskUserQuestion` with alternatives (coordination-rules, rule 7) — WARN. The gate must be followed by `touch .claude/.write-consent` (the consent-guard hook reads that marker; a skill that writes without touching it warns on every write) — a write gate with no consent touch after it — WARN.
5. A "Next step" at the end — WARN; one that is not offered as an `AskUserQuestion` with alternatives — WARN.
6. A reference/template/rules link (`stack-reference/`, `templates/`, `rules/`) for authoring/analysis skills — WARN.
7. `argument-hint` non-empty and consistent with the argument-parsing phase — WARN.
8. Language: body in English, no project-specific or personal references (hostnames, names, private repo names) — WARN.
9. A "Reply in the project conversation language" line, or a pointer to `coordination-rules.md` § Skill conventions (which defines it once) — the skill honours CLAUDE.md → Language regardless of its own English text — WARN.
Output: a table of checks, `COMPLIANT | WARNINGS | NON-COMPLIANT`; for `all` — a summary table.
**Catalog record** (only with a framework — `static` without one has no catalog and writes nothing): the catalog carries `last_static` / `last_static_result` per skill for exactly this run. After the table, record the gate (`<hooks>session-state.sh set Gate "/skill-test Phase 2A: update catalog?"`), then "May I update `catalog.yaml` (`last_static` = today, `last_static_result` = the verdict, for N skill(s))?" as one `AskUserQuestion`: update the catalog (Recommended) · do not write; clear the gate after the answer. After the "update" answer: `touch .claude/.write-consent` (rule 7), then edit only those two fields of the tested rows; nothing else in the catalog changes. `audit` reads the fields back.

## Phase 2B: spec — behavioural evaluation
1. Read SKILL.md and the spec at the catalog's `spec:` path (`skills/<category>/<name>.md` inside the framework).
2. For every case and assertion, find the instructions in the skill text that satisfy it: PASS/FAIL/PARTIAL with a quoted line.
3. Totals per case and protocol.
4. Record the gate (`<hooks>session-state.sh set Gate "/skill-test Phase 2B: write results and catalog?"`), then "May I write the result to `results/<name>-<date>.md` and update `catalog.yaml`?" as one `AskUserQuestion`: results and catalog (Recommended) · results only · do not write; clear the gate after the answer.
5. After the "write" answer: `touch .claude/.write-consent` (rule 7), then write.

## Phase 2C: category — rubric
The category section of `quality-rubric.md` → each metric PASS/WARN/FAIL with justification; the category's verdict is `COMPLIANT | WARNINGS | NON-COMPLIANT` from the worst metric.
**Catalog record**, as in 2A: record the gate (`<hooks>session-state.sh set Gate "/skill-test Phase 2C: update catalog?"`), then "May I update `catalog.yaml` (`last_category` = today, `last_category_result` = the verdict, for the N skill(s) of the category)?" — one `AskUserQuestion`: update the catalog (Recommended) · do not write; clear the gate after the answer. After the "update" answer: `touch .claude/.write-consent` (rule 7), then edit only those two fields.

## Phase 2D: agent
Static: the agent file exists, `name/description/model/tools`, the collaboration protocol block, a stack-reference link, domain and "never"/escalation described. Then evaluate against the agent's spec at the catalog's `spec:` path (`agents/<tier>/<name>.md`, 5 cases) as in 2B, including its write gate. `all` runs every catalogued agent and ends with a summary table; an agent without a spec is listed as such, never skipped silently.

## Phase 2E: audit
A table of all skills/agents: category/tier, spec present?, last_static/spec/category (date, result), priority. Uncatalogued files listed separately.

Verdict: `COMPLIANT` | `WARNINGS` | `NON-COMPLIANT`. Next step — one `AskUserQuestion`: `/skill-improve <name>` for failures (Recommended) · `/skill-test spec <name>` next · stop here.
