---
name: doc-summarize
description: Summarizes a long document, PDF, transcript, or report into a clear one-page brief with the key takeaways, notable quotes, and any action items. Use when the user asks to summarize, TLDR, give me the short version of, or digest a document. Works on files in the project folder or uploaded directly.
---

# Doc Summarize

Turn a 40-page PDF, a 90-minute meeting transcript, or a dense article into a one-page brief the user can actually use.

## Before starting

1. Ask the user: what's the purpose of the summary? "For my knowledge," "for a decision I'm making," "for a meeting tomorrow" — the answer changes what you emphasize.
2. Read `context/preferences.md` — citation style, format preferences
3. If the document is long (>30 pages or >20k words), tell the user roughly how long the summary will take

## What to produce

A markdown file saved to `/output/summary-{document-name}-{YYYY-MM-DD}.md` with four sections:

1. **The 30-second version** — 3–5 sentences. The core takeaway. If the user only reads this, they got the gist.
2. **Key points** — 5–10 bullets. The things that matter. Each one stands alone.
3. **Notable quotes or passages** — verbatim excerpts if the document is worth quoting (reports, transcripts, academic papers). Include page/timestamp references if available.
4. **Action items or implications** — if the summary has implications for the user (decisions to make, things to follow up on), list them. Skip if not applicable.

## Inputs

- The document (required) — PDF, markdown, transcript, text file, article URL
- The purpose (recommended — ask if not given)
- Any prior summaries or notes on related documents in the project folder

## How it works

1. Read or fetch the document. If it's a URL, pull the content. If it's a PDF, extract the text.
2. For long documents: make a pass to identify structure (sections, arguments, conclusions), then a pass to extract the key points
3. For transcripts: identify speakers, decisions made, action items explicitly stated
4. Draft the four sections. Dense, specific, no padding.
5. If there are things the document says that contradict other things the user has read (and you have that context), flag it
6. Save the file, tell the user one sentence on what surprised you or what they should look at first

## What not to do

- Do not summarize by compression ratio ("reduce to 10%"). Summarize by importance — some documents have three things that matter, others have thirty.
- Do not paraphrase every paragraph. Skip the filler. If 80% of a report is methodology and 20% is findings, give them the findings.
- Do not editorialize beyond what the document supports. If you disagree with the document, that's a separate deliverable.
- Do not skip quotes if the document earns them. Some documents are worth reading for the exact language.

## Example output structure

```markdown
# Summary — Q1 Board Deck (Acme Corp) — 2026-04-18

## The 30-second version
Q1 was a miss on revenue (-8% vs. plan) but a beat on new logo count (+12%). The gap is pricing — new customers came in at lower ACV than plan. CEO is proposing a pricing rework in Q2 and a hiring pause through end of Q2. Board is being asked to approve both.

## Key points
- **Revenue:** $4.2M vs. $4.6M plan. Miss.
- **New logos:** 47 vs. 42 plan. Beat.
- **ACV dropped 14% YoY** — largely due to a new self-serve tier introduced in Q4
- **Net retention:** 108%, flat with Q4, below the 112% target
- **Cash:** 22 months runway, up from 19 in Q4 (thanks to reduced spend)
- **Proposed: pricing rework** — reviewing tier structure and the self-serve plan that's cannibalizing mid-market
- **Proposed: hiring pause** — through end of Q2, open reqs close today, exceptions only for existing backfills
- **Risks called out:** competitor entered the mid-market segment in Feb, churn is ticking up in the self-serve tier

## Notable quotes
> "The self-serve tier has become a revenue problem. It's pulling customers who would otherwise buy the $15K plan into the $3K plan." — CEO letter, p. 3

> "We're not cutting. We're pausing while we figure out why our growth is outpacing our monetization." — CEO letter, p. 5

## Action items / implications
- Board to vote on pricing rework (scope: tier restructure) and hiring pause — both require approval
- Finance to model the revenue impact of three pricing scenarios before next board (dates not specified in deck)
- No action items for you personally unless you're on the pricing committee
```

## Customization notes

- **For transcripts** (meetings, interviews). Replace "notable quotes" with "decisions made" and "open questions."
- **For research papers / academic**. Add a fifth section: "What the authors are wrong or unclear about."
- **For product specs / tech docs**. Add a "dependencies and risks" section.
- **If the user asked for a summary to brief someone else**. Write the whole thing in a voice-neutral tone, not in the user's voice. They'll forward it.
- **If the document is genuinely low-signal**. Tell the user. A short, honest "this document has three things in it, here they are" is better than padding it out to look substantive.
