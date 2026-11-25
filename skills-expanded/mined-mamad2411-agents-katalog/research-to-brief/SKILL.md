---
name: research-to-brief
description: Folds any pile of research — pasted notes, files, transcripts, reports — into the right sections of marketing-brief.md, graded T1 to T3 for confidence, with contradictions surfaced instead of averaged away. Use whenever research exists anywhere other than the brief.
argument-hint: "[paste the research or point to the files]"
---

# Research to Brief — one home for what you know

Research that lives in scattered documents might as well not exist: the next campaign gets built from memory and vibes regardless. The brief is the department's single memory, and this skill is its intake valve — everything decision-relevant gets extracted, graded, routed to its section, and reconciled with what is already there.

## Inputs
- The research, in any form — pasted text, file paths, folders, notes: $ARGUMENTS
- The whole current `marketing-brief.md`, read end to end first, so new material lands as an update rather than a duplicate. If no brief exists, run `/marketing:onboard` to create the skeleton, then return here.

## Do this
1. **List the sources with dates.** Recency matters at grading time, and every finding must trace back to one of them.
2. **Extract every decision-relevant finding** — a claim, a number, a verbatim quote, a pattern — and route each to its brief section: the business, the market, the customer (ICP, avatar, pains, desires, objections, language bank), the competitors, positioning & message, the offer, channels & funnel, voice, numbers that matter. A finding can feed two sections; cross-reference rather than duplicate.
3. **Grade each finding on the brief's own scale:**
   - **T1 sourced** — a customer said or did it, or a measured result.
   - **T2 reasoned estimate** — credible secondhand: review mining, reports, competitor observation.
   - **T3 guess** — inference, or a single anecdote doing a lot of work.
   Write the grade inline with the finding.
4. **Surface contradictions.** Where new findings disagree with the brief or with each other, do not overwrite and do not average — log both versions in a "contradictions to resolve" block, each with the one input that would settle it.
5. **Merge into `marketing-brief.md`.** Update sections in place, date-stamp the pass, and keep customer quotes verbatim in the language bank. An existing entry is replaced only when the new evidence grade is equal or better — a T3 never overwrites a T1.
6. **Report the delta:** what was added to which section, what got upgraded or downgraded, the contradictions raised, and the single research task that would most improve the brief's weakest section.

## Output
An updated `marketing-brief.md`, plus a change log in chat: findings added per section with grades, contradictions to resolve, and the one next research task. The brief's T3-marked sections remain the visible research backlog.

## Rules
- Verbatim beats paraphrase. Customer language enters the language bank exactly as spoken — the copy skills depend on it.
- Grade honestly. A brief full of T3 guesses dressed as T1 facts briefs the whole department into fiction.
- Contradictions are findings. Averaging two conflicting numbers destroys both.
- Nothing enters without a source. "Everyone knows" is not a source.
- Date-stamp every pass. An undated finding cannot be superseded cleanly, and stale certainty is worse than fresh doubt.
