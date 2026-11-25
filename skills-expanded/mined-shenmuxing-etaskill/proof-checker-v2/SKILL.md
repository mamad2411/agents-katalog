---
name: proof-checker-v2
description: Independent DeepSeek-backed adversarial proof-audit step for existing theorem, lemma, proposition, or proof artifacts in Markdown, LaTeX, or proof logs. Use when asked to check, audit, verify, red-team, or adversarially review a proof; when a completed proof task needs a correctness pass; or when a broader proof workflow dispatches an independent reviewer to find gaps, hidden assumptions, counterexamples, or unjustified steps.
---

# Proof Checker V2

Audit an existing proof as an independent verification step. Prefer a precise
blocker over an optimistic repair.

## Operating Contract

Treat this skill as one reviewer step in a larger proof workflow.

- Do not spawn additional agents from inside this skill unless the user explicitly requests nested review.
- Use DeepSeek as the external reviewer when a DeepSeek route is available. Prefer an MCP bridge such as `llm-chat`; use `deepseek-agent` only as fallback.
- Do not edit source proofs unless the user explicitly asks for a patch. Produce an audit, suggested fixes, and optional replacement statements.
- Do not silently strengthen assumptions or weaken conclusions. Label every such move as a proposed repair.
- Do not accept "clearly", "standard", "by symmetry", or "it follows" unless the missing obligation is genuinely trivial under stated assumptions.
- Use project-local source files before outside memory. If source support is missing, mark the claim as unverified.
- In Markdown notes, use `$...$` and `$$...$$` math delimiters.

## Inputs

Accept any of:

- a named theorem, lemma, proposition, proof sketch, `.md`, or `.tex` file;
- a completed proof-task artifact such as `proof-logs/tasks/<TASK_ID>.md`;
- a request to audit a section of a paper or note.

If the target is ambiguous, inspect nearby context and ask only when multiple
plausible targets would lead to different audits.

## Workflow

1. Locate the exact proof boundary: statement, assumptions, definitions, cited lemmas, and conclusion.
2. Restate the claim with explicit quantifiers, parameter domains, limit order, and dependencies of constants when relevant.
3. Build a lightweight obligation ledger:
   - hypotheses used at each application;
   - nontrivial micro-claims;
   - analytic interchanges and required side conditions;
   - asymptotic uniformity and hidden parameter dependence;
   - dependency and circularity risks.
4. Load `references/deepseek-routing.md` and send the audit brief to DeepSeek using the first available route.
5. Check DeepSeek's response against `references/audit-rubric.md`; do not accept unsupported issue labels or missing locations without review.
6. Attempt simple counterexamples for global or structural claims: one-dimensional collapse, degenerate parameters, boundary cases, and adversarial scaling.
7. Assign a verdict and write the audit using `references/output-contract.md`.

## Reviewer Route

Use these routes in order:

1. an installed DeepSeek MCP bridge, for example `mcp__llm_chat__chat`;
2. `deepseek-agent` with an answer-only result file;
3. local Codex audit only if both DeepSeek routes are blocked.

When using the local-only fallback, mark the saved audit as `BLOCKED` or `WARN`
with `reviewer_backend: "local-codex-fallback"` unless the caller explicitly
permits local-only verification.

Never write API keys into the repository. Do not run connectivity checks unless
the user asks or a proof-checker invocation needs them to complete the requested
audit.

## Verdicts

- `PASS`: The proof appears justified under the stated assumptions.
- `WARN`: Only minor or local gaps remain; the main conclusion likely survives.
- `FAIL`: A fatal or critical gap, false statement, circular dependency, or missing global assumption blocks the proof.
- `BLOCKED`: The target proof or required dependency cannot be read.
- `NOT_APPLICABLE`: No theorem or proof content is present.

Use the statuses `PROVABLE AS STATED`,
`PROVABLE AFTER WEAKENING / EXTRA ASSUMPTION`, and
`NOT CURRENTLY JUSTIFIED` when auditing a single theorem-like claim.

## Output Location

Follow the caller's requested destination. If none is given:

- For a proof task file, write beside it as `proof-logs/tasks/<TASK_ID>-audit.md`.
- For a broad proof-plan audit, update or create `proof-logs/PROOF_AUDIT.md`.
- For a one-off chat request, answer in chat and do not create files.
- For a formal paper workflow that explicitly expects an assurance artifact, write `<paper-dir>/PROOF_AUDIT.json` using the schema in `references/output-contract.md`.

## Final Response

Keep the final response short:

- verdict;
- most serious issue, if any;
- files written or updated;
- what remains unverified.

Load `references/deepseek-routing.md` before reviewer calls,
`references/audit-rubric.md` for detailed checks, and
`references/output-contract.md` before writing a saved audit.
