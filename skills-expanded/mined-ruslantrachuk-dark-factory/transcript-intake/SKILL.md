---
name: transcript-intake
description: Analyse a meeting transcript on the "what's new for us" principle — a delta against the board and the project's commitments, not a retelling. Use when given a meeting transcript/recording or asked to "go through the meeting", "what did we decide there", "run the transcript".
---

# Skill `transcript-intake` — "what's new for us"

> Canonical template (templates/base); carry generic improvements from deployed copies back here. Needs no configuration — the project registry and trackers come from the `board` skill.

> **Seam:** board = Linear, through the `board` skill. To use another tool, rewrite step 2 "Collect the baseline" and the `board` skill.

Input: a meeting transcript (a file, text in the chat, an email with a recording, an export). Output: a **delta** against what the factory already knows + card drafts. NOT a retelling of the meeting.

## Order

### 1. Project and date
Determine the board project(s) (participants, topics) and the **meeting date**. Not sure — ask with a single question, do not guess. The diff is always built "as of today": for an old meeting, work may have happened between "it was said" and "now" — every candidate finding is first checked with "hasn't this already been done/created after the meeting?".

### 2. Collect the baseline (mandatory minimum)
- The board (skill `board`): the project's open cards (Backlog…Merged) and Shipped.
- The Project description in Linear — the target picture / baseline of commitments.
- **The client's external tracker**, if the project has one.
- Release notes / open questions from the project repo.

If some source is unavailable — the report is **explicitly marked "baseline incomplete: X not checked"**, and wording changes from "this doesn't exist" to "didn't find it on the board". With no baseline at all — only questions, no cards.

### 3. Diff — sorting into buckets
Each substantive fragment goes into one bucket. Separate a **participant's proposal** from an **agreed decision** (confirmed by the other side); quote with the speaker named, do not glue remarks of different people into one "quote".

| Bucket | What it is | What to do |
|---|---|---|
| **New** | an agreement that did not exist before the meeting (born in it) | a card draft (what/why/where from + quote + speaker) |
| **Known but untracked** | the commitment existed before the meeting, but it is neither on the board nor in the tracker | NOT "new" and NOT a change request: show it as an accounting gap — "known since …, not tracked anywhere" — propose a card with this mark |
| **Already done** | what was said was implemented after the meeting (for old transcripts) | drop it, mention it in one line in the filter |
| **Commitment shift** | a change in scope/deadlines against the recorded baseline | **change request**: what changes, a quote; do not silently edit the baseline. Needs checking: the baseline really recorded something else (do not infer a shift from the brevity of the Project description) |
| **Contradiction** | what was said diverges from an open card/an earlier decision | raise it explicitly, ask the owner |
| **Answers** | the client answered a pending question | a **comment draft** for the card (not an automatic link); check whether the answer is outdated (a fresher artifact wins) |
| **Can't verify** | a claim the baseline neither confirms nor refutes (including "surely there is an API") | a question to the owner, NOT a card |

Promised artifacts ("I'll send the reference list", "I'll give you the spreadsheet") — check whether they were received (a file in inputs/, a card): not received → into the report as a pending dependency.

### 4. Output — the "What's new for us" report
Short, by bucket, with quotes and speakers. At the end — card drafts as a batch: "create them? (you can pick some)". Creation — only after a "yes" (rule of the `board` skill). A development card draft is allowed only from the "New" and "Known but untracked" buckets; from "Can't verify" — only a question/investigation.

## Rules
- **Do not retell the meeting.** If the delta is empty — say so: "nothing new, everything is already on the board".
- A quote is mandatory for: commitment shifts, contradictions, everything that ends up in a card text. Do not paraphrase commitments in your own words.
- Promises made **from our side** ("we'll do it by Friday") — on a separate line in the report: these are new commitments, the owner must see them.
- One transcript may concern several projects — the delta is split by project, not dumped into one.
- Transcription errors (speech recognition mixes up words): when a key phrase is doubtful, mark it [uncertain transcription] and do not build a card on it without confirmation.
