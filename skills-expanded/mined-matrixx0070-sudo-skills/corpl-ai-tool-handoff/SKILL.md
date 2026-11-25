---
name: corpl-ai-tool-handoff
version: 1.0.0
description: Package AI-generated corporate/M&A work product for a licensed attorney's review, with a clear provenance trail and an escalation gate.
author: matrixx0070
tags: [corporate-legal, handoff, review, provenance, escalation, diligence]
capabilities: []
---

## When to use

Use this whenever AI-assisted output — a diligence issues list, a draft consent, a contract schedule, a closing checklist — is about to leave the drafting stage and reach a lawyer, client, or counterparty. It converts an unreviewed draft into a reviewable package: what was done, on what inputs, with what open questions.

**Not for:** the drafting itself (use the specific corpl- skill); a document a supervising attorney has already reviewed and adopted; anything you intend to file or send without attorney sign-off. This skill never authorizes sending — it prepares the handoff.

## Method

1. **State the work product and its purpose.** One line: what it is, which deal/entity, and the decision it feeds.
2. **List every source input.** Documents, data-room folders, and facts relied on, with versions/dates. Mark anything reconstructed or assumed rather than sourced.
3. **Summarize what the AI did and did not do.** Extraction, drafting, comparison — and explicitly what was out of scope (no legal conclusions, no jurisdiction analysis unless stated).
4. **Flag every judgment call and gap** as an open question for the attorney, not a silent guess.
5. **Route to the escalation gate.** *Decision point:* any material risk, novel legal question, privilege issue, or missing consent → mark **attorney review required — do not send** and name the reviewer. No output goes to a client or counterparty without licensed attorney sign-off.
6. **Attach a confidence note** per section: high / needs-verification / unverified.

## Example

Handoff: "Target material-contract schedule (Project Harbor), feeds the disclosure schedule." Inputs: data-room folder 4.2 (as of 6/30), 41 agreements. AI did: extracted parties, term, assignment/CoC clauses into a table. Did not: opine on whether consents are required. Open questions: 6 contracts have ambiguous change-of-control language — flagged for counsel. Gate: attorney review required — reviewer: deal lead. Confidence: extraction high; consent-trigger analysis unverified.

## Pitfalls

- **Presenting a draft as final.** Every handoff is a draft until an attorney adopts it.
- **Hiding assumptions inside clean prose.** Reconstructed facts must be labeled.
- **Skipping the gate on "small" items.** A one-line consent can still bind the entity.
- **No source versions.** A schedule built on a superseded data-room set is worse than none.

## Output format

```
Handoff: <work product> — <deal/entity>
Purpose / decision it feeds:
Inputs (source — version/date):
AI did / did not do:
Open questions for attorney:
Confidence: <section> — high | needs-verification | unverified
GATE: attorney review required — reviewer: <name> | cleared by: <attorney>
```

## Reference

Handoff is the enforcement point for the attorney-escalation gate that every corpl- skill shares: AI output is drafting assistance, not legal advice, and reaches no external party without a licensed attorney's adoption. Preserve provenance so the reviewer can retrace every claim to a source. When work product may be privileged, mark it "Privileged & Confidential — Attorney Work Product" and restrict distribution to counsel.
