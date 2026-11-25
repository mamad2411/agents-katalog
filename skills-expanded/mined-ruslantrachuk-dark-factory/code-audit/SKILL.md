---
name: code-audit
description: Evidence-based code analysis — understand unfamiliar code before changing it, check hypotheses (a client's diagram, README, "how this works") against the code and the deployment, audit someone else's multi-repository system, find the root of an incident in the code. Use for "figure out how this works", "check whether it's true that…", "code audit", "what does service X do", "due diligence", "assess someone else's code", and before planning a change in an unfamiliar part of the code.
---

# Skill `code-audit` — evidence-based code analysis

> From the dark-factory canon (the "Code analysis" practice, [docs/practices/code-analysis.md](https://github.com/ruslantrachuk/dark-factory/blob/main/docs/practices/code-analysis.md)). The method comes from
> multi-repository audits with fan-out passes, an auditor prompt, independent spec reviews and review
> lenses. A fan-out run over many repositories is the `code-audit` module.

## Main principle: everything is a hypothesis until proven by code

A client's diagram, a README, documentation, repository and service names, comments and **agents' conclusions**
are all hypotheses. Only a fact with an address is proof. When docs and code disagree, the code wins, and
the disagreement itself is a finding.

**Evidence tiers** (each answers a different question; they are not ranked):
- **T1 — code** (sources, DB schema, application config): "what it can do";
- **T2 — deploy/CI** (Dockerfile, CI, manifests, orchestrator stack): "what is built and where it goes";
- **RT — runtime** (what is actually running: orchestrator, logs, prod host metrics): "what works";
- **OWNER — owner confirmation**: "what is intended and what is legacy".
"In the code ≠ enabled ≠ deployed" (a feature can be "moved out" according to the code while prod still runs the legacy path; always ask "is it even enabled?").

**Verification statuses:** `confirmed` · `refined` (broadly right, clarified) · `refuted` · `not_found` (no evidence — remains a hypothesis). `confirmed`/`refuted` without evidence are not allowed.

**Evidence** = `path:line` (or range) + a quote no longer than a line, or a CI stage/config key, or a dependency with its version. The revision (tag/commit) — in every conclusion.

## Mode 1 — "figure it out" (one task, your own project)
Before planning a change in an unfamiliar part of the code, or when an incident was not explained by the logs.
1. Phrase the questions as hypotheses: "request X goes through A → B → C", "flag Y is off in prod".
2. Check each against the code and config, with evidence; "is it enabled" — by the environment config, not by the presence of code.
3. Result — a short path map with addresses and a list of hypotheses with statuses; it goes into the preparation package (spec/plan) or the incident report.

## Mode 2 — "audit" (someone else's system or all of your own)
0. **Frame:** goal (support / due diligence / presale / diagram check), scope, prohibitions: write nothing to client repositories, do not print or commit secrets and personal data (a found secret — path and type, without the value).
1. **Sources and their status:** a table current / secondary / dead (a first draft built on an outdated PDF had to be rewritten entirely). The client's input is recorded verbatim (`hypothesis/baseline.md`) and not edited.
2. **Access and clones** — the module's `scripts/clone-group.sh` (token only in a header, clones in the gitignored `app/`). Inventory right away: default branch, last commit, prod tag, where the substantive code is (sometimes not on the default branch). Ask: **where the desired state of the deployment lives** — often outside git (the orchestrator stack).
3. **Revision:** read what is deployed (the prod tag), not HEAD, if that is known.
4. **Fan-out:** unit = a repository, a group of repositories, or an investigation ("where does X live"); hypotheses — as a list in the unit; the module's workflow `scripts/audit-verify.wf.js`, raw results are saved (`audit/runs/<date>-<name>.json`).
5. **Spot check of evidence** — by a separate cheap agent: all `refuted` and at least a fifth of `confirmed` — does the quote exist at the address? Invalid → `not_found`. Without this step agent conclusions are not accepted (in practice manual review keeps only a minority of agents' reclassifications).
6. **Consolidation:** a "hypothesis → fact" ledger (`hypothesis/verification-ledger.md`), a card per unit (`services/<unit>.md`), link edges from both sides (one unit's outgoing = the other's incoming — a cross reconciliation).
7. **Runtime and owner:** RT and OWNER — as separate tiers; questions to the owner — in waves, answers as a map (question → answer → what it changes), history is not overwritten.
8. **Report** — as a new dated file (the old one is marked historical): summary and verdict · coverage and method (units, revisions, number of agents) · fact map with tiers · delta against the input (✅/🔧/❌/❔) · risks with severity, security separately · questions to the owner · plan: top by risk/cost and "deliberately not doing" · links to raw runs and the previous report.
9. **Independent report reviewer** (another model or Codex) — tries to refute factual claims (such a review catches the author's own mistakes).
10. **Findings → work:** task candidates as a list in the report; created in bd/on the board only on the owner's "yes" (without an explicit step, findings stay buried in the report).

## Finding format
Per `docs/review-contract.md`: location · evidence · violated requirement or risk · trigger conditions · consequence · severity. "Clean" is also proven (what was checked and how).
