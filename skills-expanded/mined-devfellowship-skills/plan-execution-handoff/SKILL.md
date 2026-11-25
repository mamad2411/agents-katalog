---
name: plan-execution-handoff
description: "Use when a large plan is about to be executed by agents or people, and when resuming execution after a crash or handoff — executor briefs by section reference, who merges, verification tools by path, resource budget, requester corrections mid-flight, and the definition of done (seen running on the path real users get). Skip for executing a one-PR plan yourself."
author: SamuelStefano
tags: [planning, execution, multi-agent, handoff, verification]
---

# From plan to shipped

**Core principle:** the executor brief carries the gates, not just the tasks.

*(A builder merged its own PR 84 s after opening it and deleted the branch the
deploy pointed at; "browser tool unavailable" was accepted while it was installed
next door; three sessions resumed the same handoff; a plan was marked done four
hours before three layout bugs were found on a phone.)*

## Executor brief

One per agent, from `complex-plan/templates/EXECUTOR-BRIEF.md`:
- Scope by section reference ("§2.1–2.2, ADR-3, PR rows 4–5"). Two executors
  sharing only a file-format section can run in parallel.
- **Open a PR. Do NOT merge.**
- Re-read the live plan and ADRs before starting and before each PR. *(A
  follow-up PR contradicted ADRs added after the executor's snapshot; closed, zero credit.)*
- Never delete or weaken an assertion of code you did not change.
- Verification tools by path; a failing tool is a blocker to report, never a reason to skip.
- No dead controls. Resource budget stated. A step the brief forbids cannot be in the acceptance.
- Commit WIP early; one worktree per agent; `.gitignore` committed before any agent starts.

## Merge policy

- The merger is named (orchestrator or a human) and is never the PR's author.
  It merges only after an independent review; UI PRs with a screenshot of the built app.
- Deploys track `main` only.
- If a required suite is skipped, name its replacement (e.g. one full e2e run on the chained tip).
- A red covering suite blocks the stack; fix specs in the PR that changed the UI.

## During execution

- Requester corrections go to `EXECUTION-LOG.md` → "Open corrections" at once,
  until applied. *(A correction said in chat was lost when an incident took over.)*
- A requester answer that overrides an ADR: edit the ADR in the live plan first,
  then act. Executors follow the plan, not the chat.
- Removing a capability: see `plan-acceptance-gates/non-ui-gates.md` §5.

## Resuming after a crash or handoff

1. Read the last 20 lines of `EXECUTION-LOG.md` and `git worktree list`.
2. `gh pr list --state open` (or equivalent) vs the PR table.
3. Re-read ADRs changed since the log's last date.
4. Write yourself as the single owner session in the log before touching a branch.

## Definition of done

- Production build on the **default** path, screenshot per band; pipelines: the
  named consumer saw the output in their place.
- Deploy runbook: DNS → verify it resolves → domain/certificate → deploy `main`
  → verify HTTPS 200. *(A domain created before its DNS record failed certificate
  issuance; the proxy never retried.)*
- Status moves to done only with that evidence linked.

## After shipping

Retro, one line per issue: symptom → cost → rule → which skill owns the rule.
Feed it into your local copy of this pack, or a PR to its registry. The fastest
clean plan in the source cases was fed by retros written that way.
