---
name: ticket-write
description: Draft and file short tickets (bug, task, story, spike, epic) that a business analyst or product owner can read in under a minute, with the engineering detail moved to a first comment. Use when the user wants to create, draft or file a ticket in Jira, Linear or GitHub Issues, or to turn findings from an investigation, incident or review into backlog items.
---

# Ticket write

A ticket has two readers. The **description** is for the person who prioritizes and accepts the work. The **technical notes** are for the engineer who picks it up. Nothing is cut; the detail moves one click away into the first comment.

## Two layers

**Description:** in plain language, what is wrong or wanted, why it matters, and how anyone can tell it is done. No file paths, function names or stack traces.

**Technical notes:** the first comment, titled `Technical notes`. Root cause, suggested approach, files, how to verify. Past about 250 words it is a document: write it as one, link it from the ticket, and keep two sentences of it in the comment.

## Budgets

| Part | Ceiling |
| --- | --- |
| Title | 80 characters |
| Description of a bug, task or story | 150 words |
| Description of a spike or epic | 80 words |
| Headings in the description | 6 |
| Acceptance criteria | 2 to 5 bullets |
| Code identifiers in the description | 3 |
| Technical notes | 250 words |

These are ceilings. Shorter is better when nothing is missing.

## Steps

1. **Pick the type.** Something broken now: bug. Preventive or operational work: task. A capability someone will notice: story. The output is an answer, not code: a spike, titled `Investigate …` and timeboxed. Three or more related tickets, or a plan whose phases could ship separately: an epic with one child per phase.
2. **Search for duplicates** with two or three distinctive words, open tickets only. If one matches, offer to comment on it instead.
3. **Draft** from the template for the type in [references/formats.md](references/formats.md). Name the effect, not the mechanism ("search engines drop the product data" rather than the serializer bug). Write acceptance criteria as outcomes someone can check without reading code. Put history under **Links** as bare links, not summaries.
4. **Lint** the draft until it passes:

   ```bash
   python3 scripts/ticket_lint.py --type bug --title "<title>" draft.md
   ```

   The path is relative to this skill's folder. It counts words, headings, criteria and code identifiers, and lists the identifiers to move.

5. **Show the user** the title, description and technical notes, with one line of numbers ("118/150 words, 2 identifiers, 4 criteria"). Filing a ticket notifies people, so wait for a go-ahead unless the user already gave one.
6. **File it**, then add the technical notes as the first comment, and report the key and link on one line.

## Several tickets at once

A burst of new tickets is hard to absorb. Put them under one epic or parent so the board shows one item, keep the children short because the parent carries the why, and finish with the `ticket-digest` skill so the reader gets one message instead of a pile of notifications.
