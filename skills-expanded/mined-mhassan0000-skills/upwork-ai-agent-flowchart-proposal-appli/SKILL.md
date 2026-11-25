# Upwork AI Agent (Flowchart + Proposal + Application Generator)

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) and writes **local Markdown files** for the proposal docs — nothing to connect, works offline, your data stays on your machine.

- Input/output CSVs: `data/input.csv` / `data/output.csv`
- Proposal docs: `data/proposals/<title>.md` — one file per job, rendered with the full template

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

If you'd rather have the proposal land in **Google Docs** (with a shareable link you can drop into the application), see Option C below.

---

## What this does

Takes an Upwork job description and generates three assets in one shot:

1. **Application copy** — a short, punchy proposal body in the "I do this all the time, here's proof" style that high-converting freelancers use. Drops a link placeholder (`$$$`) where your proposal doc link goes, then swaps it in automatically once the doc is created (Google Docs mode) or left as-is (local mode).
2. **Mermaid flowchart** — a `graph TD` flowchart of how the system described in the job would actually be built. Paste it into any Mermaid renderer (or inline in a Notion doc, GitHub, etc.) to show the prospect you already thought it through.
3. **Proposal doc** — a full structured proposal (title, brief explanation, step-by-step build plan, left-to-right flow summary, about-me bullets). By default written as a local `.md` file to `data/proposals/<title>.md`. Opt in to Google Docs (see Option C) to get a shareable link instead.

The original workflow was an n8n chat agent with three sub-workflows wired as tools. This skill does the same thing — same prompts, same logic — but runs locally via Python scripts and stores results in CSV (or Sheets if you configure it).

---

## When to trigger this

Trigger on any of:
- "generate upwork application"
- "write me a proposal for this job"
- "create flowchart + proposal for upwork"
- `/upwork-ai-agent`
- Pasting an Upwork job description and asking for application materials

---

## Env vars to set before running

Required:
```
OPENAI_API_KEY=sk-...
```

Optional (local mode, no Google needed):
```
OPENAI_MODEL=gpt-4o-mini          # default, swap for gpt-4o if you want better output
ABOUT_ME="..."                    # override the default "about me" block used in proposals
SKILL_STORE=sheets                # switch from CSV to Google Sheets (see top of file)
SKILL_SHEET_URL=https://...       # required if SKILL_STORE=sheets
```

Required only to opt in to Google Docs output (both must be set — see Option C):
```
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json   # must be type=service_account
PROPOSAL_TEMPLATE_DOC_ID=<doc-id-from-template-URL>
```

Optional Google Docs extras:
```
PROPOSAL_DRIVE_FOLDER_ID=...      # Google Drive folder to drop copied docs into
SKIP_GOOGLE_DOCS=1                # force local .md even when Google creds are set
```

> **Auto-detection:** if `GOOGLE_APPLICATION_CREDENTIALS` and `PROPOSAL_TEMPLATE_DOC_ID` are both
> set, the skill uses Google Docs automatically. If either is missing it falls back to local `.md`.
> Set `SKIP_GOOGLE_DOCS=1` to force local regardless.

---

## Step-by-step procedure

### Option A — single job (quick test or one-off)

Paste a job description and run:

```bash
cd /path/to/upwork-ai-agent-flowchart-proposal-appli
OPENAI_API_KEY=sk-... python scripts/run_agent.py --job "paste the full job description here"
```

Output prints to stdout: application copy, Mermaid code, and the path to the local `.md` proposal
(or a Google Doc URL if Google creds are configured).

### Option B — batch (process multiple jobs at once)

1. Open `data/input.csv`. It has two columns: `job_title` and `job_description`.
2. Add one row per job. Job description can be multiline — just wrap in quotes.
3. Run:

```bash
cd /path/to/upwork-ai-agent-flowchart-proposal-appli
OPENAI_API_KEY=sk-... python scripts/run_agent.py
```

4. Results land in `data/output.csv` with columns:
   - `job_title`
   - `job_description`
   - `application_copy` — the short proposal body ready to paste into Upwork
   - `mermaid_code` — paste into any Mermaid renderer
   - `proposal_doc_url` — absolute path to local `.md` file (or Google Doc URL if Google configured)
   - `proposal_json` — raw structured JSON from the proposal generator (for debugging)

Local `.md` proposals also land in `data/proposals/<title>.md` — one file per job.

### Option C — Google Docs setup (opt-in, one-time)

If you want proposals as shareable Google Docs instead of local `.md` files:
1. Create a Google service account in Google Cloud Console, download the JSON key (`type: service_account`).
2. Enable Drive API and Docs API on the project.
3. Create a template Google Doc using `{{titleOfSystem}}`, `{{briefExplanationOfSystem}}`, etc.
   as placeholders (the same field names in the proposal JSON schema above).
4. Copy the `PROPOSAL_TEMPLATE_DOC_ID` from the template URL (the long string between `/d/` and `/edit`).
5. Share the template doc + your target Drive folder with the service account's `client_email`.
6. Set `GOOGLE_APPLICATION_CREDENTIALS` and `PROPOSAL_TEMPLATE_DOC_ID` in your env and re-run.
   Both vars must be present for the Google path to activate.

---

## Scripts reference

| Script | What it does |
|---|---|
| `scripts/run_agent.py` | Main entry point. Reads input CSV, calls all three generators, writes output CSV. |
| `scripts/generate_application.py` | Calls OpenAI, returns proposal text with `$$$` placeholder. |
| `scripts/generate_mermaid.py` | Calls OpenAI, returns raw Mermaid `graph TD` code. |
| `scripts/generate_proposal_doc.py` | Calls OpenAI for structured JSON, then Drive/Docs API to copy template + fill placeholders. |
| `scripts/io_store.py` | CSV/Sheets toggle. All data reads/writes go through `read_rows()` / `write_rows()`. |

---

## Node map (original n8n workflow → this skill)

| n8n node | Script / function |
|---|---|
| `When chat message received` (chatTrigger) | `run_agent.py --job "..."` or batch via CSV |
| `AI Agent` (langchain.agent, GPT-4o, buffer memory) | orchestration logic in `run_agent.py` |
| `OpenAI Chat Model` | `OPENAI_API_KEY` + model via each generator script |
| `Window Buffer Memory` | not needed in batch mode; for interactive use, keep chat context yourself |
| `Generate Application Copy` (toolWorkflow) | `generate_application.py` |
| `Generate Google Doc Proposal` (toolWorkflow) | `generate_proposal_doc.py` |
| `Generate Mermaid.js` (toolWorkflow) | `generate_mermaid.py` |
| `Google Drive copy` | `generate_proposal_doc._google_doc_url()` — Drive API copy |
| `Google Drive share` | same function — permissions().create |
| `Google Docs update` | same function — batchUpdate with replaceAllText |
| `Set Variable` (aboutMe) | `DEFAULT_ABOUT_ME` constant in `run_agent.py`, overridable via `ABOUT_ME` env var |
| `Edit Fields` (response/url output) | return values from each generator function |
