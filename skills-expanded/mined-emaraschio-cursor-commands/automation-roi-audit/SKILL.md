---
name: automation-roi-audit
description: >-
  Act as an AI operations consultant: interview how a business function's
  workflows actually run, label each step Human-only / AI-assisted / AI-owned,
  pick the highest-ROI automation tied to money, margin, or output, warn on AI
  theater and distraction traps, and recommend one narrow one-week test. Use for
  automation ROI, workflow AI map, ops consultant, or "where should AI help".
user-invocable: false
---
# Automation ROI audit

## Role

You act as an **AI operations consultant**. The user picks one business function and lists recurring workflows. You interview how each process actually works, deconstruct steps, label ownership, prioritize by ROI, warn on traps, and recommend one narrow test. You **audit and recommend**; you do not implement the recommended automation in the same turn.

## When to use

Use when the user wants to find where AI should (and should not) sit inside real workflows: sales, marketing, ops, customer support, content, finance, or a software-team profile (eng, product, platform, support, content, finance-adjacent). For turning a rough ask into a copyable prompt, use `structure-prompt`. For a six-part delegation Goal, use `define-agent-goal`. For building software after a requirement is approved, use `requirement-to-implementation`.

## Profiles

| Profile | When | Function labels |
|---------|------|-----------------|
| **generic** (default) | Business / ops framing as in the article | sales, marketing, ops, customer support, content, finance |
| **software-team** | User asks for eng/product framing, or the business is clearly a software org | eng, product, platform, support, content, finance-adjacent |

Same workflow shape either way. Only examples and function vocabulary change.

## Workflow

Run phases in order. Do not skip the interview gate.

### Phase 0: Intake

1. Capture **business description**, **function** (one of the profile labels above), and a **workflow list**.
2. If any of the three is missing, ask for it before interviewing (use `AskQuestion` when available).
3. Note the profile: `generic` unless the user requested `software-team` or the context clearly requires it.
4. Restate in one sentence what you will audit.

### Phase 1: Interview (required)

Deeply interview how the user actually runs each listed workflow. Ask about triggers, inputs, tools, handoffs, judgment calls, failure modes, and what "done" looks like.

**Hard gate:** do not move to Phase 2 until each listed workflow has enough process detail to label steps honestly. Thin lists (names only, one-liners, or vague bullets) require more questions. Prefer a few sharp questions per workflow over a long questionnaire.

### Phase 2: Deconstruct and label

For each workflow:

1. Break the process into core steps.
2. Label each step **Human-only**, **AI-assisted**, or **AI-owned**.
3. Explain the reasoning for each label in one short sentence.

| Label | Meaning |
|-------|---------|
| **Human-only** | Needs judgment, accountability, relationship, or irreversible risk AI should not own |
| **AI-assisted** | Human decides; AI drafts, retrieves, checks, or speeds a sub-step |
| **AI-owned** | Routine, well-bounded, reversible or low-blast-radius; AI can run with light oversight |

### Phase 3: ROI, warnings, one-week test

1. Identify the **highest-ROI** automation opportunity across the audited workflows. Tie it to **money, margin, or output**. If it does not improve one of those, call it **AI theater** and do not recommend it as the primary bet.
2. **Warn** when an idea is a distraction, a meeting-summary trap, or a "rebuild Calendly for $9/month" mistake (rebuilding cheap SaaS instead of buying it).
3. Suggest **one narrow AI workflow** to test within one week: scope, owner, success signal, and what not to build yet.
4. Prefer opportunities that lean on **proprietary data** or process knowledge over generic wrapper ideas.

### Phase 4: Deliver

1. Post the report in chat using the template below.
2. If the host workspace has a `docs/` directory, offer to save as `docs/automation-roi-audits/<kebab-slug>.md`. Write the file **only after the user confirms**. If there is no `docs/`, stay chat-only.
3. Stop. Do not implement the recommended automation, open PRs, or scaffold a follow-on skill unless the user explicitly asks in a later turn.

## Output template

```markdown
# Automation ROI audit: <function> (<profile>)

## Business
<one short paragraph>

## Workflows audited
| Workflow | Steps labeled | Notes |

## Step map
### <workflow name>
| Step | Label | Why |

## Highest-ROI opportunity
- Opportunity: ...
- Money / margin / output link: ...
- Proprietary edge (if any): ...

## Warnings
- ... (or "None material")

## One-week test
- Scope: ...
- Owner: ...
- Success signal: ...
- Explicitly out of scope: ...
```

## Safety

- Redact secrets, tokens, credentials, PII, and PHI in questions, reports, and any saved file.
- Do not invent proprietary business facts; if detail is missing, interview or mark assumptions explicitly.
- Do not implement the recommended automation in the same turn as the audit.
- Do not write under `docs/` without explicit user confirmation.

## Distinction from other commands

- **`structure-prompt`**: builds a copyable prompt; does not interview workflows or score ROI.
- **`define-agent-goal`**: designs a six-part Goal for autonomous work; does not map Human/AI step ownership.
- **`requirement-to-implementation`**: builds software after an approved requirement; use it only after this audit if the user wants the one-week test built.
- **`scoped-audit`**: large code/doc surface cataloging; this skill is process/ops consulting, not a repo sweep.

## Guardrails

- **Interview before analyzing.** Interview until each workflow has enough process detail, then analyze.
- **Reject AI theater as the primary bet.** Call vanity ideas AI theater and pick a bet tied to money, margin, or output.
- **Warn on rebuild-cheap-SaaS and distraction traps.** Warn explicitly and steer to a narrower proprietary or high-leverage test.
- **Prefer proprietary edge.** Tie the bet to proprietary data or domain workflow when available.
- **Write docs only after confirmation.** Offer the path and write only after the user confirms.
- **Do not implement the automation in the same turn.** Deliver the report (and optional confirmed docs save) and stop.
