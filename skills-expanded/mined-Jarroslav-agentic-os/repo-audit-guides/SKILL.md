---
name: repo-audit-guides
version: 0.1.0
author: agentic-os
allowed-tools: [Read, Glob, Grep, Bash]
description: Read-only audit of a repository's documentation, structure, and agentic assistant setup, run before knowledge planting so the downstream repo-guides workflow knows how to handle every pre-existing doc and assistant surface. Invoke when the user asks to survey, audit, inspect, assess, or review repo docs, assistant instructions, Claude / Codex / Gemini / GitHub Copilot setup, subagents, skills, hooks, AGENTS.md, CLAUDE.md, GEMINI.md, or whether a repository is ready for knowledge planting. Produces a structured readiness report, never a numeric grade, and never writes. Not for: writing or fixing anything it finds (repo-guides plants knowledge afterwards), numeric grading, or auditing application-code quality.

---

# Repo Audit Guides

Survey what a repository already tells its coding agents, then hand the next step a per-surface plan. This is the audit that runs before **knowledge planting** — the later `repo-guides` foundation step that installs factory-owned guidance under `.agentic/guides/`. You look, you reason, you report. You do not touch anything.

> This is a readiness analysis, not a report card. Abstract quality scoring is banned: no letter grades, no 1-10, no "documentation health: 72%". Every claim rides on cited evidence and resolves to one concrete foundation action.

## When to use

Trigger on requests to survey / audit / inspect / assess / review:

- repo documentation, README, CONTRIBUTING, `docs/`, ADRs, runbooks, architecture or onboarding material;
- assistant instructions and entrypoints — `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`;
- Claude Code / Codex / Gemini / GitHub Copilot / Cursor setup;
- assistant assets — commands, skills, subagents, hooks, settings, prompts, memory files;
- whether the repo is **ready for knowledge planting** / foundation.

## Blast radius

**R0 — read-only.** You inventory and report; you never write run artifacts, repo files, or external side-effects. Nothing you do requires a gate because nothing you do mutates state.

## Read-only contract

Strictly non-mutating. You MUST NOT:

- write, create, or edit guides, entrypoints, configs, hooks, settings, or any file;
- install, publish, push, open PRs, or run migrations / formatters / test suites / package installs;
- mutate caches or lockfiles;
- run any destructive command.

Allowed shell is inspection only: `pwd`, `find`, `rg`, `ls`, `sed -n`, `wc -l`, and **read-only** git (`git status`, `git branch --show-current`, `git log`, `git diff --name-only`). Narrow noisy commands before running them; adapt every path to what actually exists in the tree.

## Scoping rules

**`.agentic/` is ignored by default.** Pre-existing `.agentic/` and `.agentic/guides/` state is NOT inventoried and NOT rated — unless one of these holds:

1. the user explicitly asks you to audit agentic-sdlc artifacts, or
2. an assistant entrypoint references `.agentic/`.

When it is in scope, treat it as **pre-existing generated guidance**: inventory it as evidence, weigh it against the other docs, and flag it if it is stale, conflicting, or non-portable. Never treat it as authoritative by default.

> These outputs come from earlier factory runs. Presuming they exist, or that they are the source of truth, would bias the whole audit. Start from the assumption they do not matter, and let the evidence change your mind.

**Markdown triage.** When many `.md` files exist, classify each by purpose — overview, setup, architecture, ADR, API, testing, release, operations, assistant instruction, generated guidance, external doc reference — rather than dumping them into generic buckets. For a link-only file, record the destination and whether it is local, external, missing, or ambiguous.

**Topic scoping.** Cover the concrete topics the repo actually carries: architecture, setup, commands, testing, quality gates, release, security, API, data, workflows, integrations, contribution process. Omit a topic that is absent — unless its absence itself blocks foundation, in which case name the gap.

## Inputs

| Input | Source |
| --- | --- |
| Audit request + any scope hints | The user (e.g. "audit our assistant setup", "are we ready to plant?") |
| Repository tree | The current working directory |
| Rubric, exemplars, standards, conflict taxonomy, recommendation map | `references/` (see below) |

## Watched paths

Look for these first; they carry the highest signal:

```
.agentic/   .agentic/guides/   AGENTS.md   CLAUDE.md   GEMINI.md
.github/copilot-instructions.md
.claude/   .codex/   .agents/   .gemini/   .copilot/   .cursor/
README.md   CONTRIBUTING.md   SECURITY.md   docs/
settings*.json   .claude/skills/
```

## Workflow

Nine steps, in order. Steps 5-8 lean on the bundled `references/` tree.

1. **Confirm root.** Run `pwd`; make sure you are auditing the intended repository.
2. **Inventory repo + docs.** Map manifests, modules, and source dirs; enumerate documentation-bearing files and triage the `.md` set by purpose.
3. **Inventory assistant entrypoints.** Find the entrypoint files and per-tool config dirs above.
4. **Inventory agentic assets.** Enumerate commands, skills, subagents, hooks, settings, prompts, memory files, and any managed / generated regions.
5. **Assess quality against the rubric.** Apply `references/audit-rubric.md` for finding labels; judge docs against `references/doc-standards.md` and assistant surfaces against `references/agent-surface-standards.md`.
6. **Compare against exemplars.** Calibrate the observed setup against the graded profiles in `references/setup-grades.md`.
7. **Detect conflicts.** Sweep for contradictory guidance using `references/conflict-patterns.md`.
8. **Map findings to recommendations.** Convert each finding into a foundation action using `references/planting-advice.md`.
9. **Emit the report.** Produce the structured report defined below.

### Discovery commands

Read-only inspection only; paraphrased intent — adapt paths and narrow before running.

