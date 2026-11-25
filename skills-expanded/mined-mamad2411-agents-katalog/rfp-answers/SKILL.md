---
name: rfp-answers
description: Answer RFP and client security or functional questionnaires from an approved answer bank, with compliance status, sized answers and a gap log. Use when the user asks to fill an RFP, answer a security questionnaire, RFI, vendor assessment or DDQ.
---

# RFP & Questionnaire Answers

## Inputs
- Questions: pasted list, Excel/CSV rows, or PDF text (keep the client's question IDs)
- `references/answer-bank.md`: approved product facts (the only source of truth)
- Optional: client-specific notes from the user, previous answers to the same client, word/character limits per question

## Defaults (state them in the output if used)
| Setting | Default | Options |
|---|---|---|
| Answer length | Tier S (per-question limit wins) | S · M · L, see `references/answering-guide.md` |
| Product / module | As named in RFP; else "TBD" | From answer bank |
| Deployment model | As in answer bank | Only values filled there |
| Output | Answer table + gap log | Also CSV-ready rows if input was a sheet |

Ask **one** question only if the product or module in scope is unclear. Otherwise use defaults and state them.

## Steps
1. Read all questions; keep each question ID and wording exactly; number any without an ID as Q-1, Q-2 in order.
2. Classify each question by topic (Security, Hosting, Integration, Functional, Support/SLA, Commercial, Company) and pick the length tier.
3. Look up each question in `references/answer-bank.md`. Use only filled entries, or facts the user states in this request; any entry still marked TO FILL counts as missing.
4. Assign a compliance label (Yes / Partial / Roadmap / No / Needs input) by the rules in `references/answering-guide.md`.
5. Write the answer: label first, then the approved fact, reworded only for fit; cite the bank entry ID.
6. When no approved fact exists, do not answer from general knowledge: label **Needs input**, draft nothing factual, and add a gap-log row.
7. Keep answers to repeated or similar questions identical in substance (same label, same facts).
8. Fill `templates/answer-sheet-template.md` (answer table, then gap log).
9. Run the self-check and fix before returning.

## Format
Use `templates/answer-sheet-template.md`: Summary counts by label, Answer table (Q-ID · Question · Status · Answer · Source), Gap log (Q-ID · Missing fact · Suggested owner · Needed by).

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never invent capabilities, certifications, audit dates, numbers (uptime, RPO/RTO, users, TPS), customer names or roadmap dates.
- Use only filled answer-bank entries or facts the user states in this request (cite "User note" and log them in the gap log for adding to the bank); TO FILL entries count as missing.
- Keep client question IDs and product names exactly as given.
- Label first, then answer. "Yes" needs a fact from the bank that fully meets the question.
- "Roadmap" only if the bank lists it as roadmap; never give a date the bank does not give.
- Never name other clients as references unless the bank marks them approved for reference.
- No marketing filler ("best-in-class", "world-class", "seamless").
- Every Needs input and every Partial answer appears in the gap log.

## Self-check
- [ ] Every question answered or labelled Needs input; none skipped
- [ ] Every Yes / Partial / Roadmap cites a filled bank entry
- [ ] No fact that is not in the bank or the user's notes
- [ ] Similar questions have consistent labels and facts
- [ ] Answer lengths within tier or the client's limit
- [ ] Gap log lists every Needs input and Partial

## Output
Return the summary, the answer table and the gap log, then an **"Assumptions & Needs input"** block (defaults used, product scope, bank entries still TO FILL that blocked answers).

Benchmark after edits with `evals/test-cases.md`.
