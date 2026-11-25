# VAPI AI Modules

> Two Make.com webhook tools converted to standalone Python scripts. These power a VAPI voice AI agent that can check calendar availability and book consultations on Google Calendar.

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Two workflows, two HTTP endpoints, one VAPI voice bot:

**Workflow 1 — Get Availability** (`/get-availability`)
VAPI sends a date. The script queries Google Calendar free/busy for that day (9am-5pm window), passes the busy blocks to OpenAI gpt-4o-mini, and returns natural-language availability back to VAPI (e.g. "Free between 10:00am-12:00pm and 2:30pm-5:00pm").

**Workflow 2 — Book Event** (`/book-event`)
VAPI sends a datetime. The script creates a 30-min "Consultation" event on Google Calendar and returns "Booked successfully." to VAPI.

Original source: Make.com scenarios "YouTube Tool: Get Calendar Events" + "YouTube Tool: Book Calendar Events" from the VAPI product bundle.

---

## When to trigger

Use this skill when:
- Setting up or re-deploying a VAPI assistant that needs calendar tool functions
- Debugging why VAPI can't check availability or book slots
- Running the tools locally to test the calendar integration before going live
- Adapting the calendar/booking logic for a new VAPI assistant

---

## Env vars required

```
OPENAI_API_KEY                  — for availability natural-language conversion
GOOGLE_CALENDAR_CREDENTIALS     — absolute path to a Google service-account JSON
                                   shared on the target calendar with editor access
CALENDAR_ID                     — (optional) defaults to nick@leftclick.ai
```

---

## Step-by-step procedure

### Local test (no HTTP server)

1. Set env vars:
   ```bash
   export OPENAI_API_KEY=sk-...
   export GOOGLE_CALENDAR_CREDENTIALS=/path/to/service-account.json
   export CALENDAR_ID=you@yourdomain.com
   ```

2. Check availability for a date:
   ```bash
   cd /Users/nicksaraev/Business/active/free-community/skill-conversion/skills/vapi-ai-modules
   python3 scripts/get_availability.py --date 2026-07-10
   ```
   Output: VAPI-format JSON with `availabilityTimes` string.

3. Book a slot:
   ```bash
   python3 scripts/book_event.py --datetime "2026-07-10T14:00:00"
   ```
   Output: VAPI-format JSON with "Booked successfully."

### Run as live webhook server (for VAPI to call)

```bash
python3 scripts/serve.py --port 8080
```

Then point your VAPI assistant's two tool server URLs to:
- `https://your-host:8080/get-availability`
- `https://your-host:8080/book-event`

### Batch test from CSV

The `data/input.csv` has sample rows with `date`, `tool_call_id`, and `action` columns. To run all rows:

```bash
python3 scripts/batch_test.py --input data/input.csv --output data/output.csv
```

(batch_test.py not written yet — add it if bulk testing is needed)

---

## Node map (original Make.com → Python)

| Make node | Module | Mapped to |
|---|---|---|
| VAPI YouTube (1) | `gateway:CustomWebHook` | `serve.py` POST /get-availability |
| Get Free/Busy | `google-calendar:getFreeBusyInformation` | `get_availability.py::get_busy_blocks()` |
| Transform to JSON | `json:TransformToJSON` | `json.dumps(busy)` inline |
| OpenAI completion | `openai-gpt-3:CreateCompletion` (gpt-4o-mini) | `get_availability.py::availability_from_busy()` — key from `OPENAI_API_KEY` |
| Webhook respond | `gateway:WebhookRespond` | `build_vapi_response()` → printed/returned |
| Book Calendar Event (YT) | `gateway:CustomWebHook` | `serve.py` POST /book-event |
| Create an Event | `google-calendar:createAnEvent` | `book_event.py::create_event()` |
| Webhook respond | `gateway:WebhookRespond` | `build_vapi_response()` |

No Google Sheets / Airtable / Excel nodes in source — no read_rows()/write_rows() mapping needed. The CSV store is available for logging/batching if you want it.

---

## Dependencies

```bash
pip install openai google-api-python-client google-auth
# optional for Google Sheets mode:
pip install gspread
```
