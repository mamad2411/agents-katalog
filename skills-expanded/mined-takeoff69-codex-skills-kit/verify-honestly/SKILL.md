---
name: verify-honestly
description: "Choose proportional verification and write evidence-bounded completion claims for coding-agent work. Use before saying work is fixed, done, working, passing, shipped, or deployed; when asked to verify a change; when relying on another agent's findings; or when reporting counts, artifact properties, UI behavior, live data, or production state."
metadata:
  version: 0.2.0
---

# Verify Honestly

Match every completion claim to evidence from the context that actually runs the work.

## Core rule

Verify in the real execution context, then name the verification level reached. Do not silently substitute an easier context:

- source inspection for execution
- mocks for real data
- local behavior for production behavior
- build success for rendered UI correctness
- configuration text for an external probe
- intended output for the actual artifact

If exact context is unavailable, state what remains unverified and what would verify it.

## Verification ladder

Use this vocabulary in completion reports:

1. `code read` – trace logic without executing it.
2. `local tests` – run relevant unit or integration checks locally.
3. `browser pass` – exercise rendered behavior in a browser, including relevant viewports.
4. `live data check` – query real data or service state consumed by the change.
5. `production smoke` – exercise deployed behavior end to end.

Name highest applicable level per shipped item. Lower levels need mention only when they explain residual risk. Ladder represents increasing runtime proximity, not a demand to run every level.

## Proportionality

Choose cheapest probe that would catch likely failure.

- Scale depth with blast radius, irreversibility, and uncertainty – not session length.
- Treat green deterministic gate as evidence. Cite it instead of re-deriving same fact manually.
- Verify each unchanged property once.
- Prefer one consolidated verification pass over many redundant agents or repeated commands.
- Add independent verifier only when it contributes different evidence, failure lens, or required independence.
- If verification costs more than safely redoing work, say so and choose cheaper path.

## Surface matrix

| Claim | Minimum useful evidence |
|---|---|
| Code behavior | Focused executable test or exact reproduction |
| UI behavior or layout | Browser pass at affected viewport and state |
| Database or data-shape behavior | Representative real rows or production-shaped fixture; name which |
| Pipeline or scheduled job | Run same command, environment, and working directory when accessible |
| Infrastructure state | External probe or observed event, not config grep alone |
| Artifact size, count, or contents | Measure generated artifact itself |
| Webhook, email, or integration | Captured real payload or test delivery through actual boundary |
| Production behavior | Deployed revision plus production smoke |

## Claims from agents and audits

Treat another agent's RED/GREEN verdict, line citation, or confirmed bug as untrusted evidence until checked against current source.

For large finding sets:

1. Re-check riskiest two or three findings plus one random finding.
2. Escalate to full re-check only when sample disagrees.
3. Anchor fixes to live source, not quoted source in audit report.
4. Re-check current revision when HEAD may have moved during audit.

## Reporting contract

Lead with outcome and level:

```text
Fixed; local tests passed: <commands>. Browser pass and production smoke not run.
```

For partial evidence:

```text
Code read confirms new guard is wired. Runtime behavior remains unverified because <blocker>.
```

Avoid `works`, `verified`, `all good`, or `should be fixed` without named evidence.

## Completion checklist

- [ ] Match every shipped item to named verification level.
- [ ] Use execution context that runs property being claimed.
- [ ] Measure counts and artifacts directly.
- [ ] Re-check agent or audit claims relied upon.
- [ ] Flag deploy-gated or inaccessible checks explicitly.
- [ ] Keep verification proportional and non-duplicative.
- [ ] State exact commands, probes, or artifacts supporting claim.

## Stop conditions

- Required surface is inaccessible: stop verification and report exact gap.
- User asks to confirm someone else's result: verify from current state rather than inheriting approval.
- Evidence contradicts expected result: report failure before attempting broader work unless task includes fixing it.

## Related skills

- `gate-engineering` builds durable nets after recurring failures.
- `session-close` uses this vocabulary in final handoff.
- `retro-distill` turns verification failures into reusable rules.
