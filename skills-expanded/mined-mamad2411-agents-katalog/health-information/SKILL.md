---
name: health-information
description: "Use when answering medical condition questions."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [health, medical, citations, research]
    category: research
    related_skills: [grounded-citations]
---

# Health information answers

Use when the user asks what a condition is, what it implies, how it is treated, or how to tell it apart from a look-alike (irritation vs allergy, wellness label vs disease).

Do not use for first-aid instructions in an active emergency — tell them to get emergency care first.

This skill is **how to answer**. Condition-specific notes live in `references/`. Pair with `grounded-citations` in **fact-checking / evidence mode**.

## Procedure

1. Treat the answer as educational, not a diagnosis or a dose plan. Say that once, then stop hedging.
2. Load `grounded-citations`, reset the ledger, and retrieve **primary clinical sources** before writing:
   - NIH institute pages (NIDDK, NHLBI, NCI, MedlinePlus)
   - Academic centers (Mayo Clinic, Cleveland Clinic)
   - The relevant specialty society patient page or guideline (Endocrine Society, AHA, IDSA, …)
3. Skip wellness blogs, supplement marketing, and “adrenal fatigue” / functional-medicine summaries as authorities.
4. Structure the answer by **implication**, not encyclopedia dump:
   - what hormone/organ/system actually fails
   - everyday effects if untreated or under-treated
   - the emergency presentation (and when chat is the wrong tool)
   - what living with treatment changes
   - what the label is **not**
5. Attach verbatim quotes from extracted pages; `verify --evidence` before delivering. Cite inline; render the Sources block from the ledger.
6. If a trailing token looks like a person, lab, or paper (e.g. a last name after the question), say you answered the general case and offer to map it onto that case.

## Pitfalls

- **Kanban cwd is not a medical task.** A workspace under `kanban/workspaces/` does not mean you should run worker-ops unless the user asked about the board.
- **Do not invent incidence, doses, or “life expectancy” numbers.** Only quote figures the extracted page actually states.
- **Crisis language belongs in the answer, not as theater.** Name the emergency signs and point to emergency care; do not walk through unprescribed injection technique.

## References

- `references/adrenal-insufficiency.md` — primary vs secondary vs tertiary; crisis; replacement implications (NIDDK / Mayo / Endocrine Society / Cleveland Clinic)
