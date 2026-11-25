---
name: bot-template
description: One sentence on what this produces, then the triggering phrases. Use when the user asks to <phrase>, says <phrase>, or wants <outcome>. This text is the routing logic Cowork matches a request against, so write it for the matcher and not for a reader.
---

# <Bot name>

<One line: the repeatable outcome this owns. Not a category.>

## Inputs

- What the user supplies, if anything
- Which built-in skills this reads through: Email, Enterprise Search, Meetings, Deep Research,
  Calendar Management, Excel, Word
- Which config file it reads, if any

## Config the user edits

Read `references/config.md` at the start of every run. If it is missing, say so once and continue
with the defaults below rather than failing.

- Thresholds, VIP names, project names, the window in days
- Never hard-code a person, a project or a number into these instructions

## Procedure

Be concrete. "For each thread, return sender, the ask, the deadline and the source link" is a
procedure. "Analyse the inbox thoughtfully" is not.

1. Gather: <exact sources and the exact window>
2. Filter: <the rule that decides what is in and what is out>
3. For each item, extract: <named fields>
4. Rank by: <the stated rule>
5. Write the output to: <exact path and filename pattern>

## Output

Reproduce the exact structure. Every factual line carries a link to the item it came from.

| Column | Column | Source |
|---|---|---|

- State facts and inferences separately. Label anything inferred.
- If a figure came from a document, the document is the source of truth, not this output.
- Mark the whole artifact DRAFT.

## Definition of done

Say plainly what finished looks like, and what the success state is when there is nothing to
report. Silence is a valid and good outcome: a bot that manufactures a finding to look useful
trains its reader to ignore it.

## When there is no data, or stale data

- No matching items: say so in one line and stop. Do not widen the window to find something.
- A source is unavailable: report the failure. Never fall back to older data silently.
- Partial results: say which source was missing and what that omits.

## Boundaries

- Draft only. Never send, post, delete, accept or decline anything without explicit approval.
- Never share outside the organisation.
- Never state a figure as authoritative. The system of record is.
- <Any job-specific prohibition>

## Self-check before returning

- Does every factual line carry a source link?
- Are inferences labelled as inferences?
- Did I stop at the approval boundary?
- If I found nothing, did I say so rather than padding?
