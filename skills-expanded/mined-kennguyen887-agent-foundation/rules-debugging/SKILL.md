---
name: rules-debugging
description: Binding personal rules for bugs, errors, incidents and perf regressions — load before diagnosing or fixing any bug/error/failing check, choosing the fix layer, or claiming a root cause or that something is verified.
---

# rules-debugging

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Bug Fixes — `07-bug-fix-rules.md`
- Confirm intended behaviour for each branch before adding `return`/`else`/flow changes.
- Never run a strict check before a permissive one validating the same constraint.
- **Fix the whole class**: grep every sibling of the pattern and fix all in the same change; prefer one choke-point guard; verify copied patterns actually work; state the sweep in the report. Guard where data crosses a boundary (persist/accept), throw loudly; reuse the existing contract (e.g. schema `.pick()`), sized to the flow — no new architecture inside a bug fix. A 50+ site sweep is the smell.
- **Event payload null/missing field → first decide boundary, grep all emitters**: in-process (same deploy, emitter holds data) → fix the PRODUCER, emit complete payload, delete listener reconstruction, handle multi-producer union deliberately. Cross-service → consumer tolerates by design, producer keeps always sending (gating drops the whole payload); trace the true blast radius; deploy consumer-tolerance first. Pin with a test through the real path.

## Solution Confidence Rating — `08-solution-confidence-rating.md`
- After every bug/error fix: `Root-cause confidence: X/10` + `Risk: …`. Symptom masks ≤5/10; say "not verified" if not repro'd+tested. Score = weakest load-bearing link; an unproven causal story is a hypothesis (≤3).

## Reasoning Rigor — `09-reasoning-rigor-investigate-fully-before-fixing.md`
- GROUND-TRUTH first: read the real state of the system showing the symptom (API/query/console) before theorizing; access gap = first blocker. Don't flip-flop diagnosis.
- LOGS FIRST, code second: one targeted log query on the entity/route/time before a code crawl.
- Establish baseline/history (did it ever work, when did it break, telemetry over time).
- Find every instance; name the invariant; enumerate what else could be wrong.
- Verify every load-bearing assumption with evidence before shipping.
- "Done" = real end-to-end success artifact, not a proxy; otherwise state what's unproven.
- Answer the whole question (blast radius, adjacent failure modes).
- Stay anchored to the exact reported symptom + example; re-read the report each turn; "re-read the task" = hard drift signal.

## Root-Cause First — `10-root-cause-first-no-fix-arounds.md`
- Trace to the true cause (one level up every time); name guards/try-catch/suppression as symptom patches and rate low.
- Surface root-fix vs patch trade-offs. Patch-first only as explicit hotfix with root fix tracked.
- **Root cause not proven → deliver a REPORT, not a PR** (proven / unproven / the one measurement that settles it). No workaround code litter.
- Resource/perf incidents: isolate the consuming component by direct per-process measurement before naming a cause; blind spots = "undetermined".

## Fix at the Smartest Layer — `11-fix-at-the-smartest-layer-propose-the-layer-choi.md`
- Before code, scan layers cheapest first: config/env → vendor setting → datastore/engine → data fix → existing mechanism → infra → code. Ground-truth the layer. Config cures instance, code kills class — present as a pair, sized to severity. Multiple viable layers → one short block + recommendation BEFORE writing code.
- Error text from inside a dependency (engine/driver/broker/vendor) → diagnose in THAT system first. Locking bugs: read the lock footprint (`performance_schema.data_locks`), not EXPLAIN. Never claim "nothing to fix on our side" without running the diagnostic. Retry is survival, not root fix. Propose engine observability first (deadlock logging). Local engine ≠ deployed engine (vendor + version + default param group).
- A layer needing someone else's hands is blocked, not cheap — prefer the layer you can finish; deliver the whole prepared change, not a question queue.

## Reproduce & Verify — `12-reproduce-verify-by-running-not-logs-tests-alone.md`
- Reproduce before declaring root cause; verify by driving the real flow to its real success state.
- Replacing a live API → capture REAL requests (browser Network tab / access logs), replay against old and new, diff field-by-field, drive the real UI flow. Never invented payloads.
- **Gate in the target branch's own toolchain AND schema**: mirror CI's exact install/Node/script; no symlinked node_modules; diff migrations on both branches before porting any query; a throwing query in a shared `Promise.all` kills every consumer. Clean locally but red in CI on a rule/version you never saw = your gate ran in the wrong environment, not flaky CI.
- **Do not conflate**, each is a separate claim needing its own evidence: rc code ≠ master code, rc schema ≠ prod schema, a local DB named after prod ≠ prod, my own script against a live third party ≠ the deployed service doing it. Say which one you verified.
- **HARD GATE before PR/push**: boot via the real dev runner, clean logs, health endpoint 200.
