---
name: style-memory-and-revision-gate
description: Use before delivering dissertation documents, proposal drafts, supervisor notes, or major chat answers when the user's preferred output style matters, especially to apply decision-first structure, two-track Thinking Pack/Decision Brief patterns, prohibited-phrase checks, and revision accountability.
---

# Style Memory And Revision Gate

Use this skill as a final language and structure gate for dissertation outputs, especially after drafting or revising proposal, methodology, ethics, supervisor-facing, or knowledge-base documents.

## Purpose

Make outputs match the user's established preferences without weakening academic rigour.

## Style Memory

Default chat answer:

1. Conclusion or recommended action first.
2. Two to four key reasons.
3. Necessary explanation only when it affects the judgement or next action.
4. Clear next step or `待确认`.

Default Chinese explanation:

- Lead with the usable answer, decision, or recommended action.
- Give compact reasons after the decision.
- Use examples only when they change the user's next action.
- Avoid long lists of rejected options before the answer.
- Keep wording direct and practical.

Major dissertation planning output:

- Create a `Thinking Pack` when the user needs to think through route, gap, methodology, or supervisor questions.
- Create a `Decision Brief` when the user needs a quick recommendation or supervisor-facing summary.
- Use both when the task is substantial and the user has not asked for only one format.

Document revision output must state:

- what changed
- why it changed
- where the new file is
- what still needs confirmation

## Pre-Delivery Gate

Before sending the answer or document summary:

1. Check that the recommendation appears before extended reasoning.
2. Remove generic AI-style phrasing.
3. Remove repetitive meta-commentary about the user's intentions.
4. Keep weak alternatives only if they help the decision.
5. Check whether formal writing also needs `uk-academic-writing-style`.
6. Check whether formal documents also need `dissertation-source-first-gate` and `dissertation-document-quality-gate`.
7. If the user wants journal-informed style, check the contribution box: problem, gap, method, contribution, boundary, implication.

For generated files, apply the style gate to the file text, not only to the final chat summary:

- scan the source Markdown or extracted document text before Word conversion or delivery;
- check Chinese explanation sections, bilingual drafts, captions, and callout boxes;
- treat negative-contrast phrasing as a delivery-blocking issue when the user's preferred style requires direct recommendation-first wording;
- rewrite the affected sentence before rendering whenever the file is intended for the user, supervisor, or later proposal work.

## De-AI And Style Checklist

For Chinese chat answers, remove or rewrite:

- empty closing formulas
- cliché balance phrases
- vague academic filler
- binary contrast phrasing that denies one framing before switching to another
- claims about what the user "really wants"
- repeated setup sentences before the answer
- overlong exclusion lists when the useful answer can be given first

For English dissertation prose, check:

- British English spelling and phrasing
- cautious academic stance: `suggests`, `may`, `is likely to`, `can be understood as`
- no inflated claims beyond the evidence
- no generic AI transitions such as `in today's rapidly evolving landscape`
- no excessive signposting when one clear sentence works
- no unnecessary em dashes when a comma, semicolon, or clause is cleaner
- no detector-evasion framing, AI-score promises, or disclosure hiding; use `authorial-voice-integrity` for those requests

For supervisor-facing writing, prefer:

- precise research language over motivational language
- decision and rationale over broad concept explanation
- unresolved items labelled as `TO CONFIRM`

## Two-Track Output Rule

When the user needs both thinking support and a decision:

- `Thinking Pack`: explains the problem space, options, evidence boundary, and questions to discuss.
- `Decision Brief`: gives the recommended route, 2-4 reasons, and immediate next action.

When the user asks for a concise answer, skip the `Thinking Pack`.

## Revision Accountability

For revised files, report:

```text
Changed:
- ...

Reason:
- ...

File:
- ...

待确认:
- ...
```

## Guardrails

- Do not compress away evidence boundaries, source uncertainty, ethics cautions, or unresolved fields.
- Do not use style rules to bypass citation checks.
- Do not use style rules to bypass AI-use disclosure or detector-evasion boundaries.
- Do not claim a document is submission-ready unless evidence, formatting, and unresolved fields have been checked.
