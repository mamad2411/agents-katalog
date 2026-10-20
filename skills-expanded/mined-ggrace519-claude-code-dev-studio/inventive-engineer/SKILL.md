---
name: inventive-engineer
description: Inventive senior-engineer loop — survey the codebase deeply, research the state of the art, write ranked proposals to INNOVATIONS.md, then build the top picks on innovation/<slug> branches. Use when the user asks to innovate, modernize, level up, or make a project elite or impressive, asks which features could be added or are missing, or wants state-of-the-art research applied to their own code.
---

# Inventive Engineer

Turn a working codebase into an exceptional one. The job is not a code review and not a refactor — it is invention grounded in evidence: deeply understand what exists, study what the best projects in this space do, then propose (and optionally prototype) improvements that are novel, concrete, and worth building.

The deliverable is two things: `INNOVATIONS.md` at the repo root (the ranked proposal record), and working implementations of the top proposals, each on its own `innovation/<slug>` branch. Never commit to the default branch.

## Phase 1 — Deep codebase survey

Do not skim. Spend real effort here; weak ideas almost always trace back to a shallow survey.

1. Map the architecture: entry points, services, data flow, storage, external integrations, deploy targets. Read configs (Docker/Compose, CI, systemd, IaC) — they reveal operational reality better than source code.
2. Identify the stack precisely: languages, frameworks, versions, infra. Note anything pinned old or deprecated.
3. Infer the project's *purpose and users*. Ideas must serve what the project is actually for.
4. Assess maturity honestly: prototype, internal tool, or production system? The bar for "elite" differs for each.
5. Collect friction signals: TODO/FIXME/HACK comments, dead code, copy-pasted blocks, manual steps documented in READMEs, missing observability, error handling gaps, things done by hand that machines should do.
6. Note conventions and taste: naming, structure, idioms. Proposals must fit the codebase's existing voice unless changing it *is* the proposal.

Write a short internal summary (10–20 lines) of findings before moving on. If the repo is large, prioritize: entry points → core domain logic → infra/config → tests → docs.

## Phase 2 — Research the state of the art

Use web search aggressively. The goal is to import ideas from outside the user's bubble.

Research along these axes (pick the relevant ones, not all):

- **Best-in-class peers**: What do the most admired open-source projects in this exact domain do that this codebase doesn't? Study their feature lists, architecture docs, and changelogs.
- **Emerging techniques**: New libraries, language features, protocols, or patterns from the last 1–2 years that apply here. Check release notes of the project's own dependencies — major versions often unlock capabilities the code isn't using.
- **Adjacent-field transplants**: Techniques standard in one field but rare in this one (e.g., property-based testing applied to a config parser; CRDTs applied to a sync feature; eBPF applied to an ops tool). Cross-pollination is where "novel" usually comes from.
- **Operational excellence**: How elite teams run this kind of system — observability, self-healing, progressive delivery, chaos/fault injection — scaled appropriately to the project's maturity.
- **AI leverage**: Where an LLM, embedding index, or agent loop would genuinely remove toil or unlock a feature — only if it fits the project. Prefer local-first options when the user's environment suggests it.

Record sources. Every externally-inspired proposal should cite where the idea comes from (project, post, paper, release notes).

## Phase 3 — Ideation, then ruthless filtering

Generate broadly, then cut hard. Aim for 15–25 raw candidates across categories: novel features, performance, architecture, developer experience, observability/ops, security, and "wow factor" (the thing that makes someone say "I can't believe this project does that").

Then filter. Kill an idea if it is any of:

- **Generic boilerplate** — "add tests", "add CI", "write docs", "add linting" are banned unless the gap is severe and the proposal is specific about *what* and *why this project*.
- **A rewrite in disguise** — "port to Rust/switch frameworks" needs extraordinary justification.
- **Resume-driven** — technology for its own sake with no problem behind it.
- **Misfit** — ignores the project's purpose, users, maturity, or the user's constraints (budget, hardware, team size).
- **Vague** — if it can't be sketched concretely in Phase 4, it isn't ready.

Score survivors on four axes (1–5 each): **Impact**, **Novelty**, **Effort** (inverted — lower effort scores higher), **Fit**. Keep the top 6–10. Ensure the final set is mixed: at least one quick win (< a day), at least one ambitious flagship idea, and a spread across categories.

## Phase 4 — Write INNOVATIONS.md

Use this exact structure:

```markdown
# Innovation Proposals — <project name>
*Generated <date> · based on commit <short-sha>*

## How this codebase stands today
(5–10 honest lines: what it is, what it does well, where it's ordinary.)

## What the best in this space are doing
(Short synthesis of Phase 2 research, with links.)

## Proposals (ranked)

### 1. <Imperative title, e.g. "Add speculative prefetch to the RAG retriever">
**Category:** feature | performance | architecture | DX | ops | security | wow
**Impact 5 · Novelty 4 · Effort 3 · Fit 5**

**The idea.** 2–4 sentences. What it does and why it makes the project better.
**Inspired by.** Source(s) with links, or "original — derived from <observation in codebase>".
**Implementation sketch.** Concrete: which files/modules change, new components, data flow, key library choices. Enough that a competent engineer could start tomorrow. Include a code/config snippet when it sharpens the sketch.
**Effort.** Realistic estimate (hours/days) and main risk.
**First step.** The single smallest action that starts this.

### 2. ...

## Killed ideas (and why)
(3–6 one-liners. Shows judgment and saves the user from re-proposing them later.)

## Suggested order of attack
(2–4 sentences: what to do first and why, considering dependencies between proposals.)
```

Tone of the document: confident, specific, zero filler. Every claim about the codebase must be true (verified in Phase 1); every claim about the outside world should be sourced (Phase 2).

## Phase 5 — Build

Building is the default, not an option. After delivering `INNOVATIONS.md`, implement the top proposals — by default the highest-ranked quick wins plus the #1 overall pick, unless the user scopes it differently ("build all of them", "just #3", "doc only").

Rules:

1. One branch per proposal: `innovation/<slug>`, branched from the current default branch. Never commit to the default branch, and never stack proposals on one branch — independent branches keep each idea reviewable and revertible on its own.
2. Build a complete, working vertical slice — running code with the happy path proven, not pseudocode or scaffolding. Stub only what genuinely can't be built locally (external paid APIs, prod-only infra), and mark stubs loudly.
3. Match existing code conventions exactly: naming, structure, error handling style, logging patterns. New code should look like it was written by the original author on a good day.
4. Commit in logical units with clear messages referencing the proposal (`innovation #2: add speculative prefetch to retriever`).
5. Run whatever verification the repo offers (tests, linters, a smoke run). If something fails, fix it before moving to the next proposal.
6. Close each branch with a `DEMO.md` in the branch root (or a section appended to the final summary): how to run it, what works, what's stubbed, what the next increment would be.

Finish with a summary table: proposal → branch name → status (working / partial / blocked) → how to try it.

## Quality bar

The user asked for *elite, novel, impressive* — hold proposals to that. Before delivering, self-check:

- Would a staff engineer at a top company find at least 2 of these proposals genuinely interesting (not obvious)?
- Is at least one proposal something the user has likely never seen suggested for this project?
- Could every implementation sketch be started today without further clarification?
- Did the research phase actually change the proposal list, or did Phase 2 get skipped in spirit? If proposals could have been written without reading the code or searching the web, start over.
