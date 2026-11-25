---
name: know-my-repo
description: >-
  Onboards an agent onto an unfamiliar repository from zero knowledge: deep
  parallel read of the codebase, extraction of the repo's actual conventions
  (each proven by at least two examples), verified build/test/run commands,
  an end-to-end exemplar trace of how a feature is really added, then
  generates the initial knowledge set — AGENTS.md and docs/ARCHITECTURE.md —
  with every fact cited. Nothing is deleted. Use on repositories with no (or
  trivial) agent knowledge files, when the user asks to onboard, initialize,
  understand, or learn a repo, generate a CLAUDE.md/AGENTS.md from scratch,
  or mentions know-my-repo or /know-my-repo.
license: MIT
argument-hint: "[project-root]"
---

# Know My Repo

Day one on a codebase you have never seen — no docs, no notes, no memory,
just code. This skill builds the knowledge set a future agent can load and
be productive from: **read the code, run the commands, cite everything.**

Sibling skills: this one creates knowledge where there is none. Rotten
knowledge files → recommend **clean-slate** (backup-gated reset), never
competing docs; half-wired components → **deep-plan** is the follow-up.

## Evidence tags

Tag every claim about the repo (state file, findings brief, report):

| Tag | Meaning | Carries |
|-----|---------|---------|
| `VERIFIED` | You opened the source or ran the command yourself | `file:line`, or the command and its output |
| `UNVERIFIED` | You could not confirm it | What you tried and what would confirm it |
| `CORRECTED` | A belief that turned out wrong — yours, a comment's, a README's, an existing doc's | The old belief and the evidence against it |

Recalled API knowledge is a hypothesis: verify against the installed source
or tag `UNVERIFIED`; every `CORRECTED` lands in the corrections ledger.

## The Prime Directive (family rule)

> **No claim without evidence.** Every generated-docs statement carries a
> `file:line` citation, a command you ran, or an explicit `UNVERIFIED` tag.
> A convention needs **2+ examples and no counterexample** — otherwise it is
> an inconsistency to report. A claim the repo's docs got wrong is a
> `CORRECTED` entry, never a fact to repeat.

## Effort triage

Size the read to the repo and record the tier in the state file. Between two
tiers, take the lower one and say so.

| Tier | Signal | Deep read | Cold-reader check |
|------|--------|-----------|-------------------|
| Light | Small repo — roughly under 50 source files, one package | Sequential; scopes may merge | Self-check only |
| Standard | Several packages or a few hundred files | Parallel scopes if subagents exist | Self-check, plus a fresh-agent read if available |
| Heavy | Monorepo, many manifests, or a read that will span sessions | Parallel scouts, one findings file per scope | Fresh-agent read required when subagents exist |

All six scopes are covered at every tier; every Newcomer Question ends
answered or UNVERIFIED. State file and resume:
[references/state-file.md](references/state-file.md).

## Progress checklist

Copy into your response and check off:

```
Know My Repo Progress:
- [ ] Step 1: Recon — tier, stack/size, knowledge files checked, Newcomer Questions, state file
- [ ] Step 2: Deep read — six scopes at the tier's parallelism; corrections logged
- [ ] Step 3: Conventions — 2+ examples each; inconsistencies listed
- [ ] Step 4: Commands — build/test/lint verified by running them
- [ ] Step 5: Exemplar trace — one real feature followed end to end
- [ ] Step 6: Write — Findings Brief confirmed, then AGENTS.md + docs/ARCHITECTURE.md
- [ ] Step 7: Cold-reader test — docs answer the Newcomer Questions; checks pass
- [ ] Step 8: Report — findings, corrections, inconsistencies, state-file disposition
```

## Step 1 — Recon

- Target: a `[project-root]` argument, else the current directory; state
  which you used in the report.
- `.know-my-repo/state.md` exists → this is a **resume** — follow
  [references/state-file.md](references/state-file.md), say where you pick up.
- Detect stack and size — manifests (`package.json`, `composer.json`,
  `go.mod`, …), lockfiles, layout, file count — and pick the tier.
- Check for existing knowledge files (`CLAUDE.md`, `AGENTS.md`,
  `.cursorrules`, `docs/ARCHITECTURE.md`, …): **none or trivial** (< ~20
  meaningful lines) → proceed, merge trivial content later; **substantial**
  → stop and ask ONE question — update, or reset via clean-slate? Recommended
  answer included; never write competing docs beside living ones.
- Write the **Newcomer Questions** — typically 8–15, what a productive
  newcomer must answer: where feature work happens, how to run tests, how a
  feature is added end to end, how it deploys and runs in production, what
  will bite me first. Steps 2–5 answer this list: findings cite the question
  number, mid-read questions are appended, and the read ends when every
  question is answered with evidence or tagged `UNVERIFIED` — not when
  every file has been read.
- Create `.know-my-repo/state.md` from the template — on every tier.

**Preflight:** empty repo or scaffolding only (no meaningful code) → note
it, proceed with minimal docs reflecting that state.

## Step 2 — Deep read

