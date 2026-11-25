---
name: facade-success-diagnosis-loop
description: Applies the Sept 2026 wave of self-diagnosing local-first agents (ElyAgent v2.2, KIRA Superapp) formalizing the **façade-success problem** — agents that report success without the runtime having evidence from the tool that performed it — with the diagnosis loop: record whether the agent actually did what it claimed after each autonomous run, flag "reported success, no real effect," diagnose the cause, and surface a reviewable fix proposal. Use when [building self-diagnosing agent runtimes, auditing whether an agent completed what it claimed, designing façade-success detection, or implementing evidence-based task-completion gates]. NOT for [agent payment record keeping (see agent-payment-record-gap), trust calibration for twin agents (see twin-agent-trust-attribution), or general agent security (see mcp-security-trust)].
---

# Façade-Success Diagnosis Loop: Evidence, Not Confidence

## Overview
The Sept 2026 wave of local-first agents formalizes a runtime discipline the library's payment skills named but didn't operationalize: **façade success** — an agent reports a task complete without the runtime holding evidence from the tool that performed it. ElyAgent v2.2 (self-hosted, Elastic License v2) runs a background diagnosis loop after every autonomous run: record whether the agent *actually* did what it claimed, flag "reported success, no real effect," diagnose the cause, and surface a reviewable fix proposal on an admin Incidents page. KIRA Superapp (Apache-2.0, Apple silicon) states the design rule directly: **KIRA should not say a task is complete unless the runtime has evidence from the tool that performed it.** The model is the planner; the runtime owns execution, permissions, and proof.

## When to Use
- Building self-diagnosing agent runtimes that measure real success rate, not declared success rate
- Designing evidence-based task-completion gates (tool result > model confidence)
- Auditing whether an agent product reports success honestly
- Implementing façade-success detection in production agent systems

## Façade-Success Diagnosis Loop
1. **Record, don't trust.** After each autonomous run, record whether the agent *actually* did what it claimed — the runtime, not the model, is the witness.
2. **Flag façade success.** Surface "reported success, no real effect" as a distinct incident class on an admin Incidents page.
3. **Diagnose the cause.** Classify the failure (tool call failed silently, wrong tool, malformed arguments, hallucinated path, premature `finish`).
4. **Propose a reviewable fix.** Surface a concrete fix proposal (add a missing tool, tighten an argument check, add a post-condition) on the incidents page for human approval.
5. **Measure real success rate, not declared.** Publish the gap as a product metric: "measured completion" vs "claimed completion."

## KIRA's Evidence Rule (the runtime's job)
- The model is the planner; **the runtime owns execution, permissions, and proof**.
- A language model can write a convincing sentence saying a file was created or a command succeeded; the runtime must confirm via the tool before reporting.
- Memory filtering (strip likely secrets), permission gates on mutating actions, private-reasoning filtered before display and before chat persistence.

## Key Evidence
- ElyAgent v2.2 (June 2026): self-diagnosis loop — "façade success" detection + diagnosis + reviewable fix proposals on an admin Incidents page; mission failures always graded by an external LLM-as-judge; successful missions spot-checked (1 in 5).
- KIRA Superapp (Sept 13, 2026): the orchestration loop requires tool results to confirm task completion; evidence from the runtime, not model confidence; local-first with permission gates; memory filtering for secrets; the developer explicitly asking for criticism of "the permission model, memory boundaries, and tool-result loop."
- Design-rule convergence across independently built products: both treat façade success as a first-class runtime concern, not a prompt-engineering problem.

## Pairs-with
- `agent-payment-record-gap` (the accountability layer beneath payment agents — same "who witnessed the behavior" question)
- `trust-calibration-ux-pattern` (the human-side calibration this supports)
- `privacy-preserving-local-ai` (the local-first runtime this pattern lives in)
- `sovereign-pii-masking-middleware` (same September wave, the privacy layer)
- `twin-agent-trust-attribution` (attribution ambiguity — the failure mode this catches)
- `mcp-security-trust` (the tool layer this monitors)

## A-Tech Alignment
- **Open source:** both ElyAgent (Elastic License v2) and KIRA (Apache-2.0) are open source; the pattern is implementable in any agent runtime.
- **Privacy:** the diagnosis loop runs on the runtime, not the cloud — private reasoning filtered before display and before persistence.
- **Financial freedom:** a solo maintainer product where the façade-success metric is the product's own quality bar; solo builders can adopt the loop without enterprise infrastructure.
- **Practical:** the five-step loop is a one-weekend implementation for any agent product; the "evidence-based completion gate" is the highest-leverage single fix.

## Honesty Caveats
- ElyAgent's diagnosis loop is self-reported (single maintainer, 46 releases, 4 stars — early-stage, small community).
- KIRA is explicitly early software; the developer asks for criticism of the permission model, memory boundaries, and tool-result loop — the façade-success mechanism itself is claimed, not benchmarked.
- Neither project publishes measured façade-success rates; the pattern is validated by design review, not by published metrics.
- The library's existing agent-payment-record-gap skill covers the *payment* layer; this skill is the *general runtime* layer — they are siblings, not duplicates.

*Sources: franckolv-dev/ElyAgent v2.2 (June 2026, GitHub); KIRA Superapp (Sept 13, 2026, Web Pulse/DEV); both project READMEs.*