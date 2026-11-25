# Bland.ai -> Make.com Voice Bot Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

Takes a list of phone numbers + per-call task instructions, fires off an AI voice call for each one via Bland.ai, waits for the call to finish, then analyzes the call to extract structured answers (e.g. "was the appointment rescheduled? if so, to what time?"). Results get written back to `data/output.csv`.

This is a direct port of a Make.com scenario that had 6 nodes: Google Sheets read -> Bland.ai call -> parse call_id -> sleep 300s -> Bland.ai analyze -> parse analysis. The Google Sheets dependency is gone by default; everything runs locally.

Original use case was appointment rescheduling detection, but the task and analysis questions are fully configurable per row.

## When to trigger

- "run bland.ai calls on my lead list"
- "fire voice bot calls from CSV"
- "analyze what happened on my bland.ai calls"
- `/bland-ai-make-com-voice-bot-flow`

---

## Required env vars

```
BLAND_AI_API_KEY=your_key_here
```

Get your key from https://app.bland.ai -> API Keys.

---

## Input CSV format

`data/input.csv` — two required columns:

| phone_number | task | reschedule_goal | questions_json |
|---|---|---|---|
| +14035550123 | You are a scheduling assistant... | Identify if the appointment was rescheduled... | [["Was the appointment rescheduled?","true or false"],["What time was it rescheduled to?","string"]] |

- `phone_number`: E.164 format (`+1XXXXXXXXXX`).
- `task`: The instruction prompt passed to the Bland.ai voice bot for the call.
- `reschedule_goal` (optional): Overrides the default analysis goal. If blank, uses the default from the original workflow.
- `questions_json` (optional): JSON array of `[question, answer_type]` pairs for call analysis. If blank, uses default rescheduling questions.

---

## Step-by-step procedure

1. Put your phone numbers + task instructions in `data/input.csv` (or keep the sample).
2. Set `BLAND_AI_API_KEY` in your env.
3. Run:
   ```bash
   python3 scripts/run_calls.py
   ```
4. The script processes rows one at a time: places the call, waits up to 300 seconds, then hits the analyze endpoint.
5. Results land in `data/output.csv` with the original row fields plus `call_id`, `call_status`, `rescheduled` (true/false), and `reschedule_time`.

### Optional: run analysis only (if you already have call IDs)

```bash
python3 scripts/run_calls.py --analyze-only data/calls_with_ids.csv
```

Skips the dialing step, just runs analyze on each `call_id` in the file.

---

## Output CSV columns

Original input columns, plus:

| call_id | call_status | rescheduled | reschedule_time | analysis_raw |
|---|---|---|---|---|
| bland_abc123 | completed | true | 13:00 | {...} |

---

## Node map (original Make.com -> this skill)

| Make.com node | Module | This skill |
|---|---|---|
| #3 | google-sheets:filterRows | `io_store.read_rows("data/input.csv")` |
| #4 | http:ActionSendData POST /v1/calls | `bland_call()` in run_calls.py |
| #6 | json:ParseJSON (call response) | `json.loads()` inline |
| #8 | util:FunctionSleep 300s | `time.sleep()` with configurable wait |
| #5 | http:ActionSendData POST /v1/calls/{id}/analyze | `bland_analyze()` in run_calls.py |
| #9 | json:ParseJSON (analysis response) | `json.loads()` + `io_store.write_rows()` |
