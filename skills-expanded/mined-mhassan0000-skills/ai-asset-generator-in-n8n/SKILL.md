# AI Asset Generator in n8n

> Converted from the "AI Graphic Designer Agent" n8n workflow. Generates logos, style guides, gradient backgrounds, and image edits using OpenAI gpt-image-1. Optional upscaling via Replicate. Saves all outputs locally.

## Before you run this

By default this skill uses **local CSV files** for its data (input and output) — nothing to connect, works offline, your data stays on your machine. The CSVs live next to the skill in `./data/` (input: `data/input.csv`, output: `data/output.csv`), or point it at any path you like.

If you'd rather read/write a **Google Sheet** instead, just say so and I'll switch you over. It's a one-time setup: you'll paste a Google service-account JSON (or authorize once), share your Sheet with that account's email, and give me the Sheet URL. After that it behaves exactly the same, just backed by your Sheet. Say **"use Google Sheets"** to start that, or **"keep CSVs"** (default) to just go.

---

## What it does

Takes a list of image generation jobs (type + prompt + optional reference image) and produces PNG files for each one using OpenAI's gpt-image-1 model. Four asset types are supported:

- **logo** — generates a new image from a prompt (no reference needed)
- **style_guide** — generates a branded style guide sheet, optionally using an existing brand asset as reference
- **gradient** — generates a mesh/abstract gradient background, optionally layered on a reference image
- **edit** — takes an existing image (URL or local file) and applies revision instructions to it

After generation, each output is saved to `data/outputs/<job_id>.png`. A summary CSV (`data/output.csv`) logs every job with its status, local path, and any errors.

Optionally, you can call the upscale step (x2 or x4) on any output URL using Replicate's google/upscaler model — just provide the URL and factor.

This replaces the full n8n agent graph: the orchestrator AI Agent, four sub-workflow tools (Generate Logo, Generate Style Guide, Generate Gradient Background, Edit/Revise Image), and the Upscale Image HTTP tool. The Google Drive upload/share nodes from the original are skipped by default — files stay local. If you want Drive upload, ask and I'll add it.

---

## When to trigger

Use this skill when:

- You need to batch-generate brand assets (logos, backgrounds, style guides) from a list of briefs
- Someone gives you image revision instructions and a reference URL
- You want to upscale an existing image URL by 2x or 4x
- You're running the original "AI Graphic Designer Agent" n8n workflow locally without n8n

Trigger phrases: "generate a logo", "make a style guide", "create a gradient background", "edit this image", "upscale this image", "run the AI asset generator", "batch generate brand assets".

---

## Node map (original workflow → this skill)

| Original node | Type | Maps to |
|---|---|---|
| When chat message received | chatTrigger | CLI args / user prompt |
| AI Agent (gpt-4.1) | LangChain agent | Orchestration logic in this SKILL.md |
| Simple Memory | memoryBufferWindow | Conversational context (handled by Claude) |
| Generate Logo (toolWorkflow) | Sub-workflow | `generate_asset.py --type logo` |
| Generate Style Guide (toolWorkflow) | Sub-workflow | `generate_asset.py --type style_guide` |
| Generate Gradient Background (toolWorkflow) | Sub-workflow | `generate_asset.py --type gradient` |
| Edit/Revise Image (toolWorkflow) | Sub-workflow | `generate_asset.py --type edit` |
| Upscale Image (httpRequestTool → Replicate) | HTTP | `generate_asset.py` upscale path |
| OpenAI node — gpt-image-1 (Logo sub) | OpenAI images/generations | `generate_logo()` in generate_asset.py |
| HTTP Request — /v1/images/edits (Style/Gradient/Edit subs) | HTTP multipart | `generate_with_reference()` in generate_asset.py |
| Google Drive download | googleDrive | `--reference-image` arg (URL or local path) |
| Google Drive upload + share | googleDrive | Skipped (local save to data/outputs/) |
| Convert to File | convertToFile | Handled internally (base64 decode → PNG) |
| Edit Fields (set output fields) | set | Output row written to data/output.csv |
| Switch (Google vs Non-Google URL) | switch | URL type detection in `generate_with_reference()` |

---

## Required env vars

```
OPENAI_API_KEY=sk-...          # Required — all generation and edit calls
REPLICATE_API_KEY=r8_...       # Optional — only needed for upscaling
```

Set in your shell or a `.env` file. Never hardcode.

---

## Step-by-step procedure

### Single asset (interactive)

1. Make sure `OPENAI_API_KEY` is set.
2. Run:
   ```bash
   python3 scripts/generate_asset.py \
     --type logo \
     --prompt "Minimal wordmark for a fintech app called Vault, dark navy and gold" \
     --output data/output.csv
   ```
3. The PNG lands in `data/outputs/<job_id>.png`. The result row is appended to `data/output.csv`.

For an edit (reference image required):
```bash
python3 scripts/generate_asset.py \
  --type edit \
  --prompt "Change the background to white and remove the tagline" \
  --reference-image https://your-image-url.com/image.png \
  --output data/output.csv
```

### Batch mode

1. Fill in `data/input.csv` with one row per job. Columns: `job_id, asset_type, prompt, reference_image, size`.
   - `reference_image` can be a URL or local file path. Leave blank for logo/style_guide/gradient if you have no reference.
   - `size` defaults to `1024x1024`. Use `1536x1024` for landscape, `1024x1536` for portrait. (`1792x1024` is not supported by gpt-image-1.)
2. Run:
   ```bash
   python3 scripts/generate_asset.py --batch --input data/input.csv --output data/output.csv
   ```
3. All PNGs go to `data/outputs/`. The full results table is written to `data/output.csv`.

### Upscaling

Call this after generation — pass the URL of the image you want upscaled:
```bash
python3 scripts/upscale.py --image-url https://... --factor x2 --output data/output.csv
```
Requires `REPLICATE_API_KEY`. Returns the Replicate output URL and appends to the results CSV.

### Google Sheets mode

Set these env vars, then re-run any command above:
```
SKILL_STORE=sheets
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
SKILL_SHEET_URL=https://docs.google.com/spreadsheets/d/...
```
`io_store.py` will read jobs from the Sheet and write results back to it automatically. The Sheet must be shared with the service account's email.

---

## Output CSV schema

| Column | Description |
|---|---|
| job_id | Short unique ID for the job |
| asset_type | logo / style_guide / gradient / edit |
| prompt | The generation prompt used |
| local_path | Path to the saved PNG (e.g. data/outputs/job001.png) |
| status | ok / error |
| error | Error message if status=error, else empty |
