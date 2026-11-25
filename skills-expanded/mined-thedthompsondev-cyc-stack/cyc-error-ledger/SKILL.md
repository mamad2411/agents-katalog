---
name: cyc-error-ledger
description: "Retain searchable failure history with causes, attempted fixes, results and regression evidence. Use when diagnosing a reported bug, error or log, when an attempted fix fails, and when recording its resolution."
---

# Error ledger

Before debugging anything, ask the ledger: "Have we seen this, and what did we already try?" After debugging, write down what you learned, **especially the fixes that failed**. A failed fix is the most expensive thing to rediscover.

For a controller run, `run next` returns `projectLedgerPath` for shared-history lookup and `ledgerPath` for recording. Usually they match: explicit `context.ledgerPath`, otherwise existing `INCIDENT-LEDGER.md`, otherwise `docs/context/error-ledger.md`. When the shared path is outside permitted writes, new runs select `.cyc/runs/ID/error-history.md` and explain why. Search existing shared history and relevant earlier run-local histories; write only the selected target. Create it if absent using [references/entry-format.md](references/entry-format.md). Preserve existing formats; do not create a competing shared ledger.

Run-local history is retained evidence, not an update to the shared project log. Disclose that distinction; later promotion needs authorized scope. Do not expand scope, change configuration, or override a project rule requiring a shared/committed record. Outside a controller run, use the same shared-ledger preference and respect the task's write permissions. Update a context index only when useful and authorized.

## Look up: first step on any bug, error, or log

1. **Make a signature.** Take the error's stable core: error type plus message with the variable parts removed (IDs, timestamps, paths, line numbers), plus the throwing function or area. `TypeError: Cannot read properties of undefined (reading 'finished') @ loadAll`.
2. **Search shared history and relevant `.cyc/runs/*/error-history.md` files** for the error type, key message words, and area or file. Search loosely; the same bug can surface with different wording. Run-local files may exist only in this checkout; do not imply another checkout has them.
3. **On a match, read the whole entry before doing anything.** Then:
   - **Resolved, same cause:** it has regressed. Check whether the recorded fix or its regression test was removed or bypassed. Start there.
   - **Resolved, different cause:** a new entry, linked to the old one.
   - **Open:** continue from the recorded attempts. Do not retry a failed fix unless you can state what is different now.
4. **No match:** say so, and continue with the [diagnose branch](../cyc-understand/references/diagnose.md).

## Record: as attempts happen, not only at the end

- **Open an entry** as soon as the red loop reproduces the error, with status `open`.
- **Append every fix attempt** when it is tried: what was changed, the hypothesis behind it, and the result. A failed attempt gets why it failed, with evidence (the command output that stayed red).
- **On resolution:** record the root cause, the fix commit, the regression test that now guards it, and set status `resolved`.
- **Can't fix it now:** leave it `open` with the best current understanding, or `wont-fix` with the reason and who decided.

Record failures even if the task was abandoned. Unlike context docs, the ledger values dead ends from unfinished work.

Finalize resolved entries before final verification. Record covered-file evidence when the fix is not committed; do not invent a commit. New implementation runs with failures, and all bug-fix runs, must reference the selected `ledgerPath` in their [Deliver assessment](../../docs/work-assessments.md). The controller checks referenced file hashes; it cannot observe unreported attempts or prove the diagnosis. Include shared documentation paths in scope only when those edits are authorized; run-local storage preserves history without broadening source scope. Existing runs keep their captured selection.

## Done when

- Look up: the signature was searched and the result (match or none) stated before diagnosing.
- Record: the entry has a signature, the area, every attempt with its result, and a status. Resolved entries name the root cause, fix commit, and regression test.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Diagnose first, check later | Debugging before searching the ledger | Search first; it takes seconds |
| Success-only record | Only the working fix is logged | Log every failed attempt and why |
| Raw paste | A 200-line stack trace as the entry | Keep the signature and the key frames |
| Symptom as cause | "Root cause: the page crashed" | Name the mechanism that produced it |
| Retrying a known dead end | Same fix as a failed attempt, no new reason | State what changed, or pick another hypothesis |
| Leaked data | Customer data, tokens, or hostnames from logs | Redact before recording |

## Handoff

Look up returns the matching entries (or "none") to [Understand](../cyc-understand/SKILL.md). Record returns the entry ID and status to [Deliver](../cyc-deliver/SKILL.md), which reports it. A regression of a resolved entry is worth a row in the improvements log, because the guard that should have caught it did not.
