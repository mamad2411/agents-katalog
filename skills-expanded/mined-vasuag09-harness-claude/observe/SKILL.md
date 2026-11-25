---
name: observe
description: Feedback step that closes the loop from production back into the harness — take a signal you BRING to it (a pasted stack trace, log snippet, error text, or an issue/monitoring URL), triage it into a located, reproducible failure, and route it into the existing /fix lane. Bring-a-signal only — no polling, no credentials, no new MCP. It locates the failing area and shapes a repro SEED; it does NOT write the finished failing test — that is /fix's job. Opt-in; invoked explicitly. Use when production surfaced something and you want it fixed under the harness's gates.
---

# /observe — triage the signal, locate the area, route to /fix

Goal: turn a raw production signal into something the harness can act on. The user **brings** the
signal (the harness does not watch anything); `/harness-claude:observe` grounds it in real code —
*which* component, *what* failure, *what* would reproduce it — and hands that package to
`/harness-claude:fix`, which runs the reproduce-first discipline. This is the step that makes the
pipeline a **loop** rather than a line: `…/ship → /deploy → (prod) → /observe → /fix → …`.

> **Opt-in.** Invoked explicitly. **Bring-a-signal only** — no polling, no credentials, no new MCP;
> you paste/point at the signal. **Git boundary:** `/harness-claude:observe` is read-only — it never
> commits, pushes, or branches; the fix is committed (if at all) only later through
> `/harness-claude:ship`.

## When `/harness-claude:observe`, when `/harness-claude:fix`
- **`/harness-claude:observe`** is for a prod signal you **don't yet know how to reproduce in code** —
  it triages and locates, then routes. Start here when all you have is a stack trace / log / alert.
- **`/harness-claude:fix`** is the lane itself — reproduce-as-a-failing-test-first, root-cause, minimal
  fix. If you **already** have a red test or a known repro, skip `observe` and go straight to `fix`.

## How it works
```
parse the brought signal → locate the failing area (mgrep/graph) → shape a repro SEED → hand to /fix
```

## Do this
1. **Parse the brought signal.** From the pasted stack trace / log / error / issue URL, extract a
   structured failure description: the service or component, the error message or pattern, the
   conditions it appears under, and any data visible in the signal. No polling, no credentials, no new
   MCP — you work only from what was handed to you. (AC-O1)
2. **Locate the failing area in real code.** Use `mgrep` / the knowledge graph to trace the signal to
   its origin — the function, module, or path the error points at. Ground the signal in the codebase
   rather than guessing; name the suspected location. (AC-O2)
3. **Shape a repro SEED — not the finished test.** Describe the smallest input/state likely to trigger
   the failure (or concrete **manual** repro steps when automation genuinely isn't possible — the same
   carve-out as `/harness-claude:fix` step 1). **Do NOT write the finished failing test here** —
   capturing the bug RED is `/harness-claude:fix`'s non-negotiable first step; duplicating it blurs the
   boundary. (AC-O3)
4. **Hand off to `/harness-claude:fix` — then stop.** Pass the package: the structured failure
   description (1), the located area (2), and the repro seed (3). `/harness-claude:fix` runs
   reproduce → root-cause → minimal fix-plan and rides the existing review/verify/ship gates.
   `/harness-claude:observe` does **not** duplicate any of that, and stays read-only throughout. (AC-O4)

## Security & trust
- A brought signal (stack trace, log line) may contain **PII or secrets**. Do not echo raw log content
  into any persisted artifact; carry forward only the structured failure description needed by `/harness-claude:fix`.
- **Read-only:** `/harness-claude:observe` never writes to the repo. The git boundary holds.

## Notes
- Self-contained: a single skill that *leads* and reuses existing tools — `mgrep` / the graph (locate)
  and `/harness-claude:fix` (the hand-off). **No new agent, no new dependency, no new MCP server, no new
  runtime.**
- **Active monitoring is deferred (YAGNI).** Polling Sentry / Datadog / CloudWatch would need an MCP +
  credentials + a running poller — out of scope for v1. The intake is a clean seam: a future source
  adapter could push signals in, but it is built only when a backend actually exists.
- The skill *is* the lead — there is no separate observe agent (same pattern as
  `/harness-claude:fix`, `/harness-claude:orchestrate`, `/harness-claude:operate`).

## Exit criterion
The brought signal was parsed into a structured failure, the failing area was located in real code, a
repro seed (or manual steps, with the reason automation wasn't possible) was shaped, and the package
was handed to `/harness-claude:fix` — never a finished RED test produced here, and never a commit made.
