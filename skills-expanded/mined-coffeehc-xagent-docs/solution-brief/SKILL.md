---
name: solution-brief
description: Use when creating, rewriting, comparing, or reviewing a concise solution brief that aligns stakeholders on a proposed product, workflow, technical, operational, or business solution before detailed specification. Prefer this Skill when the output needs problem recap, proposed approach, essential capabilities, success metrics, trade-offs, risks, open questions, decision asks, or next steps.
meta:
  version: 2
  display_name: 方案简报
  source: product-on-purpose/pm-skills develop-solution-brief; product-on-purpose/pm-skills prioritized-action-plan and iterate-pivot-decision
  license: Apache-2.0
---

# Solution Brief

## Purpose

Create a production-ready solution brief that explains what problem is being solved, what solution is proposed, why this approach is reasonable, what trade-offs are accepted, and what must happen next.

This Skill adapts the open-source `develop-solution-brief` candidate for XAgent. It removes pm-skills runtime assumptions and treats the brief as an evidence-backed artifact, not a command workflow.

## Use When

Use for:

- Pitching a proposed solution to stakeholders for review, buy-in, or decision.
- Aligning product, engineering, design, operations, sales, leadership, or clients on a shared approach.
- Turning discovery notes, research, meeting outcomes, tickets, incidents, or rough proposals into a one-page solution overview.
- Comparing multiple solution options before writing a PRD, implementation plan, roadmap item, or project charter.
- Deciding what solution direction is most reasonable when options, constraints, risks, and unknowns need to be explicit.
- Reviewing an existing solution brief for unclear scope, weak metrics, missing trade-offs, or unsupported claims.

## Do Not Use When

Do not use for:

- XAgent platform architecture or product self-description. Use the project architecture and product docs directly instead of this Skill.
- Broad market, competitor, or literature synthesis where no solution is being proposed; use `research-synthesis`.
- Recurring status reports; use `weekly-report`.
- Meeting records or communication-heavy updates; use `meeting-recap` for recaps or `internal-comms` for internal announcements.
- Full PRDs, technical designs, legal approvals, procurement decisions, or final implementation plans unless the user explicitly asks for a brief version first.
- Sending, publishing, or approving the proposal. This Skill drafts and reviews content only.

## Material Gate

Before drafting, identify:

- Problem: who is affected, current pain, impact, urgency, and source material.
- Proposed solution: target user/customer, core experience, operating model, or change being proposed.
- Scope: in scope, out of scope, alternatives considered, and non-goals.
- Success metrics: baseline, target, timeline, measurement owner, and confidence.
- Constraints: budget, timeline, staffing, dependencies, compliance, data, platform, customer, or rollout limits.
- Decision context: intended audience, decision ask, required approvals, open questions, and next artifact.

If a key fact is missing, preserve the brief shape and mark `待确认`. Do not invent metrics, baselines, customer commitments, owner names, dates, approvals, or implementation feasibility.

## Workflow

1. Classify the brief mode: product solution, technical solution, operational process, business initiative, customer-facing proposal, or option comparison.
2. Read the provided source material before writing. Keep source-backed facts separate from inference.
3. Normalize inputs into this evidence model:
   - problem recap
   - proposed solution
   - key capabilities
   - success metrics
   - trade-offs and non-goals
   - risks and mitigations
   - open questions
   - decision ask and next steps
4. If multiple options exist, compare them with shared criteria before recommending one.
5. Identify the binding constraint or critical next unknown when prioritization matters; do not pretend every action is equal.
6. Use `references/brief-patterns.md` for mode-specific guidance, option comparison, decision quality, metric rules, and review checks.
7. Use `templates/solution-brief.md` only when the user wants a durable Markdown artifact or a consistent reusable structure.
8. Write in the user's language by default. Use plain language for business readers and include technical detail only when it affects feasibility, risk, scope, or decision quality.
9. Make trade-offs explicit. State what is not being done and why.
10. Put the decision ask, priority, or next step where a busy reviewer can find it.
11. Validate against the checks below before finalizing.

## Checks

- The problem recap names the affected audience, pain, and impact.
- The proposed solution is understandable without implementation deep-dive.
- Key capabilities are limited to the minimum needed for the solution to work.
- Option comparisons use the same criteria for all options.
- Metrics include baseline, target, timeline, or are marked `待确认`.
- Trade-offs include rejected alternatives, non-goals, or deliberate scope limits.
- Risks include likelihood, impact, and mitigation when known.
- Open questions are separated from decisions already made.
- Next steps are prioritized when the user needs action, not just listed.
- External-facing briefs do not expose internal-only details, unapproved roadmap, private staffing issues, or unsupported commitments.
- Review comments distinguish missing evidence from subjective style preferences.

## Outputs

Produce one or more of:

- solution brief
- one-page proposal
- option comparison brief
- executive solution summary
- customer-facing proposal draft
- trade-off and non-goal section
- risk and mitigation section
- prioritized next-step rationale
- review notes for an existing solution brief
- Markdown artifact content ready for XAgent artifact tools

Use the user's requested format. Do not force the template when the user only needs option reasoning or concise advice.

## Recovery

If evidence is weak, produce a constrained draft with a `待确认` section and source-quality notes. If multiple options are present but no preferred solution is clear, produce an option comparison and recommend a decision criterion instead of pretending one option is approved.

If the user asks for a full PRD, architecture design, or implementation plan but provides only solution-brief-level material, first create the brief and list the missing inputs needed for the larger artifact.

## Boundary

Skill owns solution-brief workflow, artifact structure, source discipline, audience framing, option comparison, trade-off writing, risk framing, metric quality checks, and review guidance.

It does not own XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, product approval, technical feasibility approval, legal/compliance approval, budget approval, external customer commitments, document export, or message sending. It must not run shell, Python, Node, curl, project-management, email, CRM, analytics, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/brief-patterns.md`: mode-specific brief patterns, option comparison, metric quality, risk/trade-off rules, and review checklist.
- `templates/solution-brief.md`: production Markdown template for a source-backed solution brief.
- `examples/solution-brief-example.md`: example output shape adapted from the upstream candidate.
- `LICENSE`: source and license notice.
