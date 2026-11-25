---
name: pm-jtbd-synthesis
description: Synthesize Jobs-to-be-Done from one or more customer interview transcripts. Extracts Forces of Progress (push, pull, anxiety, habit) with verbatim quote + line-number attribution, clusters jobs across transcripts, and emits three artifacts — a full synthesis report, job stories in canonical When/I-want/So-I-can format, and an Opportunity-Solution Tree stub. Triggers on "synthesize calls", "synthesize interviews", "jtbd", "jobs to be done", "discovery synthesis", "what did customers say", "interview synthesis", "forces of progress", or when the user points at a folder of call transcripts and asks for product insight. Composes downstream of `transcribe` (audio → text, multiplai-media plugin) and `extract-insights` (general extraction, multiplai-research plugin); composes upstream of `pm-persona-codifier`.
---

# pm-jtbd-synthesis

Turn raw customer-interview transcripts into discovery artifacts a product team can act on. This is **synthesis**, not summary — the output is structured around the four Forces of Progress (Bob Moesta) and clustered jobs, not around what each speaker said in order.

## Arguments

| Arg | Description | Default |
|-----|-------------|---------|
| **source** | File path, folder path, or comma-separated list of transcript files | *(required)* |
| `--depth` | `quick` (forces + top jobs only) or `full` (forces + jobs + OST stub) | `full` |
| `--audio` | `true` if any inputs are audio files (will call `transcribe` first) | `false` |

If the user gives a folder, glob all `*.txt`, `*.md`, `*.vtt`, `*.srt` files inside it. Confirm the file list with the user before processing if there are more than 5 files.

## Input Handling

