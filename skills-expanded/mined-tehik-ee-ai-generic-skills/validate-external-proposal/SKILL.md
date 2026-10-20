---
name: validate-external-proposal
description: >
  Use this skill whenever the user shares an external partner proposal, vendor offer, PoC description,
  architecture proposal, or any document from a third party that needs technical or business validation.
  Trigger even on casual phrasing: "can you check this offer", "what do you think of this proposal",
  "does this make sense technically", "review this solution from X", "is this vendor any good".
  Produces a structured assessment (strengths / risks / open questions / recommendation) aimed at an
  analyst or developer — not a legal or procurement decision.
---

# Validating an external proposal / solution

## When this applies

Use this skill when:
- The user shares an external partner proposal, vendor offer, or PoC description for review
- The user asks "can you check this offer", "does this make sense technically", "review this from X"
- Any document from a third party needs technical or business assessment

Do NOT use this skill for:
- Reviewing your own code or internal architecture decisions (use `/codebase-auditor` or your workflow's review phase)
- Legal or procurement decisions — this skill produces an analyst/developer assessment only

## Required inputs

The skill requires:
- **The proposal document** — text, markdown, or PDF content pasted into the conversation
- **What it replaces or enables** — the problem or capability gap the proposal addresses
- **Must-have requirements** (optional but helpful) — known functional, technical, or regulatory constraints to evaluate against

If the document is absent, stop and ask the user to provide it.

The user provides **input** (document, email, PDF as text, markdown) — partner proposal, PoC description, architecture proposal.

> This workflow is an **assessment for an analyst/developer** in an IDE context, not a legal or procurement decision.

---

## Step 0 — Gather context if missing

Before diving into the checklist, check whether the user has stated:
- What the solution is meant to replace or enable
- Any must-have requirements (functional, technical, regulatory)

If this context is absent from the document and the user's message, ask one focused question first:

> "What is this solution meant to replace or enable, and are there must-have technical or business requirements I should evaluate against?"

Once you have enough context (or if the proposal itself is self-contained), proceed.

---

## Checklist

> **Note:** Item 4 contains TEHIK-specific checks (X-Road, EHDS, national health data regulations). These are subject to change as regulations evolve. Verify the authoritative requirements against current legislation and internal TEHIK guidelines before using this checklist in a review.

1. **Clarity:** are scope, assumptions, and pricing points sufficiently precise?
2. **Requirements fit:** does the offering cover the user's stated business or technical requirements? Note any gaps explicitly.
3. **Technical soundness:** technology maturity, integration approach, scalability, security (OWASP, data residency, logging, access control).
4. **TEHIK-specific technical checks:**
   - X-Road compatibility — does the solution integrate with Estonia's data exchange layer, or does it bypass it?
   - Health data regulation — does the design respect EHDS and Estonian health data act constraints?
   - Public procurement implications — are there riigihangete seadus considerations (e.g., minimum competition, framework agreement eligibility)?
   - GDPR + national health data — health records are subject to stricter rules than standard GDPR; flag any gaps.
5. **Dependencies and lock-in:** vendor lock-in risk, license model, reliance on open vs. proprietary standards.
6. **Risks:** single-channel dependency, missing or weak SLA, hidden costs, organisational/support risks.
7. **Alternatives:** a brief list of other feasible approaches — no deep dive unless the user asks.

---

## Output

Produce markdown. Choose the right template based on your conclusion:

### Standard output

```markdown
# Validation summary: <short name>

## Recommendation
[Recommend / Do not recommend — one sentence with rationale]

## Strengths
- ...

## Weaknesses and risks
- ...

## Open questions for the partner
1. ...
2. ...

## Alternatives
- ...

## Next steps (optional)
- ...
```

### When recommendation is "Recommend with conditions"

```markdown
# Validation summary: <short name>

## Recommendation
Recommend with conditions

**Conditions that must be met before proceeding:**
- ...

## Strengths
- ...

## Weaknesses and risks
- ...

## Open questions for the partner
1. ...
2. ...

## Alternatives
- ...

## Next steps (optional)
- ...
```

### When input is insufficient (blocked)

```markdown
# Validation summary: <short name>

## Status: blocked

**Reason:** The provided input is too brief/incomplete to assess [specific dimension(s)].

**What's needed to proceed:**
- ...
```

Save to a user-specified file or — if working within **`/process-task-board`** — the same task's output directory.

---

## Limitations

- Do not invent the organisation's internal procedures, procurement law, or budget without user input.
- Do not make definitive legal or procurement rulings — flag concerns and recommend the appropriate specialist.
- If the input is too short or ambiguous, use the **blocked** template above rather than guessing.
