---
name: sui-move-auditor
description: Use only for full Sui Move security audits that validate exploitability, retain code-backed medium, low, and informational issues, and produce a structured audit report. Do not use for general Sui Move questions, workflow discussions, skill-maintenance tasks, or ordinary code explanation unless the user explicitly invokes $sui-move-auditor or clearly asks for a full audit.
---

# Sui Move Skill

Use this skill for Sui-specific smart contract security reviews. This file defines the execution process for the agent. Detailed vulnerability categories, check items, and bug-specific prompts belong in `references/checks/check-router.md` and the routed check files under `references/checks/checklist/`.

Read supporting references only when they are needed:

- `references/banner.txt` at the start of the audit to print the skill banner once
- `references/workflow.md` for the full step-by-step audit flow
- `references/pre-audit/scoping.md` during initial package inventory and trust-boundary mapping
- `references/pre-audit/review-lens.md` before deep review and during false-positive validation
- `references/validation/candidate-validation.md` when turning a candidate into a validated finding or rejecting it
- `references/validation/false-positive-filters.md` during the false-positive pass
- `references/reporting/report-formatting.md` before assembling the final report
- `references/reporting/severity.md` when assigning risk

Read `references/checks/check-router.md` twice:

- once after initial scoping, to decide which topic references to load
- once before finalizing findings, to confirm coverage and eliminate blind spots

If any prior audit artifact exists in the target workspace, such as a PDF, markdown report, issue list, or patch note that names historical findings, treat it as mandatory input. Do not begin fresh bug hunting until those prior findings have been converted into a regression checklist with explicit current-code anchors.

Treat `references/checks/check-router.md` as the checklist router and loading guide. Treat this file as the workflow and reporting layer.

Some harder checklist items include tiny Sui Move examples. Use them to recognize the state transition or invariant being discussed, but never treat the example match alone as a finding.
Default toward evidence over speculation: omit unsupported leads, but keep well-supported medium, low, and informational security issues when they are grounded in code and relevant to security, operability, or incident response.

## Audit Objective

Your job is to determine whether an attacker can do any of the following:

- gain assets, minting power, or privileged control without authorization
- violate economic or state invariants
- lock, burn, freeze, or orphan user assets unexpectedly
- bypass intended workflow or role restrictions
- exploit initialization, migration, or upgrade paths

Also identify code-backed security weaknesses that may not directly yield theft but still matter, such as scoped denial of service, trust-boundary weaknesses, monitoring blind spots, and defense-in-depth failures.

Prioritize real impact over surface-level observations. A good finding in Sui Move usually ties together object ownership, capabilities, and a broken state transition, but the report should also retain lower-severity issues when the downside is concrete and the evidence is direct.

## Workflow

Use `references/workflow.md` for the full step-by-step procedure.

1. Scope the package, identify trust boundaries, and collect any prior audits, issue trackers, or historical findings before loading topic checks.
2. Build a privilege and asset map to anchor the rest of the review.
3. If prior findings exist, convert them into a regression matrix before fresh bug hunting and classify each as fixed, still valid, changed form, or unresolved.
4. Route the package to the relevant checklist topics and skip the rest explicitly.
5. Trace critical state transitions instead of reasoning from isolated lines.
6. Test attacker-controlled reachability and function composition paths.
7. Validate each candidate against the evidence standard appropriate to its severity: exploitability for higher-impact findings, or concrete security and operational downside for lower-severity findings.
8. Run a false-positive pass that tries to disprove every remaining candidate.
9. Assemble the final report using validated findings and code-backed lower-severity review notes.

## Working Style

- Read code before theorizing.
- Print the banner from `references/banner.txt` once near the start of the audit before the substantive review begins.
- Prefer package-wide reasoning over isolated lint-style comments.
- Use `references/checks/check-router.md` for depth and coverage, not as a substitute for code-backed reasoning.
- Execute the full audit flow autonomously until the final report file has been written unless a critical input is missing or the target is ambiguous.
- Keep this skill source-first.
- If prior audit reports or known findings exist, build a concrete regression checklist from them before concluding that a subsystem is safe.
- Treat the historical regression checklist as a blocking deliverable, not a best-effort note. Do not finalize coverage or the report until every prior finding has an explicit `Fixed`, `Still Valid`, `Changed Form`, or `Unknown` outcome with code-backed justification.
- Do not let early wins in one module starve equally critical neighboring modules of review depth; rebalance coverage before finishing.
- Treat localized new checks as evidence to verify, not proof that the whole call chain is now safe.
- During candidate validation, prefer direct evidence from reachable call paths, object flow, capability flow, and broken invariants instead of speculative reasoning.
- Do not discard a well-supported issue solely because it is medium, low, or informational. Only discard it when the code does not support it or it is irrelevant to security or defensibility.
- If dynamic verification is not feasible because the package lacks a runnable test setup, the path depends on non-local environment state, or the proof would be misleading, state that limitation explicitly and fall back to source-backed validation.
- If a temporary draft such as `.codex-report-draft.md` is created in the audit target while assembling the final report, delete it before finishing so only the intended final output remains.
- Call out uncertainty explicitly when assumptions about off-chain components, package deployment, or governance are missing.

## Invocation

Explicit skill invocation inside Codex uses `$sui-move-auditor`.

The wrapper should start Codex in the target project and use this skill to generate `{project-name}-exvul-sui-move-audit-report.md` in the current Codex workspace root by default.
