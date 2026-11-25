---
name: vibespec-gate
description: Review launch security for products built with vibe coding. Use only when explicitly invoked for a security, privacy, launch-readiness, authentication, authorization, secrets, database rules, deployment, AI Agent/tool, MCP/IPC, Electron, or desktop boundary review. Produce an evidence-qualified launch decision, high-impact risks, a human-gated repair plan, and project-specific retests without modifying the reviewed project.
---

# VibeSpec Gate

Review authorized project evidence and answer whether the product is ready to launch from a practical security and data-safety perspective.

## Required Inputs

- Confirm the project or evidence directory the user authorizes for read-only review.
- Identify product type, deployment stage, sensitive data, identity model, and Agent or local-system capabilities.
- Treat existing scanner output as supporting evidence, never as a complete review by itself.

Default to a chat-first result. Create files only when the user explicitly asks to save them and approves an output directory outside the reviewed project. Resolve both paths and reject equal, parent, or child overlap before any write.

Do not edit the reviewed project during the review. A later fix requires separate authorization after the user confirms the evidence and scope.

## Chat Output Contract

Use exactly one of these decision lines in every chat review: `Decision: BLOCK`, `Decision: REVIEW`, `Decision: PASS_WITH_WARNINGS`, or `Decision: PASS`. Do not replace the token with synonyms such as `FAIL`, `NO-GO`, `Blocked`, or `Launch Readiness`.

Report `Coverage: complete | partial | insufficient | truncated` before the decision, then list all seven review surfaces with evidence or a concrete reason for `not_applicable`, `missing`, or `truncated`. Empty, unavailable, or truncated evidence requires `Decision: REVIEW` unless the available evidence independently confirms a launch blocker; missing evidence alone is not a blocker.

Use these exact chat section headings after the decision: `Highest-Impact Risks`, `Missing Evidence`, `Limitations`, `Human Confirmation Required`, `Human-Gated Repair Tasks`, and `Project-Specific Retests`. `Limitations` must state the reviewed scope and anything the evidence cannot establish, including when coverage is complete. Keep complete credentials masked. Do not omit a required section; write `none identified` when a section has no supported item.

## Resource Routing

1. Read `references/review-protocol.md` before every review. Follow its evidence order, risk rules, decision precedence, and stop conditions.
2. Read `references/evidence-coverage.md` before assigning a launch decision. Record all seven review surfaces, including reasoned `not_applicable` entries.
3. When the user approves file output, copy and complete each template:
   - `assets/templates/launch-decision.md` -> `launch_decision.md`
   - `assets/templates/top-security-risks.md` -> `top_security_risks.md`
   - `assets/templates/agent-fix-plan.md` -> `agent_fix_plan.md`
   - `assets/templates/retest-checklist.md` -> `retest_checklist.md`
4. Store supporting machine-readable evidence under `evidence/` only when file output is approved. Treat it as potentially sensitive.

## Review Flow

1. Establish scope and inventory the available evidence. Record skipped, unreadable, or truncated files.
2. Review authentication, authorization, secrets, data rules, deployment, Agent/tool authority, and desktop/IPC boundaries as applicable.
3. Trace security claims to concrete files, lines, configuration, or an explicit missing-evidence statement.
4. Separate confirmed runtime risk from suspected, example, generated, test, or documentation-only evidence.
5. Apply the coverage gate before allowing a passing decision.
6. Return a compact chat result with coverage, decision, highest-impact risks, bounded repair tasks, and retests.
7. Stop after judgment and planning unless the user separately authorizes a fix.

## Decision Gate

- `BLOCK`: confirmed launch-blocking evidence exists. Incomplete coverage may still produce `BLOCK` when the blocker is confirmed.
- `REVIEW`: evidence is insufficient, partial, truncated, ambiguous, or requires human judgment.
- `PASS_WITH_WARNINGS`: coverage is complete and no blocker remains, but lower-priority risk or an accepted warning remains.
- `PASS`: coverage is complete, every review surface is reviewed or reasoned not applicable, and no material finding remains.

Never infer `PASS` from an empty finding list. Never report a numeric security score when coverage is incomplete.

## Finding Quality

For each actionable risk, provide severity, launch impact, affected files, evidence, plain-language impact, technical reason, confidence, recommended fix, allowed scope, prohibited changes, human confirmation, and verification steps. State what evidence would confirm or dismiss uncertain findings.

## Safety Boundaries

- Review only user-owned or explicitly authorized projects.
- Keep the review read-only unless the user gives separate fix authorization.
- Do not auto-fix, auto-suppress, broaden permissions, weaken validation, or mutate production systems.
- Do not print complete secrets, OTPs, reset tokens, JWTs, cookies, session IDs, or authorization headers.
- Do not provide exploit payloads, login bypass, brute force, credential theft, persistence, privilege escalation, or destructive testing instructions.
- Do not run dynamic or live-target tests without explicit scope authorization.
- Do not claim absolute security, professional certification, penetration-test equivalence, legal approval, or compliance attestation.
- Inspect generated reports manually before sharing because paths, snippets, and findings can be sensitive.

## Stop Conditions

Stop and ask for user input when authorization, target scope, sensitive-data handling, output location, or a product-policy choice is unclear. Mark unavailable evidence as missing and return `REVIEW`; do not silently assume it is safe.
