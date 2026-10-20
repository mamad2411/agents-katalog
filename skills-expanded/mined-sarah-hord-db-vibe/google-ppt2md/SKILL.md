---
name: google-ppt2md
description: Converts Google Slides or local PowerPoint (.pptx) presentations into clean, LLM-optimized markdown with extracted images and speaker notes. Processes slide decks for AI context consumption by extracting text, tables, charts, architecture diagrams, and speaker notes into structured markdown. Triggers on /google-ppt2md invocation. Accepts Google Drive URLs, Google Slides links, Drive file IDs, or local .pptx file paths. Handles Shared Drives and large presentations automatically.
user-invocable: true
---

# Google PPT2MD

Convert Google Slides presentations or local .pptx files into structured markdown with extracted images, speaker notes, and visual context narratives.

## Usage

```
/google-ppt2md <Google Drive URL or local .pptx path>
```

Examples:
- `/google-ppt2md https://docs.google.com/presentation/d/1abc123/edit`
- `/google-ppt2md /path/to/presentation.pptx`

## Phase 1: Resolve Input

The input can be a Google Drive URL, a raw file ID, or a local path. The skill needs to end up with a local .pptx file regardless of source — the extraction engine (markitdown) works on local files only.

**Google Drive URL or file ID:**

```bash
uv run python3 resources/drive_export.py "<input>"
```

The script handles:
1. Parsing the file ID from various Google URL formats
2. Authenticating via gcloud ADC (same token source as all fe-google-tools skills)
3. Detecting whether the file is native Google Slides or an uploaded .pptx — this matters because native Slides need the Drive export API while uploaded .pptx files use the direct download endpoint
4. Saving the .pptx to `/tmp/{name}.pptx`
5. Outputting JSON: `{"path": "/tmp/name.pptx", "name": "name"}`

If auth fails, instruct the user to run `/google-auth` first.

**Local .pptx path:**
- Verify the file exists and has a `.pptx` extension
- Skip to Phase 2

## Phase 2: Extract & Transform

markitdown handles OOXML parsing but produces flat output (HTML comment slide markers, no heading hierarchy). The post-processor restructures this into clean markdown. python-pptx extracts content images that markitdown ignores.

```bash
uv run --with "markitdown[pptx]" --with python-pptx python3 resources/ppt2md.py <pptx_path> --source "<original_url_if_applicable>"
```

For text-only output (no image extraction): add `--no-images`.