1. If `--audio true`, route each audio file through the `transcribe` skill first (ships in the **multiplai-media** plugin — if it isn't installed, ask the user to provide text transcripts); save transcripts to a sibling folder; then proceed.
2. Read each transcript with the Read tool so you get line-numbered output. Line numbers are mandatory anchors in the output — without them the synthesis is un-verifiable.
3. If a transcript is over ~2000 lines, read it in chunks and track the line offset.
4. If there are multiple speakers, identify which speaker is the customer/interviewee. Apply forces extraction only to customer utterances. Interviewer questions are context, not signal.

## Workflow

This is a three-pass process. Do not skip passes.

### Pass 1 — Per-transcript forces extraction

For **each** transcript, extract the four Forces of Progress. See `references/jtbd-forces.md` for the canon, examples, and common traps.

For each force found, capture:
- **Force type** (push / pull / anxiety / habit)
- **One-sentence statement** of the force in the customer's frame
- **Verbatim quote** anchoring it (with line number range, e.g. `L148-155`)
- **Speaker tag** if multi-speaker (`[Customer:]`, `[Acme/Jane:]`)
- **Confidence** — STRONG (stated directly + repeated), SUPPORTED (stated once clearly), WEAK (implied or hedged)

Write per-transcript extractions to a working buffer; do not emit them as a separate file unless the user asks.

**Do NOT use chain-of-thought reasoning during extraction.** CoT doubles hallucination rates in extraction tasks. Extract directly with tight source anchoring. (Same rule as `extract-insights`.)

**Hedges are sacred.** "Probably," "kind of," "I don't think," "maybe" — preserve verbatim. Stripping a hedge inverts meaning. See `extract-insights` rule 2 if unclear.

### Pass 2 — Cross-transcript job clustering

After all transcripts are processed, cluster jobs. A **job** is the progress the customer is trying to make in their life or work — not a feature, not a workflow step.

Format jobs in two registers:
1. **Functional job** — what they're trying to get done (e.g., "Hire a senior engineer in under 6 weeks")
2. **Emotional / social job** — how they want to feel or be perceived (e.g., "Look like a hiring manager who has it together")

Cluster across transcripts:
- Which jobs appear in 2+ transcripts? Those are the load-bearing clusters.
- Which jobs appear in only 1 transcript? Hold them aside as outliers; note explicitly.
- Where do forces conflict across customers? (Customer A's pull is Customer B's anxiety.) Flag the tension.

Cap final cluster count at 7. If you have more, the clusters are too granular.

### Pass 3 — Emit artifacts

Produce **three files**, all date-stamped, written to `./INBOX/` if it exists, else the current directory (or ask the user where):

1. **`INBOX/jtbd-synthesis-YYYY-MM-DD.md`** — the full report (template below)
2. **`INBOX/job-stories-YYYY-MM-DD.md`** — job stories in canonical format. See `references/job-stories-format.md`.
3. **`INBOX/ost-stub-YYYY-MM-DD.md`** — opportunity-solution tree skeleton (skip if `--depth quick`). See `references/opportunity-solution-tree.md`.

If `--depth quick`, emit only file 1 and a job-stories section inside it.

## Output Template — Full Report (file 1)

```markdown
# JTBD Synthesis — [topic / customer segment]

**Date:** YYYY-MM-DD
**Transcripts ingested:** N
**Sources:**
- path/to/transcript-1.txt — [customer / company / date if known]
- path/to/transcript-2.txt — ...

## TL;DR

- [3–5 bullets. The 1-2 highest-confidence jobs and the most important tension.]

## Forces of Progress — Cross-Transcript View

| Force | Strongest signal across transcripts | Appears in |
|-------|-------------------------------------|------------|
| Push (what's wrong with the old way) | [one sentence] | N transcripts |
| Pull (what's appealing about the new way) | [one sentence] | N transcripts |
| Anxiety (what worries them about switching) | [one sentence] | N transcripts |
| Habit (what keeps them with the old way) | [one sentence] | N transcripts |

Then for each force, a short section listing every distinct signal with quote anchors:

### Push

1. **[Short label]** — [one-sentence statement of the force]
   > "[verbatim quote]" — `transcript-name.txt L#-#` `[Customer]` `STRONG`
2. **[Short label]** — ...

(Repeat for Pull, Anxiety, Habit.)

## Job Clusters

Up to 7. For each:

### Job 1 — [Short, action-oriented label]

- **Functional job:** When [situation], I want to [motivation], so I can [outcome].
- **Emotional / social job:** [if surfaced — how they want to feel or be perceived]
- **Appears in:** [N transcripts — list them]
- **Anchor quotes (2–3):**
  > "..." — `transcript.txt L#-#`
  > "..." — `transcript.txt L#-#`
- **Forces in play:**
  - Push: [...]
  - Pull: [...]
  - Anxiety: [...]
  - Habit: [...]
- **Switching trigger (if observed):** [the moment that made them seriously consider change]

## Tensions & Contradictions

Where customers disagree, or where one customer's pull is another's anxiety. These are gold for product positioning.

- **[Tension label]** — [one sentence] — `transcripts involved`

## Outliers — Single-Transcript Jobs

Jobs that only appeared once. Listed but not promoted. May indicate a segment we haven't sampled enough of, or a one-off context. Cap at 5.

- **[Job label]** — [one sentence] — `transcript.txt L#`

## Open Questions for Next Round of Discovery

What the synthesis can't answer with this data. 3–7 questions. Each should be answerable by interview, not by analysis.

1. [Question]
2. ...

## Method Notes

- Total transcript line count ingested
- Speaker attribution method (named / role-tagged / unclear)
- Any transcripts excluded or partially read (with reason)
- Garbles silently corrected (if any)
```

## Output Template — Job Stories (file 2)

See `references/job-stories-format.md` for the format. The skill body should not duplicate it.

## Output Template — OST Stub (file 3)

See `references/opportunity-solution-tree.md`. Stub means: outcome at top, top 3 opportunities derived from the highest-confidence job clusters, 2-3 candidate solutions per opportunity, and explicit "experiment ideas" placeholders — not committed bets.

## Rules

1. **Every force, every job cluster, every quote is line-anchored.** If a source doesn't have line numbers (raw paste), say so in Method Notes and note that quotes are unanchored.

2. **Speaker attribution is mandatory in dialog.** Tag every quote `[Customer:]` / `[Interviewer:]` or with named roles. Misattributing an interviewer's leading question to the customer is the #1 failure mode and inflates job confidence falsely.

3. **No outside knowledge.** Don't add company background, market context, or competitor names the customer didn't mention. If the customer says "our current tool," you do NOT name a specific vendor. If you must, tag `[inferred]`.

4. **Hedges preserved verbatim.** Same rule as `extract-insights`. Apply rigorously.

5. **Jobs are progress, not features.** "I want a dashboard" is not a job; "I want to know whether I'm on track without having to ask anyone" is. If you find yourself writing feature names in the job statement, rewrite.

6. **Confidence tags are honest.** STRONG requires either (a) the customer stating the same thing in multiple ways, or (b) 2+ customers stating the same thing. Do not inflate WEAK to STRONG to make the report look more conclusive.

7. **Cap at 7 jobs.** Past 7, you're not synthesizing — you're transcribing. Force yourself to cluster harder.

8. **Tensions section is high-value. Do not skip it to save time.** If you found no tensions, say "No cross-customer tensions surfaced in this sample" explicitly — silence is ambiguous.

9. **Output goes to `./INBOX/` if it exists, else the current directory** (or wherever the user specifies). In a curated workspace with `RESOURCES/` and `ARTIFACTS/`, write only to `INBOX/` and let the user promote.

10. **If the input is thin, say so.** "Three transcripts is not enough to call any of these clusters high-confidence" is the honest output when warranted.

## Composing With Other Skills

- **Upstream**: If inputs are audio, invoke `transcribe` first (requires the **multiplai-media** plugin).
- **Sideways**: `extract-insights` (requires the **multiplai-research** plugin) is the general version of forces extraction — use it if the user wants insights from non-customer content (e.g. analyst reports). For customer interviews specifically, this skill is sharper.
- **Downstream**: The output of this skill is the canonical input for `pm-persona-codifier` (cluster jobs → persona archetypes). (Planned, not yet shipped: an opportunity-solution-tree skill and a PRD skill would consume these clusters next — for now the OST stub this skill emits is the hand-off.)
