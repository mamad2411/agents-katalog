---
name: autonomous-loop
description: Use when a set-up project (project/BRIEF.md approved, PROFILE/STATE/backlog present) should continue building autonomously — orchestration of CEO/PO/DEV/REVIEWER cycles with parallel agents, without user input. Also for resuming after an interruption or handoff.
model: opus
disallowed-tools: AskUserQuestion
---

# Autonomous Delivery Loop

## Principle
The loop orchestrates roles as subagents and works without user input until the MVP gate,
an escalation criterion, or context pressure. The core contract in `project/BRIEF.md` is the
constitution; `project/STATE.md` the single state store.

## Cycle (repeat)

1. **Sync:** read `STATE.md`; increment the cycle counter (basis for cooling-off) and check it against the cycle cap — cap reached → runaway stop (see stop conditions), no further cycle. Incorporate open merges, blockers, review results.
2. **CEO tick** (inline per `role-ceo`): activate next WORK items up to the WIP limit, evaluate gates. No new reason → no reprioritization.
3. **PO step** (per `role-po`): cut activated items into cards — with acceptance criteria, claim limits, and **disjoint claim zones**. Idea triage via `project/IDEAS.md`.
4. **DEV fan-out (parallel):** one DEV subagent per card, all in **one** invocation block. **Embed context instead of having it read**: the WORK card and profile extract (commands, quality rules) are verbatim in the prompt — the subagent only reads its role skill. **Model choice by card complexity:** S/M → `sonnet` (very large diff or wide context → `sonnet[1m]`); L or "sensitive" → `opus`. These override the subagent's own `model` field (the role skills carry `inherit` precisely so the spawn decides). The orchestrator verifies the rating before spawning: risk-regex hits in the claim zone, gate relevance, or security/concurrency aspects override a lower PO rating upward — never downward. Zones not safely disjoint or > 2 parallel DEVs → worktree isolation per agent. Parallel DEVs run only targeted tests of their zone plus a regression check of the foundation modules — the full suite run belongs to the orchestrator after the merge (otherwise everyone tests against half-finished neighbor zones).
5. **Review pipeline (risk-based):** as soon as a DEV finishes, start a reviewer subagent per `role-reviewer` — don't wait for the slowest card. **Full review** (gate-relevant → `opus`, otherwise `sonnet`) for: production code, gate packages, risk-regex hits in the diff, or included status claims. **Light review** (`haiku`) for trivial packages (tests/docs only, small diff): zone check, acceptance check, targeted tests, compact claim audit — without pattern spot-check.
6. **Fix loop:** findings/`BLOCKED` → targeted fix run (same card, same zone). **Max. 2 attempts per blocker**, then the autonomy contract applies (escalation or DEFER with ADR). Findings in files **outside all zones** (no-man's-land, e.g. legacy or skeleton tests): never have the DEV fix them along the way — the PO immediately cuts a dedicated fix card with its own zone, which runs before the blocked packages merge.
7. **Merge sequentially:** merge one package after another — before each, the mechanical check per package,
   executed on the package branch with a clean orchestrator tree (commit your own `project/` changes such as
   `STATE.md`/`IDEAS.md` first, so only package changes land in the check):
   `<skills-dir>/_shared/scripts/merge-check.sh <base> --zone <card-zone>… --allow project/backlog/<WORK-NNN>.md --allow project/PROFILE.md --test-cmd "<full test from PROFILE>"`
   — `<skills-dir>` is the installation location of these skills (project-local `.claude/skills/`, global `~/.claude/skills/`, or the plugin root when installed via `/plugin install`).
   **No broad `--allow project/`:** that would wave through DEV changes to `STATE.md`, `BRIEF.md`, or `IDEAS.md`.
   Allowed are only the package's own card (evidence) and `PROFILE.md` (command maintenance);
   for special cases the check knows `--deny` (overrides zone and allow).
   `FAIL` blocks the merge hard (zone violation → finding + fix card; red suite → fix loop) — no discretion.
   The **full suite runs exactly once per package: here, via the check** — DEV and reviewer only test targeted, duplicate runs are cut. Card to DONE incl. evidence, update `STATE.md`.
8. **Collect ideas:** transfer `IDEAS`/`FOLLOW-UP` from all DEV outputs to `project/IDEAS.md` — record only; evaluation happens in the PO step of the **next** cycle (cooling-off).
9. **Stop check** (see below), otherwise next cycle.

## Focus rules (hard)
- **Value filter:** nothing is built that doesn't strengthen a must-have outcome or passed PO triage as an extension.
- **Cooling-off:** no idea is born and built in the same cycle.
- **Idea-chain rule:** ideas that arise while implementing an extension (second order) are never activated in this project run — only recorded.
- **Extension budget** from the brief is a hard cap per milestone.
- Must-have outcomes beat extensions: as long as a P0 is open, no extension gets activated.

| Rationalization | Reality |
|---|---|
| "The DEV agent is already in that file anyway" | Opportunity is not value. The zone applies; the idea goes into the funnel. |
| "Just this one extension, then MVP" | That's how idea-upon-idea starts. Budget and P0 rule apply. |
| "The review takes too long, I'll merge directly" | Unverified claims are the most expensive shortcut. Keep the pipeline. |
| "I'll quickly ask the user, it's just a small thing" | The autonomy contract applies: decide, log, continue. |

## Escalation to the user (only reasons to interrupt)
Exactly the criteria from the autonomy contract in `project/BRIEF.md`:
core-contract change needed · money/accounts/deployment/publishing · legal/security gray area ·
blocker after 2 attempts. Escalation = compact decision memo (situation, options, recommendation), not a log dump. **You have no `AskUserQuestion` tool**: emit the memo and end the turn — a background or scheduled run has no one to answer a prompt; the user replies next turn, when the restriction lifts.

## Retro at the milestone/MVP gate (mandatory before the report)
Distill max. **3–5 learnings** — each: rule in one sentence, why (evidence), application. Sources:
review findings, blockers, revised ADRs. Project-specific ones go to `project/LEARNINGS.md`;
generalizable ones additionally as their own file into the global knowledge base
(resolve: `$SKILLS_KNOWLEDGE_DIR` if set, otherwise the path in `<skills-dir>/_shared/knowledge.path`
— written by install.sh, points to the master repo; if neither resolves → project-local only;
format see its README).
No running log, no duplicates of rules already codified in skills — distillate only.

## Stop conditions
- **MVP gate:** all must-have outcomes proven by review verdicts → retro, then final report (see below), then stop. No further work on extensions without a new assignment.
- **Escalation criterion met** → decision memo to the user.
- **Runaway guard:** cycle cap from `STATE.md` reached (default 15 per milestone) → stop with a decision memo: what is done, what is stuck, why it doesn't converge; options: raise the cap, cut scope, DEFER. The cap is never raised silently — not even by "just one" cycle. Deliberately no token budget: not measurable, would be pseudo-mechanics.
- **Context pressure:** write a handoff per `_shared/templates/HANDOFF.template.md` (incl. open worktrees/branches), finish cleanly. Resume: this skill, step 1.

## Output discipline
No chat narration during cycles; the history lives in `project/log/` and `STATE.md`.
The user receives only: milestone/MVP report, escalation memos, and the final report
(achieved must-have outcomes with evidence, ADRs taken, open POST-MVP ideas, known limits).

## Red flags
- Two DEV agents with overlapping zones and no worktree → merge chaos guaranteed
- `STATE.md` and reality contradict each other → repair the sync first, then continue
- A cycle without a single review → unverified claims, stop
- Extension active while a P0 is open → violation of the focus rules
