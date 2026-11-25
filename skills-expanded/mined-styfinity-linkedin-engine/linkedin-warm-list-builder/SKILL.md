---
name: linkedin-warm-list-builder
description: Build a prioritised warming target list by scoring ICP-fit candidates and attaching the strongest why-now signal to each. Use when you need a ranked list of who to warm next, not generic prospecting.
argument-hint: "[seed lists, search filters, or signals to weight]"
---

# LinkedIn Warm List Builder

Warming is wasted on the wrong people. This skill assembles the right ones, scores them against the ICP, and sorts so the warmest sit at the top, because viral and signal warmth both decay fast.

## Inputs
- Any seed lists, search filters, or signals to weight (recent posters, role changes, mutuals, event attendees): $ARGUMENTS
- The ICP, pains, and offer load automatically from the brief.

## Do this
1. Assemble candidates. If the connected layer is available, run a live search off the filters. Otherwise work off the pasted or seed lists. Do not scrape.
2. Score each against the ICP. Use a 0 to 10 fit score on role, company size, and pain match. Drop anything under the floor the brief implies.
3. Attach the strongest why-now signal to each: a recent post, a role change, a funding event, a comment thread, a mutual. One signal per target, the freshest one.
4. Sort warmest to coldest. A strong recent signal beats a marginally higher fit score, because warmth decays and fit does not.
5. Suggest a first touch per target: engage on the post, comment, or a connect via /linkedin-connection-note.

## Output
A ranked table: name, title, company, ICP score (0 to 10), why-now signal (with the date), suggested first touch. Top of the table is who to warm today. End with a one-line note on which rows are signal-fresh (act this week) versus evergreen.

## Rules
- Live search needs the connected CLI/MCP layer. Without it, work off seed lists only. No scraping by default.
- This is a list to warm, not a list to blast. Building it sends nothing.
- No em-dashes. Every why-now signal must be real and dated, not invented.
- If a target has no genuine why-now signal, mark it evergreen, do not fabricate one.
