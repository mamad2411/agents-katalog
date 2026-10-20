---
name: requirements-to-stories
description: Turn client requirements, emails or a BRD into epics and user stories with Gherkin acceptance criteria, INVEST check, points hint, open questions. Use when the user asks to write user stories, create a backlog, break down a BRD, or make Jira stories.
---

# Requirements to Epics & User Stories

## Inputs
- Client email, meeting notes, BRD/FRD extract, RFP clause, change request
- Existing backlog or Jira export (optional, to avoid duplicates and reuse IDs)
- Glossary or process flow (optional)

Several sources: merge. When they conflict (e.g. email vs BRD), prefer the later-dated source and flag the conflict under Open questions.

## Defaults (ask vs assume)
| Setting | Default if not stated | Options |
|---|---|---|
| Output | Markdown tables | Markdown · Jira CSV (`templates/jira-import.csv`) · both |
| Personas | Derived from input (e.g. Forwarder, GHA agent, Airline ops, Customs broker, Admin) | User-supplied list |
| Estimation | Fibonacci points hint (1,2,3,5,8,13) | T-shirt · none |
| Granularity | Stories fit one sprint (≤ 8 pts) | User rule |

Ask one question only if the requirement is too vague to name a persona or outcome. Otherwise assume and state the defaults.

## Steps
1. Read all input once. List every distinct requirement statement with a source ref (REQ-01, REQ-02, or the client's own IDs).
2. Group requirements into epics by business capability (e.g. "AWB booking", "e-DO issuance"), not by screen or team.
3. Write stories: As a PERSONA, I want CAPABILITY, so that BENEFIT. One user goal per story.
4. Add 2–5 Gherkin acceptance criteria per story (Given / When / Then), covering the happy path plus at least one negative/validation case. See `references/story-rules.md`.
5. Run the INVEST check per story; split any story that fails I, S or T using the splitting patterns in `references/story-rules.md`.
6. Add a story-point hint with a one-line reason (complexity, integrations, unknowns).
7. Record dependencies (other stories, external systems like airline host, customs gateway, payment) and non-functional needs (performance, audit, security).
8. Collect open questions: every gap, ambiguity, or assumption.
9. Write output with `templates/story-template.md`; if Jira CSV is requested, also fill `templates/jira-import.csv`. See `templates/example-stories.md` for a filled example (fake data).
10. Run the self-check and fix before returning.

## Format
Use `templates/story-template.md`: Epic list, then per-epic story table, then Gherkin blocks, INVEST table, Dependencies, Traceability (REQ to story), Open questions.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never invent business rules, limits, fees, SLAs or field names. Put them in Open questions.
- Keep client requirement IDs, field names, message types (FWB, FHL, FSU) and codes exactly as given.
- Story titles: verb + object, ≤ 8 words.
- "So that" states a business benefit, never "so that I can use the feature".
- No technical tasks as user stories; list them as Tasks under the story.
- Every requirement maps to at least one story, or is marked Out of scope with a reason.
- Points are a hint, labelled "hint"; never present them as a commitment.
- Jira CSV: one row per issue, commas escaped, epics before stories.

## Self-check
- [ ] Every REQ appears in the traceability table
- [ ] Every story has persona, want, benefit, 2–5 Gherkin criteria incl. one negative
- [ ] INVEST failures split or flagged
- [ ] No invented rules or numbers; all gaps in Open questions
- [ ] IDs and terms unchanged from input
- [ ] CSV (if produced) parses: same column count every row

## Output
Return the stories (and CSV if asked), then an **Assumptions & Needs input** block: defaults used, assumptions made, open questions with suggested owner (client / BA / tech).

After edits to this skill, rerun `evals/test-cases.md`.
