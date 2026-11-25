---
name: goliath
description: Run Copilot CLI work through the Goliath ten-role R10 pipeline at Max reasoning effort, with the architect as planner (Claude Fable 5.1) and a pinned model per role — Claude Opus 5.5 for implementation and security auditing, GPT-6 Sol for red-team, GPT-6 Astra for the final reviewer, GPT-6 Luna for every remaining role — and Claude Opus 5.5 as every role's fallback.
---

# Goliath

Goliath is a Copilot CLI-only orchestration policy. Every run uses the architect as planner and
the repo's full R10 role tier (`docs/ROLE-EXPERIMENT.md`): scout, implementer, test-author,
verifier, second-verifier, red-team, reviewer, security-auditor, docs-editor, and synthesizer —
ten execution roles in that canonical order. It does not configure or invoke the Claude Code
harness, and it does not silently substitute a different role or model.

## Role roster and fallback order

Use the primary model in each row if it is available in the current Copilot `/model` picker and
documented by `data/pricing.copilot.json`; otherwise use the fallback. Model IDs must be
resolved from the pricing data at run time; do not invent IDs or hardcode prices. This roster is
a deliberate pin, not a cheapest-first ladder: no role resolves to a Grok or Gemini model.

| Role | Primary | Fallback | Reasoning effort |
|---|---|---|---|
| Architect (planner) | Claude Fable 5.1 | Claude Opus 5.5 | Max |
| Scout | GPT-6 Luna | Claude Opus 5.5 | Max |
| Implementer | Claude Opus 5.5 | Claude Opus 5.5 (same as primary — no distinct fallback) | Max |
| Test-author | GPT-6 Luna | Claude Opus 5.5 | Max |
| Verifier | GPT-6 Luna | Claude Opus 5.5 | Max |
| Second-verifier | GPT-6 Luna | Claude Opus 5.5 | Max |
| Red-team | GPT-6 Sol | Claude Opus 5.5 | Max |
| Reviewer | GPT-6 Astra | Claude Opus 5.5 | Max |
| Security-auditor | Claude Opus 5.5 | Claude Opus 5.5 (same as primary — no distinct fallback) | Max |
| Docs-editor | GPT-6 Luna | Claude Opus 5.5 | Max |
| Synthesizer | GPT-6 Luna | Claude Opus 5.5 | Max |

Claude Opus 5.5 is the pipeline's workhorse: primary for implementer and security-auditor, and
every role's fallback. That makes it a single point of failure — if it is unavailable, the
implementer and security-auditor have no candidate left, so the run stops and reports them. Any
checking role on Claude Opus 5.5 — the security-auditor always, and any other checker that falls
back — shares the implementer's model, so fresh context is its only independence; the ledger
must flag each one. GPT-6 Sol is the roster's middle rung (red-team); GPT-6 Astra is reserved
for the final reviewer gate; GPT-6 Luna covers every remaining role; Claude Fable 5.1 plans and
never executes.

Every dispatch runs at Max reasoning effort, fallback included — interactively via the `/model`
picker's left/right arrows, or headlessly with `--effort=max` / `--reasoning-effort=max` (see
the `effort` skill, and Dispatch below for why the kit driver cannot carry it).

The architect is always the planner and runs before the ten execution roles. The reviewer is
the final review gate: it compares the result with the plan, checks scope and integration, and
must not replace the architect as planner. It does not itself sequence the other nine roles —
that coordination is this policy's job, run in the canonical order below.

## Execution protocol

1. Inspect the active roster before an expensive run:

   ```bash
   python3 {{POLYTROPOS_ROOT}}/bin/copilot_pricing.py models --json
   ```

   Confirm the selected IDs are also exposed by the current `/model` picker and can run at Max;
   a model that cannot counts as unavailable. If a primary is unavailable, use that role's
   fallback. If every candidate for a role is unavailable, stop and report the missing role;
   never substitute a model outside that role's row.

2. The architect (Claude Fable 5.1) creates the durable plan and acceptance criteria before any
   execution role. Do not use the implementer, reviewer, or another role as the planner.

3. Run the ten execution roles in the canonical R10 order (a finding raised by an earlier role
   is never credited to a later one that raises it too):

   ```
   scout → implementer → test-author → verifier → second-verifier → red-team → reviewer →
   security-auditor → docs-editor → synthesizer
   ```

   - **Scout** (GPT-6 Luna) grounds the work against the target repo before anything is
     written — no adjudicable findings expected; judged qualitatively.
   - **Implementer** (Claude Opus 5.5) changes files against the approved plan. It must report
     changed paths, assumptions, and the exact validation it ran.
   - **Test-author** (GPT-6 Luna) writes adversarial tests from the architect's plan and
     acceptance criteria. It may change tests only and must not implement the feature itself.
   - **Verifier** (GPT-6 Luna) starts from fresh context and independently checks the
     acceptance criteria. It must rerun the relevant checks, never trust the implementer's
     success claim, and must report failures explicitly.
   - **Second-verifier** (GPT-6 Luna) is a redundant, independent pass over the same
     acceptance criteria. A finding raised by both verifier and second-verifier belongs to the
     verifier, not the second-verifier.
   - **Red-team** (GPT-6 Sol) is mandatory and attempts to break the
     implementation beyond the verifiers' ordinary checks, focusing on edge cases, misuse,
     regressions, and unsafe assumptions. It must not rewrite tracked files while reviewing.
   - **Reviewer** (GPT-6 Astra, the final reviewer) compares the result with the plan, checks
     scope and integration, and coordinates acceptance. It must not replace the architect as
     planner.
   - **Security-auditor** (Claude Opus 5.5) audits the accepted change for exploitable issues.
     A finding raised by both reviewer and security-auditor belongs to the reviewer, not the
     security-auditor.
   - **Docs-editor** (GPT-6 Luna) keeps directly affected documentation current — no
     adjudicable findings expected; judged qualitatively.
   - **Synthesizer** (GPT-6 Luna) distills the run's reusable lessons into notes — no
     adjudicable findings expected; judged qualitatively.

4. Accept the work only when all ten execution roles report success (or, for scout/docs-
   editor/synthesizer, complete their non-adjudicable duty) and the architect's plan is
   satisfied. On failure, send the exact evidence back to the responsible role and rerun only
   the failed stage or its necessary dependency.

## Dispatch

For an isolated role dispatch, use the selected model and Max reasoning effort explicitly:

```bash
copilot -p "<self-contained role brief>" --model <resolved-model-id> --effort=max
```

Resolve the display name to its current model ID with the pricing engine before dispatching;
the examples above intentionally do not embed live pricing-key IDs. `copilot_execute.py` does
not forward `--effort`/`--reasoning-effort`, so a Goliath run needing pinned Max effort on every
role dispatches directly with `copilot -p`, not through that driver.

Never invoke the real Copilot CLI from tests or verify commands. Use `--dry-run`, injected
runners, or synthetic fixtures when validating orchestration logic.

## Reporting

End with a compact ledger containing the architect planner plus all ten execution roles,
selected models and effort, availability fallbacks used, every checking role that ran on the
implementer's model, files changed, verification commands and results, reviewer decision,
red-team and security-auditor findings, and any unresolved blocker. Do not claim success when a
required role could not run.

## Installed?

If `{{POLYTROPOS_ROOT}}` is still literal, the Copilot bundle is not installed. Install it with
`python3 bin/harness_select.py install --harness copilot`, then reload skills in Copilot CLI.