The pipeline:
1. Extract text, tables, charts, and speaker notes via markitdown
2. Extract content images via python-pptx — filters out small decorative icons (< 1.5" in both dimensions), saves meaningful diagrams/screenshots to `./images/` subdirectory
3. Parse raw output into structured slide objects (splitting on `<!-- Slide number: N -->` markers)
4. Restructure into LLM-optimized markdown:
   - `# Presentation Title` with metadata (slide count, source link, image count)
   - `## Slide N: Title` headings — gives the LLM clear slide boundaries and navigation
   - Speaker notes as `> **Notes:**` blockquotes — inline with their slide because notes often contain the richest context (what the presenter actually says)
   - Images referenced with relative paths: `![alt](./images/slideNN_imgNN.png)` — Claude can read these directly when it needs to analyze a diagram
   - Tables and chart data preserved as-is (markitdown handles these well)
   - Empty/decorative slides removed
   - Whitespace normalized for token efficiency
   - `--no-images` flag available for text-only output

Output is written to a self-contained directory in the current working directory: `./{basename}/{basename}.md` with images in `./{basename}/images/` alongside it. This keeps output where the user's Claude session is running, not buried in `/tmp` or next to the source file.

## Phase 3: Enrich Slides with Visual Context

Slide text extracted from presentations is often just disconnected labels — product names, category headers, short phrases. The enrichment phase transforms these into impactful narratives that help SAs prepare for customer conversations — not just "what's on the slide" but "why this matters to the customer and how to talk about it."

This phase is split into two sub-phases: pre-fetching internal messaging context (once, upfront) and then enriching slides in parallel using the pre-fetched context. This avoids redundant MCP queries — instead of 2 searches per slide (hundreds of calls for large decks), we batch ~15-20 queries by topic upfront.

### Phase 3a: Pre-fetch messaging context

Extract unique topics from all slide titles and text, then batch query Glean and Confluence once.

**Step 1: Extract topics** — scan the generated markdown for slide titles and key terms. Deduplicate into a topic list. Common Databricks topics include: Lakehouse, Unity Catalog, MLOps, Model Serving, SDP, Mosaic AI, Delta Lake, MLflow, Feature Store, RAG, Agents, Governance, etc.

**Step 2: Batch query Glean** — for each unique topic (typically 10-15), search for internal messaging:

```
mcp__glean__search query: "Databricks {topic} value proposition customer messaging"
```

Extract the most relevant snippets: value propositions, competitive differentiators, customer success patterns, outcome metrics (e.g., "30-50% cost reduction", "10x faster time-to-insight").

**Step 3: Batch query Confluence** — for each topic, search for product messaging frameworks:

```
mcp__confluence__search_confluence_pages query: "{topic} messaging framework field guide"
```

Look for talk tracks, competitive positioning, and field engineering best practices.

**Step 4: Save to context file** — write the pre-fetched messaging to a JSON file alongside the markdown output:

```json
{
  "topics": {
    "Lakehouse": {
      "value_prop": "Unifies data warehousing, ETL, and AI on a single platform...",
      "differentiator": "Only open platform with built-in governance across all workloads...",
      "outcomes": ["30-50% infrastructure cost reduction", "Single copy of data"],
      "sources": ["Glean: Lakehouse pitch deck", "Confluence: FE Messaging Guide"]
    },
    "Unity Catalog": {
      "value_prop": "Unified governance for data and AI assets...",
      "differentiator": "Only catalog that governs tables, models, and functions together...",
      "outcomes": ["Centralized access control", "Automated lineage"],
      "sources": ["Glean: UC competitive positioning"]
    }
  }
}
```

This file is the single source of messaging context for all enrichment workers. Fetching it takes ~40-60 seconds upfront but eliminates hundreds of MCP calls during enrichment.

### Phase 3b: Parallel enrichment with pre-fetched context

Workers read images + the pre-fetched messaging context to write narratives. No MCP calls during this phase.

**Count slides with images** in the markdown (count lines matching `![`).

| Slides with images | Workers |
|---|---|
| < 20 | 1 (sequential, no fan-out) |
| 20-40 | 2 |
| 41-70 | 3 |
| 71+ | 4 |

**Dispatch workers** — launch all agents in a single message. Each worker gets:

```
You are enriching slides from a Databricks presentation with customer-facing
visual context narratives.

Read the markdown file at: {output_path}
Read the messaging context at: {context_json_path}
Process ONLY slides {start_num} through {end_num}.

For each slide in your range that has an image reference:
1. Read the image file to understand the visual layout
2. Identify the key topics from the slide title and text labels
3. Look up those topics in the messaging context JSON for value props,
   differentiators, and outcome metrics
4. Write a **Visual context** narrative (2-4 sentences) that:
   - Leads with the customer problem this slide addresses
   - Explains the Databricks approach and why it's differentiated
   - Cites specific outcomes where available (cost %, speed improvement)
   - Uses a conversational SA-to-customer tone
5. For simple charts/screenshots, keep it to 1 sentence

Output format — return ONLY a JSON array:
[
  {"slide_num": 8, "context": "Customers often struggle with..."},
  {"slide_num": 12, "context": "This architecture eliminates..."}
]

Skip slides without images. Skip slides where text alone is sufficient.
Do NOT make any MCP calls — all messaging context is in the JSON file.
```

**Merge results** — collect all worker JSON arrays, insert each `**Visual context:**` paragraph into the markdown between the slide's text content and the image reference.

### Narrative tone

The narrative should sound like an SA explaining to a customer:
- **Value-oriented** — lead with the customer problem, not the feature list
- **Differentiated** — what makes Databricks unique vs alternatives
- **Outcome-focused** — specific business outcomes (cost, speed, governance)
- **Conversational** — natural, not a marketing brochure

### Example

Before:
```
## Slide 8: The Data Lakehouse

Open Data Lake
All raw data
(Logs, texts, audio, video, images)
ETL & Real-time Analytics
Orchestration
Data Warehousing
Data Science & AI

![Slide 8 thumbnail (rendered from shapes)](./images/slide08_thumb.png)
```

After:
```
## Slide 8: The Data Lakehouse

Open Data Lake
All raw data
(Logs, texts, audio, video, images)
ETL & Real-time Analytics
...

**Visual context:** Customers typically manage separate systems for data
warehousing, ETL, and AI — each with its own copy of the data, its own
governance model, and its own team. The Lakehouse eliminates this by unifying
all workloads on a single open data lake foundation. The architecture shown
here demonstrates how SQL analytics, real-time streaming, and Mosaic AI all
operate on the same data without duplication, reducing infrastructure costs
by 30-50% while enabling teams to move from raw data to production AI models
without data movement.

![Slide 8 thumbnail (rendered from shapes)](./images/slide08_thumb.png)
```

## Phase 4: Deliver

Report to the user:
- Presentation title
- Number of slides converted
- Number of images extracted
- Number of slides enriched with visual context
- Output file path

## Prerequisites

- **Google auth** (for Drive URLs only): Run `/google-auth` to authenticate
- **markitdown[pptx]**: Installed automatically via `uv run --with`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Google auth not configured" | Run `/google-auth` to authenticate with Google |
| "File not found in Google Drive" | Check the URL is correct and you have access |
| "Permission denied" | Request access to the file from the owner |
| "markitdown not installed" | Run `uv pip install 'markitdown[pptx]'` |
| "Only .pptx files are supported" | This skill does not support .ppt (legacy format). Convert to .pptx first in Google Slides or PowerPoint. |
| Empty or corrupted output | Try re-exporting the file from Google Slides |
