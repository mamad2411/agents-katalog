# AI Automatic Proposal Generator Flow

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Takes post-discovery-call notes (filled in via Typeform or manually into CSV) and auto-generates a complete sales proposal — problem pitch, solution pitch, 4 milestones with timelines, and pricing — then creates a signed PandaDoc document from a template. The original Make.com flow was: Typeform webhook trigger → fetch latest response → filter for "Send proposal" outcome → GPT-4 generates proposal JSON → GPT-4 generates milestones JSON → PandaDoc creates document from template.

This skill replaces the webhook/polling loop with a simple CSV-driven CLI you can run any time. Each row in `data/input.csv` is one discovery call. Rows where `outcome != "Send proposal"` are skipped.

## When to trigger

- After a discovery call where you want to auto-generate and send a proposal
- Batch: drop multiple rows in `data/input.csv`, run once, get all proposals created in PandaDoc
- Testing: populate `data/input.csv` with fake data, set `DRY_RUN=1` to skip PandaDoc and just write proposal JSON to `data/output.csv`

## Required env vars

```
OPENAI_API_KEY=sk-...
PANDADOC_API_KEY=...
PANDADOC_TEMPLATE_ID=dbmxWR7jB6y3E6TzdC2buT   # "[Company Name] LeftClick Proposal"
PANDADOC_RECIPIENT_ROLE=Client                  # must match the template's role name exactly
SENDER_FIRST_NAME=Nick
SENDER_LAST_NAME=Saraev
SENDER_EMAIL=info@leftclick.ai
SENDER_COMPANY=LeftClick
DRY_RUN=0   # set to 1 to skip PandaDoc and write output.csv only
```

## Step-by-step procedure

1. **Populate input** — fill `data/input.csv` with one row per discovery call. See the sample file. Required columns: `client_first_name`, `client_last_name`, `client_email`, `client_company`, `business_description`, `problem`, `solution`, `tools`, `timeline`, `project_price`, `platform_costs`, `outcome`. Only rows where `outcome == "Send proposal"` are processed.

2. **Run the pipeline**:
   ```bash
   cd /path/to/skill/
   python3 scripts/run_pipeline.py --input data/input.csv --output data/output.csv
   ```
   Optional flags:
   - `--dry-run` — generate proposal JSON, write to output CSV, skip PandaDoc
   - `--input PATH` — override input CSV path
   - `--output PATH` — override output CSV path

3. **What happens per row**:
   - Skips rows where `outcome != "Send proposal"`
   - Calls `scripts/generate_proposal.py` → GPT-4 returns `{problemPitch, solutionPitch, title, platformList}`
   - Calls `scripts/generate_milestones.py` → GPT-4 returns `{milestone-1..4, timeline-1..4}`
   - Calls `scripts/create_pandadoc.py` → creates PandaDoc document from template, populates all tokens and pricing tables
   - Writes result row (doc ID, doc URL, status) to output CSV

4. **Check output** — `data/output.csv` has one row per processed lead with `pandadoc_doc_id`, `pandadoc_doc_url`, `proposal_title`, `status`.

## Scripts

| Script | What it does |
|---|---|
| `scripts/io_store.py` | CSV/Sheets data layer (verbatim pattern) |
| `scripts/run_pipeline.py` | Entry point — reads input, loops rows, orchestrates the 3 steps |
| `scripts/generate_proposal.py` | GPT-4 call: generates problemPitch, solutionPitch, title, platformList |
| `scripts/generate_milestones.py` | GPT-4 call: generates 4 milestones + timelines |
| `scripts/create_pandadoc.py` | PandaDoc API: creates document from template with all tokens + pricing |

## Node map (original Make.com → this skill)

| Make node | ID | Maps to |
|---|---|---|
| Typeform webhook trigger | 57 | `data/input.csv` rows |
| Sleep 2s | 58 | removed (not needed in CLI) |
| Typeform ListResponses | 59 | `read_rows()` in `run_pipeline.py` |
| Filter "Send proposal?" | 63 | `if row["outcome"] != "Send proposal": continue` |
| OpenAI Generate Proposal | 63 | `scripts/generate_proposal.py` |
| ParseJSON (proposal) | 88 | `json.loads()` in pipeline |
| OpenAI Generate Milestones | 72 | `scripts/generate_milestones.py` |
| ParseJSON (milestones) | 73 | `json.loads()` in pipeline |
| PandaDoc Create Document | 90 | `scripts/create_pandadoc.py` |
