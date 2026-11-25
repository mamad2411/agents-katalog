---
name: product-discovery
description: Use when exploring or validating a product idea, user problem, persona, JTBD, MVP, feature opportunity, user interview plan, experiment, prototype scope, or product-market fit question. Prefer this Skill when the task needs problem clarity, user assumptions, discovery questions, risks, evidence, and learning plan before writing requirements. Do not use for implementation-ready PRDs; use product-requirements after the product direction is chosen.
meta:
  version: 1
  display_name: 产品发现
---

# Product Discovery

## Purpose

Clarify user problems, assumptions, evidence, and MVP learning goals before committing to product requirements or implementation.

## Use When

Use for:

- product idea exploration
- user problem framing
- persona and JTBD work
- discovery interview planning
- MVP scope
- assumption mapping
- product-market fit questions
- experiment planning

## Material Gate

Identify:

- target user, context, problem, current workaround, and desired outcome
- business goal and constraints
- evidence already available
- riskiest assumptions and learning deadline

If no user or problem is named, start there before proposing features.

## Workflow

1. Separate problem, user, solution, and business assumptions.
2. Describe the user's job, trigger, pain, workaround, and success outcome.
3. Identify evidence and gaps.
4. Prioritize assumptions by risk and uncertainty.
5. Design discovery questions, interviews, prototype tests, or smoke tests.
6. Define MVP as the smallest learning loop, not the smallest feature list.
7. Use `product-requirements` only after direction is selected.
8. Use `html-report-builder` for discovery reports or opportunity maps.

## Checks

- User problem is not just a feature request.
- MVP has a learning goal and success metric.
- Assumptions are testable.
- Discovery questions are not leading.
- Requirements are not written prematurely.

## Outputs

- opportunity brief
- persona/JTBD summary
- assumption map
- discovery interview guide
- MVP learning plan
- experiment plan
- product discovery report

## Boundary

This Skill owns discovery framing, assumption mapping, and learning plan design. It does not own final PRD approval, engineering design, user research recruiting, analytics instrumentation, or product launch decisions.

It must not run shell, Python, Node, npm, curl, MCP, research panel, analytics, Figma, CRM, email, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
