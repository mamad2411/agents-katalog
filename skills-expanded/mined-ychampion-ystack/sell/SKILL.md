---
name: sell
description: >-
  Run the sales pipeline for a startup idea: account research, outreach and follow-up drafts, call
  prep, post-call summaries, and pipeline status tracked in a founder hub folder. Use when turning
  interested prospects into pilots, design partners or paying customers, when asked to prep for a sales
  call, draft a follow-up, research an account, or show where deals stand.
argument-hint: "<idea> [research <company> | prep <person> | followup <person> | status]"
---

# /sell: turn interest into pilots and payments

## The founder hub

This skill reads and writes a **founder hub**: one folder holding the startup's truth.

- **Location:** the `FOUNDER_HUB` environment variable, default `~/founder`. Below, `<hub>` means that
  folder.
- **Files this skill uses:**

| File | What it holds |
|---|---|
| `<hub>/README.md` | The decision and evidence rules (the `discover` skill writes defaults). Read it if present |
| `<hub>/bottleneck.md` | The current bet, this week's single bottleneck, the goal and its deadline |
| `<hub>/evidence/<idea>.md` | Conversation log, signed pilots and payments for one idea |
| `<hub>/evidence/<idea>-prospects.md` | Researched prospects and outreach status (from `discover`) |
| `<hub>/evidence/<idea>-pipeline.md` | The pipeline: one row per account, its stage, and a dated log of stage changes |

Pipeline stages: **contacted → talked → pilot offered → pilot live → paying**.

**If the hub or a file is missing,** say so and offer to create it: the folder, an empty
`bottleneck.md` (current bet, bottleneck, goal, deadline), `evidence/`, and a pipeline file seeded from
the prospects and evidence files if they exist, or empty with the stage columns if not. Never skip a
write silently because a file wasn't there.

Read `bottleneck.md` and the idea's evidence files first.

## Commands

If sales skills are installed (for example account research, outreach drafting, call prep or call
summary skills), use them for the step, then write the result back into the hub. They're optional;
everything below works with web search alone.

- **`research <company>`:** what they do, size and stage, recent news, who owns the problem, and a
  concrete signal that they have it. Cite sources. Add the result to the pipeline file.
- **`prep <person>`:** a one-page call brief: their context, what the log already says, the 3 questions
  that matter most, the commitment to ask for (pilot, data access, paid trial), and likely objections
  with honest answers.
- **`followup <person>`:** a short follow-up that restates their problem in their words and makes one
  clear, small ask. Paste notes from a call and it also logs the call (as `discover log` does) before
  drafting.
- **`status`** (the default): pipeline counts by stage, deals stuck for more than 5 days, and today's 3
  highest-value actions.

## Rules

- **The human sends every message.** Draft only. Never send, post or email anything yourself, even if
  a tool for it is available.
- Never overstate the product. A pilot offer describes what exists today, plus what will be built for
  them, with a date.
- Pricing: propose a concrete paid pilot. Even a small payment is strong evidence; "free forever" isn't.
- Log every stage change with a date in the pipeline file, and any payment or signed pilot in
  `evidence/<idea>.md`.
