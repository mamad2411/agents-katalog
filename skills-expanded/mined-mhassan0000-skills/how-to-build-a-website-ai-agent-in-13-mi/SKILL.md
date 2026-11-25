# How to Build a Website AI Agent in 13 Min (Free N8N Template)

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What this does

This is a conversion of the "Simple N8N Chat Agent for Your Website" workflow. It spins up a conversational AI agent that sits on your website, answers questions about your business, and books meetings directly into Google Calendar -- all in one chat thread.

The original n8n workflow has 5 nodes:
- **Chat Trigger** -- webhook that receives messages from an embedded chat widget
- **OpenAI Chat Model** -- GPT backing the agent's responses
- **Window Buffer Memory** -- keeps the last 10 messages in context so the convo feels continuous
- **AI Agent** -- orchestrates everything; has a system prompt defining the bot's persona, business context, and booking flow
- **Google Calendar (check availability)** -- `getAll` events in a date range so the agent knows what slots are open
- **Google Calendar (create event)** -- creates the calendar event once user confirms a time, adds both parties as attendees

The system prompt in the source workflow is for 1SecondCopy (a copywriting agency), but you swap that out for your own business. The booking flow is the same regardless.

**APIs used:** OpenAI (chat completions), Google Calendar (read + write events)

---

## When to trigger this

Invoke this skill when you want to:
- Deploy a chat agent that can answer business questions AND book meetings
- Replicate or customize the n8n website chatbot template
- Run the agent locally (no n8n required) against a CSV of test conversations
- Log all bookings made by the agent to a CSV or Google Sheet

---

## Step-by-step procedure

### 1. Set up env vars

Copy `.env.example` to `.env` and fill in:

```
OPENAI_API_KEY=sk-...
GOOGLE_CALENDAR_ID=you@yourdomain.com
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json   # only for Calendar writes
```

For Google Calendar, you need a service account with calendar access OR OAuth tokens. The script supports both; see `scripts/calendar_tools.py` comments.

### 2. Customize the system prompt

Open `scripts/agent.py` and edit the `SYSTEM_PROMPT` constant at the top. Replace the 1SecondCopy content with your business details -- what you sell, pricing, turnaround, notable clients, timezone. The booking flow logic at the bottom of the prompt stays the same.

### 3. Prepare input data (optional batch mode)

If you want to replay a batch of test conversations, edit `data/input.csv`. Each row is one conversation turn:

```
session_id, user_message, timestamp
```

If you just want to chat interactively, skip the CSV and run in interactive mode (see step 4b).

### 4. Run the agent

**4a. Batch mode** (reads from CSV, writes booking records to output.csv):

```bash
python scripts/agent.py --mode batch --input data/input.csv --output data/output.csv
```

**4b. Interactive mode** (chat in your terminal, mirrors what the n8n widget does):

```bash
python scripts/agent.py --mode interactive
```

**4c. Server mode** (exposes a local webhook endpoint, drop-in replacement for the n8n Chat Trigger):

```bash
python scripts/agent.py --mode server --port 5678
```

Then point your website chat widget at `http://localhost:5678/webhook/chat`.

### 5. Review bookings

After a session where the agent booked something, the booking is logged to `data/output.csv` with columns: `session_id`, `attendee_name`, `attendee_email`, `start_time`, `end_time`, `event_id`, `created_at`.

---

## How to use this

### If you use Claude Code
1. Download and unzip the attached folder.
2. Drop it into `.claude/skills/` in your project (so you have `.claude/skills/how-to-build-a-website-ai-agent-in-13-mi/SKILL.md`).
3. Invoke it by describing what you need, or type `/how-to-build-a-website-ai-agent-in-13-mi`. Claude picks it up automatically.

### If you use a different AI agent
The SKILL.md file is plain English instructions. Open it, paste the contents into your agent's system prompt or instructions field (Cursor rules, custom GPT instructions, etc.), and keep the `scripts/` folder alongside -- the instructions reference those scripts and any agent that can run code can use them.

### If you use n8n
1. Download the attached `.json` file.
2. In n8n, open **Workflows → ... → Import from File** and select the `.json`.
3. Reconnect your credentials on any node showing a warning (n8n strips credentials on export -- that's normal). You'll need an OpenAI API credential and a Google Calendar OAuth2 credential.
4. Edit the system prompt in the AI Agent node to match your business.
5. Run it once manually with a test message before activating the trigger.
6. Activate the workflow.

---

## Node map (n8n → this skill)

| n8n node | Type | Maps to |
|---|---|---|
| When chat message received | Chat Trigger (webhook) | `agent.py --mode server` endpoint OR interactive loop |
| OpenAI Chat Model | LLM sub-node | `openai.chat.completions.create()` in `agent.py` |
| Window Buffer Memory | Memory sub-node | In-process `deque(maxlen=10)` per session in `agent.py` |
| AI Agent | Orchestrator | Main agent loop in `agent.py` with tool dispatch |
| Google Calendar (getAll) | Tool | `calendar_tools.list_events(after, before)` |
| Google Calendar1 (create) | Tool | `calendar_tools.create_event(start, end, attendees, summary)` |

No Google Sheets / Airtable / Excel nodes in this workflow. Booking records are written via `write_rows()` from `io_store.py`.