| Intent | Shape |
| --- | --- |
| Confirm root | `pwd` |
| Root entrypoints + docs | `find` depth-3 for the entrypoint/doc filenames, excluding `node_modules` |
| All markdown | `find` depth-5 for `*.md`, excluding `node_modules` and `.git` |
| Tool config dirs | `find` depth-4 over `.claude .codex .agents .gemini .copilot .cursor .github docs` |
| Asset paths | `find` depth-6 for `*/skills/* */agents/* */commands/* */hooks/* */prompts/*`, `settings*.json`, `copilot-instructions.md` |
| Keyword sweep | broad `rg -n` for approval / test / lint / build / branch / commit / subagent / hook / managed region / source of truth across entrypoints, docs, and tool dirs |
| Git state | `git status --short`; `git log --oneline -10` |
| Conditional `.agentic/` pass | `find .agentic -maxdepth 4 -type f | sort` + targeted `rg` for quality / workflow / approval keywords |

## References

Bundled, relative to this skill directory.

| File | Supplies | Used in step |
| --- | --- | --- |
| `references/audit-rubric.md` | Grading rubric — setup finding labels | 5 |
| `references/doc-standards.md` | Documentation quality standards | 2, 5 |
| `references/agent-surface-standards.md` | Standards for assistant entrypoints, skills, and subagents | 3, 4, 5 |
| `references/setup-grades.md` | Three graded exemplar profiles (strong / partial / weak) in one doc | 6 |
| `references/conflict-patterns.md` | Contradictory-guidance patterns to flag | 7 |
| `references/planting-advice.md` | What to recommend before knowledge planting | 8 |

> The exemplar profiles calibrate *your judgment*; they are not scores you stamp on the audited repo. Grounding holds throughout — never assert a fact the tree does not show.

## Evidence discipline

Cite `path:line` wherever possible. Where a line reference is impossible, say why and cite the read-only command whose output backs the claim instead. Ground every statement — do not invent structure, rules, or history the repository does not actually contain.

## Decision vocabulary

Every table verdict draws from one shared enum.

**Foundation action** — `preserve|incorporate|merge|replace|skip|ask user|halt`

| Action | Meaning |
| --- | --- |
| `preserve` | Existing docs stay the direct source of truth for agents. |
| `incorporate` | Existing docs are source material to be converted / mapped into factory-owned guidance; the originals are not the long-term target. Your next step MUST name which docs are source material, which factory-owned guidance absorbs them, and whether the originals stay authoritative, become legacy, or remain tool-specific. Never recommend editing originals in place when foundation owns the result. |
| `merge` | Only when existing content and the foundation target are the same authority surface, or a compatible managed-region / guide target. |
| `replace` | Stale generated content or stale references. |
| `skip` | Absent or irrelevant areas. |
| `ask user` | Authority is unclear, or multiple valid setup paths exist. |
| `halt` | Proceeding would bake in an unsafe, destructive, approval-bypassing, or contradictory setup. |

Supporting enums:

- **Authority** — `authoritative|secondary|unused|unclear|conflicting`
- **Evidence confidence** — `high|medium|low`
- **Freshness signal** — `current` / `stale` / `unknown`, each with evidence.

## Report contract

Emit exactly these top-level sections, in this order:

```
# Repo Knowledge Audit
## What we found
## Where the docs live
## How usable the docs are
## Assistant instruction files
## Agents, skills and hooks
## Where they disagree
## Ready to plant?
## Evidence
```

### What we found

3-6 bullets covering: repo type; whether the docs are usable for foundation; which assistant setup is authoritative; the highest-risk conflicts or stale surfaces; and the recommended overall foundation action.

### Table column contracts

Use these headers verbatim.

- **Where the docs live**

  `| Path or group | Purpose | Freshness signal | Foundation use |`

- **How usable the docs are**

  `| Topic | Current source | What is reliable | Gaps or stale areas | Foundation action |`

- **Assistant instruction files**

  `| Surface | Role observed | Authority | Problems | Foundation action |`

- **Agents, skills and hooks**

  `| Asset group | Inventory | What it does | Alignment with docs | Foundation action |`

- **Where they disagree**

  `| Conflict or overlap | Evidence | Impact on foundation | Required decision |`

- **Ready to plant?**

  `| Area | Finding | Foundation action | Next step |`

- **Evidence**

  `| Claim | Evidence | Confidence |`

The **Foundation action** column uses the full enum `preserve|incorporate|merge|replace|skip|ask user|halt`. The Conflict table's **Required decision** column uses the subset `preserve|incorporate|merge|replace|ask user|halt` (no `skip`).

### Agents, skills and hooks — flag list

Flag any of these:

- assets already supporting foundation;
- assets pointing at stale guide trees;
- assets duplicating or competing with agentic-sdlc;
- hooks or settings able to write, install, publish, push, create PRs, or run destructive commands.

### Where they disagree — priority list

Rank conflicts by:

1. source-of-truth disputes;
2. test / lint / build / commit / branch / release / PR command conflicts;
3. approval expectations and write safety;
4. competing agents / skills / commands / prompts;
5. malformed or stale generated regions.

List only concrete findings. If there are none, say so plainly.

## Outputs

A single Markdown readiness report matching the contract above. Its per-surface action verdicts are the deliverable: the downstream `repo-guides` knowledge-planting workflow reads them to decide how it handles each pre-existing doc and assistant surface.

## Non-goals

- Never writes, edits, installs, publishes, or runs mutating / destructive commands; no test / lint / build execution.
- No auditing of `.agentic/` state unless explicitly requested or referenced by an entrypoint.
- No abstract quality grades; no report-card scoring.
- Not a fixer — it recommends foundation actions, it does not perform them.
