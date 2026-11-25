---
name: pipeline-log
description: Maintain one running deal log — stage, next step, last touch — that every other skill reads and writes, so your assistant actually remembers the pipeline.
metadata: { "openclaw": { "emoji": "🗃️" } }
---

# Pipeline Log

The memory layer for the whole pack. OpenClaw has no built-in CRM, so this file *is* the CRM: one structured log every skill updates as prospects move, plus the queries that tell you what to do today and how the pipeline looks this week.

## When to use (trigger phrases)

Use this skill when the user says:
- "what's due today?" / "what do I follow up on?"
- "show me the pipeline" / "pipeline summary"
- "add <prospect> to the pipeline"
- "update <name> to <stage>"
- "what stage is <company> at?"
- (Automatic) whenever another skill needs to read or write deal state.

## How it works

1. **Keep one source of truth.** Store the log as a single structured file in the workspace — `pipeline.csv` or `pipeline.json` (CSV is human-editable; JSON is cleaner for the agent). If the user has connected a Sheet, Airtable, or a real CRM, write there instead and treat this file as the fallback. One place, always.
2. **Use a fixed schema.** Every prospect is one row:
   - `id` — stable key (email or company-slug).
   - `prospect` / `company` / `channel` (email, LinkedIn, etc.).
   - `stage` — one of: `researched → contacted → engaged → meeting_booked → opportunity → won | lost | nurture`.
   - `angle` — the opening hypothesis (from `prospect-research`).
   - `next_step` + `next_step_date` — the single next action and when it's due. This drives everything.
   - `last_touch_date` — when you last contacted them.
   - `owner` — who's on it (for shared use).
   - `notes` — extracted facts: competitor, timeline, buyer, objection.
   - `source` — where the lead came from.
3. **Provide the core operations** the other skills call:
   - **Add** a prospect (usually right after `prospect-research`).
   - **Advance stage** (e.g. `reply-triage` moves `contacted → engaged`).
   - **Log a touch** (update `last_touch_date`, append to notes).
   - **Set next step + date** (the scheduling hook `followup-sequence` writes to).
   - **Suppress** (mark `lost` / opted-out; never contact again).
4. **Answer "what's due today."** On demand or on the daily run, list every row whose `next_step_date` is today or overdue, sorted by stage priority (opportunities and booked meetings first). This is the agent's to-do list — it's how follow-ups actually fire.
5. **Produce a weekly pipeline summary.** Counts per stage, meetings booked this week, deals that have gone stale (no touch in >10 days), and opt-outs. Surface the stuck ones so nothing rots silently.
6. **Never lose state.** Read the current file before writing, write the whole updated record back, and keep the schema stable. If a field is unknown, leave it blank rather than dropping the column.

## Output

Two shapes — a query view and the underlying record. Example:

```
DUE TODAY (Jul 2)
  🔥 Dana Ruiz / Acme        opportunity   → meeting-prep (due today)
     Sam Ng / Northwind      engaged       → send touch 3 (overdue 1d)
     Priya R / Vertex        contacted     → send touch 2 (due today)

WEEKLY PIPELINE
  researched 12 · contacted 8 · engaged 5 · meeting_booked 2 ·
  opportunity 1 · won 0 · lost 3 · nurture 4
  Meetings booked this week: 2   Stale (>10d no touch): 3
  Opt-outs this week: 1  (suppressed)

RECORD (pipeline.json excerpt):
  {
    "id": "dana@acme.com", "company": "Acme", "channel": "email",
    "stage": "opportunity", "angle": "hiring signal → ramp gap",
    "next_step": "meeting-prep", "next_step_date": "2026-07-02",
    "last_touch_date": "2026-07-01", "owner": "you",
    "notes": "VP Sales, new in seat; incumbent Outreach; wedge=research",
    "source": "careers-page signal"
  }
```

## Notes

- **This file is your pipeline's memory — protect it.** Back it up (commit it, or keep it in a synced folder). If it's lost, the assistant forgets every prospect and where they stand.
- **One log, not many.** Don't let deal state scatter across chat threads and ad-hoc notes. Every skill in this pack reads and writes *this* file so the picture stays coherent.
- **Connect a real CRM if you have one.** HubSpot, Pipedrive, Airtable, or a Google Sheet all work as the backing store — point the skill at it and it'll write there instead. The file is the zero-setup default, not a mandate.
- **PII lives here.** Names, emails, and notes on real people are in this file. Store it somewhere appropriate to your privacy obligations, and honor deletion requests (drop the row) alongside opt-outs.
- **Keep the schema honest.** The stage field only means something if you use the same values everywhere; don't invent new stages per prospect. Stability is what makes the queries and summaries trustworthy.
