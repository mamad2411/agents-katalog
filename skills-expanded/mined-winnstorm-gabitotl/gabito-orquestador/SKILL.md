---
name: gabito-orquestador
description: Delegates work without losing context: inline for small work, one read-only mapper, one writer, one verifier, always sequential. Trigger: before delegating to a helper, planning multi-step work, or when a task spans 4+ files.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
---

# Gabito orchestrator: delegate without losing context

You are the single orchestrator. You keep the thread, the decisions and the user. Helpers do bounded
reading or writing and hand back a short result. Never run two helpers at the same time.

## Routing ladder

Pick the smallest rung that fits. Never go up a rung just because the work "feels big".

| Situation | Route |
|---|---|
| Small, understood work; deciding or verifying from 1-3 files | Inline. No helper. |
| Understanding needs 4+ files, or more than ~5 sequential lookups | One read-only mapper (`gabito-recolector`). |
| Change touches 2+ non-trivial files | One writer (`gabito-escritor`). |
| Risky change: security, data loss, shared contracts, migrations | One verifier (`gabito-verificador`) after the writer. |

Reading that only prepares a write belongs to the writer, not to a separate mapper.
A helper is used only if it clearly saves context. When in doubt, stay inline.

## Rules

1. One helper at a time. Wait for its result before launching the next one. Never several agents in parallel.
2. Before delegating, check the ask rules in the persona. Ask the user first when data could be lost,
   the decision is hard to revert, or the goal is unclear. Decide alone on minor, reversible details.
3. Run `gabitotl who` first when others may touch the same area (`gabito-equipo`).
4. Query memory by relevance before planning (`gabito-memoria`).
5. Back up files a helper will modify with `gabitotl backup create`.
6. Forward the language contract: code, comments, docs, commits and PRs in English (or the project's language);
   the persona voice applies only to chat with the user.

## What every delegation carries

Give the helper a self-contained brief. It has no memory of this chat.

- Objective and why, in two or three sentences.
- Allowed edit surfaces: exact paths or globs. Everything else is read-only.
- Acceptance criteria that can be observed.
- Verification: the exact commands to run in the foreground and the project's test runner.
- Constraints: no AI attribution anywhere, no force-push, no secrets in `.gabitotl/`, truth order
  (current code > `.gabitotl/` > Git > memory).
- The advisory heuristic: about 400 authored changed lines per task. It is a planning aid, never a cap and
  never a reason to delete tests, docs or comments.
- The skill to load: `gabito-recolector`, `gabito-escritor` or `gabito-verificador`.

## After the helper returns

1. Synthesize a short handoff for yourself: what changed, what was run, what is unknown.
2. Spot check: re-run at least one reported command yourself. A report is a claim, not proof.
3. If the helper stopped because work fell outside its edit surfaces, decide: widen the surface or re-plan.
   Do not let it edit outside silently.
4. Never relay a helper's "done" without checking it.

## Substantial work

Work is substantial when it has two or more meaningful steps, or progress worth recovering after an interruption.

- Keep a short task list in the project's feature document (for example `odd/tasks/<feature>.md` when the
  project uses one) or in memory under a stable topic key. Record per task: route (inline or delegated),
  why, the commit hash and the checks observed.
- Check a task off only after its outcome and checks were observed.
- Each task ends with one work-unit commit on a feature branch, with tests and docs alongside the behavior.
  Hand the commit to `gabito-entrega`; never commit on the base branch.
- Small, understood work creates no task artifacts.

## Closing

- Report with the persona blocks: did, progress, next. Add the OJO (Heads-up in English) or TIP block only when it adds value; the persona language names it.
- Save decisions and discoveries (`gabito-memoria`) before saying "done", and write the session summary.
- Say plainly which checks failed, were skipped or were unavailable.

## Chat concision

The reply length follows `gabitotl persona mode` (normal, lite or full). It shapes only what you say in chat:
helpers' prompts, code, commits, PRs, docs and memory entries keep their normal wording, and security warnings,
destructive-action confirmations and questions to the user are never shortened.
