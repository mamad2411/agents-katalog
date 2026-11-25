---
name: adversarial-review
description: Run an independent audit gate before any fleet output lands. Use after agent-fleet-orchestration Stage 3 (or any multi-agent build) — before merge, before deploy, before the next phase. Frames the reviewer as an external adversary, not a helper; produces triaged findings with human triage for load-bearing blockers.
---

# Adversarial-review: an independent audit gate, not a helper

BLUF: the dominant failure mode of post-build review is sycophancy — the reviewer treats «looks plausible» as confirmation, confirms what the author implied was correct, and produces approval theater. This skill makes that structurally impossible by framing the reviewer as an adversary whose job is to break the work, not bless it.

## Stage 0 — frame the reviewer correctly

The reviewer is an **independent external auditor** (mental model: PhD architect encountering this code for the first time with no social obligation to the author). The instructions to the reviewer must include:

- Do NOT confirm. Do NOT hint. Do NOT ask leading questions. Do NOT soften.
- Your job is to find every way this system fails, is insecure, is brittle, or is wrong.
- «I could not find a problem in area X» is an admissible finding. «Everything looks good» is not.
- Every factual claim requires ≥2 confirmations: a code anchor (file:line or exact snippet) PLUS an external reference (spec, RFC, reference repo, web) OR an explicit «cannot verify without execution» with a stated reason.

Do NOT ask the reviewer to «confirm this is working» or «verify the implementation is correct» — those framings produce sycophancy. Ask: «find every blocker that would prevent this from working correctly in production.»

## Stage 1 — audit dimensions (fixed; do not abbreviate)

Run the reviewer across all dimensions in a single pass. Skipping a dimension is only valid if explicitly stated with a reason.

| Dimension | What to look for |
|---|---|
| Concurrency / lifecycle | data races, leaked goroutines/threads, deadlocks, use-after-free, resources not GC-safe (closed by GC rather than owned lifecycle), subscriptions re-created per-event instead of once per session |
| Error handling | swallowed errors, false success (operation failed but caller sees success), missing propagation, error type that loses context |
| Isolation / security | credentials leaking across trust boundaries, over-privileged components, missing input validation at trust boundaries |
| Architecture & code smell | duplicated logic, reinvented wheels (stdlib or idiomatic library solves this), wrong layer (business logic in transport, I/O in domain), dead code with a live twin (two sources of truth) |
| Benchmark vs reference repos | compare idiom usage to 2–3 reference repos on the same problem; flag where this code diverges from the community's solved pattern |
| Tests-as-theatre | tests that always pass regardless of behavior, mocks that make the test vacuous, test coverage of the wrong layer |
| Robustness bar | every I/O and wait: is there a hard timeout/deadline? is there a forced unblock if the far side hangs? does the system degrade gracefully or panic? |

## Stage 2 — problem-driven research register

When the reviewer encounters an unfamiliar pattern or needs external evidence:

- Register: «I did X, got problem Y — how is Y solved in industry?» (symptom → industrial pattern)
- Not: «how do I do X?» (that anchors on the author's solution, not the problem space)

This framing ensures the reviewer finds the canonical solution independently and can compare it to what was built, rather than rationalizing what was built.

## Stage 3 — triage findings: do NOT auto-fix

After the audit:

1. List findings by severity: blocker (prevents correct operation) / major (degrades reliability or security) / minor (code smell, maintainability).
2. For each finding, hold a reasoned position:
   - **Agree-with-justification**: state why this is a real defect + the code anchor that confirms it.
   - **Reject-as-false-positive-with-justification**: state the reasoning and the evidence that rules out the defect.
3. Load-bearing or disputed findings go to the human — do not auto-resolve them. The lead and developer decide together: fix, accept-with-rationale, or reject.
4. Auto-fixing every finding to silence the reviewer is «slop-on-slop»: it destroys the audit trail and removes the human decision.

## Stage 4 — fix and re-verify, not re-report

For agreed blockers that go to fix:
- The fix is a new agent run with the finding as the precise input (file:line, symptom, root cause, required behavior).
- After fix: re-run the specific verification that the finding demanded (not a full re-review — targeted verification of the changed path).
- A finding is closed when tool output (build, test, lint, static analysis) confirms the defect is gone — not when the fix agent says so.

Mirabilis example: the 2026-06-12 adversarial review of the mirabilis fleet output found 4 blockers:
1. One-shot proxy lifecycle — the proxy server started once and was never restarted on reconnect; first-launch always failed. Fix: session-owned restart.
2. Flock released by GC — an OS file lock (`flock`) was held by a Go object with no explicit release; the GC could collect it mid-session, dropping the lock silently. Fix: explicit lifecycle with deferred close.
3. PTY handoff could deadlock the UI — a synchronous PTY size-change notification ran on the Bubble Tea render loop with no escape; a non-responsive terminal process could hang the entire UI. Fix: deadline on the handoff + goroutine with forced unblock.
4. Dead-code attach with two sources of truth — an attach path existed in both the engine and the TUI layer; neither was canonical, neither was tested. Fix: remove one, make the other the single owner.

None of these were found by the implementation agents. All four were found by the independent adversarial reviewer. Human triage prioritized all four as blockers. Auto-fixing without triage would have resolved symptoms without understanding root causes.

## Output contract

1. Per-dimension findings (file:line anchors + external refs or «cannot verify without execution»). 2. Severity classification. 3. Reasoned position per finding (agree / reject-as-FP). 4. Human triage decisions on load-bearing/disputed items. 5. Targeted re-verification outputs for fixed blockers. BLUF at every stage.

Counter: for a trivial change touching one file with no cross-cutting concerns, a full multi-dimension audit is overhead — state the skipped dimensions and run at minimum the error-handling and robustness checks.

---
Provenance: distilled from the 2026-06-12 mirabilis adversarial review — an independent audit pass that found 4 production blockers missed by implementation agents, triaged with the human, and fixed with targeted verification. The anti-sycophancy framing follows the neuro-matrix critic role discipline; the ≥2-confirmation claim-typing follows the harness epistemic-boundary convention.
