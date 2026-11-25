---
name: defect-intake-triage
description: Turns a reported problem in mail or Teams into a structured, ticket-ready intake with the evidence attached and the gaps named, then an Adaptive Card for approval before anything is filed. Use when the user asks to triage a bug report, turn a complaint into a ticket, prepare a defect for filing, or says a user reported a problem.
---

# Defect Intake and Triage

Turns "it's broken" into something an engineer can act on, or says exactly what is still missing.

🔴 **This does not reproduce anything.** Reproduction needs a terminal, a staging environment and
arbitrary browser control, none of which Cowork has. The portable half of a bug-reproduction
pattern is the **intake and handoff**, and that is all this does. The card says so to the reader.

## Inputs
- The report itself, from **Email** or Teams
- **Enterprise Search** for prior reports of the same thing, and for the owning team
- `references/config.md` for the required intake fields and the severity vocabulary

## Procedure
1. **Extract the report** into the required fields from config: what was expected, what happened,
   when, who, which system, which environment, how often, and what evidence is attached.
2. **Mark every field that is absent MISSING** and generate the one question that would fill it.
   A triage whose output is three precise questions is more useful than one that guesses.
3. **Search for duplicates**: prior reports with the same system and symptom. Link them. Say
   "possible duplicate" and never "duplicate", because that call belongs to the owning team.
4. **Identify the owning team** from evidence: who owns the system in documents or who answered
   prior reports. Mark UNKNOWN rather than guessing.
5. **Assign a severity** only if the config vocabulary has an evidenced rule for it. Otherwise
   leave it unset and say why.
6. **Produce an Adaptive Card** with the full intake, the missing fields, the possible duplicates
   and the proposed owner, for the user to approve before anything is filed.

## Output
Adaptive Card carrying: the structured intake, MISSING fields with the question for each, possible
duplicates with links, proposed owning team, and the proposed ticket title and body.

## Definition of done
Every required field is filled or MISSING-with-a-question, duplicates are linked, and nothing was
filed.

**A triage that concludes "not enough information, here are the three questions" is a success.**
It is better than a ticket an engineer closes as unreproducible.

## When there is no data
- The report is one sentence: produce the questions. Do not pad the intake with assumptions.
- No owning team found: UNKNOWN, and say what you searched.
- Evidence referenced but not attached: list it as evidence to request.

## Boundaries
- **Never file, create, assign or comment on a ticket without approval.** Filing requires a work
  tracker plugin and the user's explicit go.
- **Never attempt reproduction.** No terminal, no staging, no browser steps.
- Never declare a duplicate, a root cause or a severity the config does not support.
- Never include customer identifiers in a ticket body unless the user approves.

## Self-check
- Is every missing field paired with the question that would fill it?
- Did I say "possible duplicate" rather than "duplicate"?
- Did I avoid claiming any reproduction?