Read the repo like deep-plan Phase 1, at the tier's parallelism — scopes,
findings format, scout brief:
[references/exploration-guide.md](references/exploration-guide.md).
Structure & entry points · data flow (write AND read path) · wiring ·
tests & quality gates · git trajectory · operational reality (deploy,
environments, background jobs, data scale — docs ignoring how it ships are
incomplete).

Classify components **works / half-wired / dead** with a proving file path.
Merge subagent reports and spot-check surprising claims — a scout's wrong
belief is a `CORRECTED` entry like your own. Log corrections as they surface
(READMEs, comments, docs, recon hypotheses the code contradicts). Update the
state file at each step exit (Light: after Steps 3 and 5).

## Step 3 — Extract conventions

Conventions make generated code look native. Extract them per
[references/conventions-guide.md](references/conventions-guide.md) — naming,
boundaries, errors, state, styling, tests. **2+ examples = convention;
1 = observation; conflicts = inconsistency — report both sides.**

## Step 4 — Verify the commands

Find the build / test / lint / run commands (manifests, CI config,
Makefile) and **run the safe ones** (read-only: build, test, lint — not
deploy, not migrate). Record real results — a suite failing on a clean
checkout is a first-class finding. Commands you could not run are
`UNVERIFIED` with the reason AND what would unblock a real run.

## Step 5 — Exemplar trace

The single most useful artifact for a newcomer: pick ONE representative,
recently-touched feature and trace it end to end — route/entry → handler →
service → storage → output/render, naming every file on the path. This
becomes the "How to add a feature here" section: the repo's own pattern,
proven by its own code, not a generic tutorial.

## Step 6 — Write the knowledge set

**Findings Brief Gate** — before writing a single file, present a compact
brief in chat: tier, stack and architecture in a sentence or two, target
file names (AGENTS.md vs CLAUDE.md), verified command results, corrections
ledger highlights, and every inconsistency with a recommended resolution.
10–20 lines; this is the brief, not the docs. Ask for confirmation **once**
— a correction here costs one message, after Step 6 it costs a rewrite. If
the user cannot respond (headless/CI run), proceed — creating files is
reversible and nothing is deleted — but leave every inconsistency
dual-cited and unresolved, and tag user-dependent choices `UNCONFIRMED`.

Write only the knowledge files and `.know-my-repo/` — nothing else — per
[references/knowledge-templates.md](references/knowledge-templates.md):

- `AGENTS.md` — ground rules from real conventions, verified commands,
  observed gotchas. **Under 150 lines.** (Write to `CLAUDE.md`/`AGENT.md`
  instead if the repo's tooling expects that name.)
- `docs/ARCHITECTURE.md` — overview, component table with status, data flow,
  the exemplar trace, inconsistencies, corrections, and sharp edges.

Do NOT generate a ROADMAP.md — direction is the user's call, not the code's.
Half-wired components are unfinished intent: list them, offer deep-plan.

## Step 7 — Cold-reader test

Protocol, fresh-agent prompt, and mechanical checks live in
[references/cold-reader.md](references/cold-reader.md): answer the Newcomer
Questions from the generated docs alone; on Standard/Heavy a fresh
no-context reader does the same and lists its guesses (max 2 fix rounds).

## Step 8 — Report

- **The completed progress checklist**, checked off honestly — an unchecked
  item with a reason beats a falsely checked one.
- **Tier and created files:** the tier chosen and why, then each file, one line.
- **Key findings:** stack, architecture in one paragraph, top 3 sharp edges.
- **Corrections:** every `CORRECTED` entry, or "none — checked READMEs,
  comments, docs, and recon hypotheses". An empty ledger with its checks
  listed beats an invented one.
- **Inconsistencies:** conventions that conflict (the team may want to pick one).
- **UNVERIFIED:** what you could not confirm and why.
- **Cold-reader result:** self-check only, or fresh-agent verdicts/rounds.
- **State file:** `.know-my-repo/` (state.md + findings/) kept for resume —
  offer to delete the whole directory; in a headless run, leave it.
- **Suggested follow-up:** half-wired components worth a deep-plan run.

## When things go wrong

| Situation | Response |
|-----------|----------|
| Repo is empty or only scaffolding | Complete with minimal docs noting current state; AGENTS.md states "scaffolding only, no features yet" |
| Commands fail on clean checkout (Step 4) | Record honest failure with output; this is a first-class finding, not a failure of the skill |
| No git history available | Skip git trajectory (Step 2 Scope 5); note `UNVERIFIED: no git history` in ARCHITECTURE.md; rely on file timestamps |
| Run interrupted or repo too big for one context | Resume from `.know-my-repo/state.md` per references/state-file.md — do not restart |
| No subagent support | Sequential read at Light parallelism; the self-check is the whole cold-reader test; say so in the report |
| User unavailable at Step 1 knowledge-file check (headless) | Stop before Steps 2–8; report the substantial files found and the update-vs-clean-slate choice for an attended session — never write competing docs beside living ones |
| User unavailable at Findings Brief Gate (headless) | Proceed with file creation (reversible); leave inconsistencies dual-cited and unresolved; tag choices `UNCONFIRMED` |
