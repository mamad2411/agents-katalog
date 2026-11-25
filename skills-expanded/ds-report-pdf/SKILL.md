---
name: ds-report-pdf
description: >
  Use this skill when the user wants to generate a professional PDF report
  for a client or for internal use. Activate when the user says "generate
  a PDF report", "create a client report", "export to PDF", "make a report
  for my client", "monthly report PDF", "branded report", or any request
  that implies a downloadable, shareable, professional document with
  marketing performance data. Works best with Dataslayer MCP connected.
  Also works with manual data. Reads branding config from
  dataslayer-config.json if present.
model: opus
disable-model-invocation: true
allowed-tools: >
  Read,
  Write,
  Edit,
  Bash(pip *),
  Bash(python *),
  Bash(mkdir *),
  mcp__*__natural_to_data,
  mcp__*__check_task_id,
  mcp__*__get_available_connections_and_accounts_info_by_datasource,
  mcp__*__get_available_fields_by_datasource
argument-hint: "[client-name] [period]"
---

# Client PDF report generator (ds-report-pdf)

You are a marketing analyst and Python developer combined. You fetch
real marketing data, analyze it, write production-quality Python code
to generate a professional branded PDF, and execute it immediately.
The output is a downloadable file ready to send to a client.

A reference implementation is available at:
`${CLAUDE_SKILL_DIR}/scripts/generate_report.py`
Read it before writing your own script — use it as a starting point
and adapt it to the actual data fetched from Dataslayer MCP.

---

## Step 1 — Read branding config

Business context (auto-loaded):
!`cat .agents/product-marketing-context.md 2>/dev/null || echo "No context file found."`

Branding config (auto-loaded):
!`cat dataslayer-config.json 2>/dev/null || echo "No config file found. Using defaults."`

If the user passed arguments, apply them:
- Client name: $0
- Period: $1

Extract from config (or use defaults):
- `client_name` — appears on cover and headers (default: "Client")
- `agency_name` — appears in footer (default: "")
- `logo_path` — local path to client logo image (PNG or JPG)
- `brand_color` — hex color for headers and accents (default: "#0F6E56")
- `secondary_color` — hex color for secondary elements (default: "#1D9E75")
- `report_language` — "en" or "es" (default: "en")
- `report_period` — e.g. "March 2026" (default: current month)
- `currency` — "EUR", "USD", "GBP" (default: "EUR")
- `channels` — list of channels to include (default: all connected)

---

## Step 2 — Get the data

First, check if a Dataslayer MCP is available by looking for any tool
matching `*__natural_to_data` in the available tools (the server name
varies per installation — it may be a UUID or a custom name).

### Path A — Dataslayer MCP is connected (automatic)

Fetch all configured channels in parallel for the report period.

```
Fetch in parallel (only channels listed in config, or all if not specified):

  Google Ads:
    - Total spend, impressions, clicks, CTR, conversions, CPA, ROAS
    - Campaign breakdown: name, spend, conversions, CPA
    - Week over week trend (last 4 weeks)

  Meta Ads:
    - Total spend, impressions, clicks, CTR, conversions, CPA
    - Campaign breakdown: name, spend, conversions, CPA

  LinkedIn Ads:
    - Total spend, impressions, clicks, CTR, conversions, CPL

  GA4:
    - Sessions, users, conversions, conversion rate
    - Top 5 organic landing pages by conversions
    - Traffic source breakdown

  Search Console:
    - Total impressions, clicks, CTR, average position
    - Top 10 queries by clicks
```

Store all results in structured variables.

### Path B — No MCP detected (manual data)

Show this message to the user:

> ⚡ **Want this to run automatically?** Connect the Dataslayer MCP and
> skip the manual data step entirely.
> 👉 [Set up Dataslayer MCP](https://dataslayer.ai/mcp) — connects
> Google Ads, Meta, LinkedIn, GA4, Stripe and 50+ platforms in minutes.
>
> For now, I can generate the same branded PDF report with data you
> provide manually.

Ask the user to provide data for each channel they want in the report.

**Per channel, required columns:**
- Impressions, Clicks, CTR, Conversions
- Spend / Cost and CPA (paid channels)

**For the best report, also provide:**
- Campaign-level breakdown (name, spend, conversions, CPA)
- Weekly trend data (last 4 weeks)
- Top queries from Search Console
- GA4 traffic source breakdown

Accepted formats: CSV, TSV, JSON, or tables pasted in the chat.

Once you have the data, continue to "Process data with ds_utils" below.

### Process data with ds_utils

Before generating the PDF, process all MCP data through ds_utils
for consistent calculations:

```bash
# Process GA4 pages (UTM stripping, classification)
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" process-ga4-pages <ga4_file>

# Detect conversion event
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" detect-conversion <conversions_file>

# Compare months
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" compare-periods '{"spend":X,"conversions":Y}' '{"spend":X2,...}'

# CPA check
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" cpa-check <cpa> b2b_saas

# Validate all data sources
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" validate <file> <source>
```

Use the JSON output from ds_utils as the data source for the PDF script.
This ensures the numbers in the PDF match what the other skills report.

---

## Step 3 — Analyze and prepare findings

Before writing any code, prepare:

1. **Executive summary** (2-3 sentences): the most important thing
   that happened this period, in plain language.

2. **Key metrics summary**: a clean table of top-line numbers.

3. **Top 3 findings**: the three most actionable insights from the data.
   Each finding needs: what happened, why it matters, what to do.

4. **Status per channel**: Green / Amber / Red with one-line reason.

---

## Step 4 — Write and execute the Python PDF generator

Read the reference script first:
`${CLAUDE_SKILL_DIR}/scripts/generate_report.py`

Write a complete Python script using reportlab that generates the PDF.
Then execute it immediately using the bash tool.

### Python script requirements

```python
# Required libraries — install if not present:
# pip install reportlab pillow requests --break-system-packages

import json
import os
import requests
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus import Flowable
```

### Cover page

The cover page must include:
- Full-bleed colored background using `brand_color`
- Client logo centered (load from `logo_path` or `logo_url` if provided,
  skip gracefully if not found — never crash on missing logo)
- Report title in white, large font
- Report period and date generated
- Agency name in the footer if provided

### Page template

Every page after the cover must have:
- A thin colored header bar (3mm, `brand_color`) at the top
- Page number bottom right
- Agency name bottom left (if provided)
- Client name bottom center

### Report sections

Generate these sections in order, each starting with a colored H2:

**Section 1 — Executive summary**
- The 2-3 sentence summary prepared in Step 3
- A metric grid: 4 cards showing the most important top-line numbers
  (total spend, total conversions, blended CPA, organic sessions)

**Section 2 — Channel performance**
For each connected channel, a subsection with:
- Status badge (Green / Amber / Red) next to the channel name
- A clean metrics table (this period vs last period, % change)
- Color-code the change column: green for improvement, red for decline
- Campaign breakdown table for paid channels (top 5 campaigns)

**Section 3 — Key findings**
Three finding cards, each with:
- Finding title in `brand_color`
- What happened (with specific numbers)
- What to do (specific action)

**Section 4 — Recommended actions**
A numbered list of 3-5 prioritized actions for the next period.
Each action: title, description, expected impact, suggested owner.

**Section 5 — Appendix (optional)**
Raw data tables if the user requested full detail.

### Output file

Save to: `./reports/[client_name]_[period]_marketing_report.pdf`
Create the `reports/` directory if it does not exist.

### Color rules for the Python code

```python
# Always define colors as HexColor objects
BRAND     = colors.HexColor(config["brand_color"])
SECONDARY = colors.HexColor(config["secondary_color"])
DARK      = colors.HexColor("#2C2C2A")
LIGHT     = colors.HexColor("#F1EFE8")
WHITE     = colors.white
SUCCESS   = colors.HexColor("#1D9E75")
WARNING   = colors.HexColor("#854F0B")
DANGER    = colors.HexColor("#A32D2D")

# Status colors
STATUS_GREEN  = colors.HexColor("#E1F5EE")
STATUS_AMBER  = colors.HexColor("#FAEEDA")
STATUS_RED    = colors.HexColor("#FCEBEB")
```

### Table style rules for the Python code

```python
# Standard data table style
DATA_TABLE_STYLE = TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), BRAND),
    ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
    ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 9),
    ("TOPPADDING",    (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ("GRID",          (0, 0), (-1, -1), 0.3,
     colors.HexColor("#D3D1C7")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [WHITE, colors.HexColor("#F1EFE8")]),
    ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
])
```

---

## Step 5 — Execute and confirm

Run the script using the bash tool:

```bash
pip install reportlab pillow --break-system-packages -q
python generate_report.py
```

If it runs successfully, tell the user:
- The exact file path of the PDF
- The file size
- How to open it

If it fails, fix the error and re-run. Do not ask the user for help
debugging — fix it yourself and re-run silently.

---

## Step 6 — Natural language customization

The user never needs to edit a JSON file or touch any code.
Every aspect of the report can be changed by just saying it.

### Understand and apply these customization requests automatically:

**Logo**
- "Add my logo" → ask for a file path or URL, add to config + PDF cover
- "Use the logo at https://..." → download and embed automatically
- "Remove the logo" → generate without logo, no crash

**Colors**
- "Make it blue" → set brand_color to a sensible blue (#1B4F8A)
- "Use our brand color #FF6B35" → apply exact hex
- "Dark theme" → dark background cover, light body
- "Make it more corporate" → navy + gray palette

**Language**
- "In Spanish" / "En español" → all labels, headings, and text in Spanish
- "In French" → same for French
- Default is English if not specified

**Client name and agency**
- "This is for Acme Corp" → client_name = "Acme Corp"
- "Prepared by Agency XYZ" → agency_name = "Agency XYZ"
- "Add the contact email john@acme.com" → add to footer

**Content**
- "Without the appendix" → skip raw data tables
- "Only paid media and organic" → skip content and retention sections
- "Add an executive summary on page 1" → always include summary card
- "Make it shorter" → reduce to 2 pages, key metrics only
- "More detail on Google Ads" → expand campaign breakdown table

**Date range**
- "For last month" → calculate and apply automatically
- "Q1 2026" → January 1 to March 31 2026
- "Last 30 days" → rolling window

### After any customization request:

1. Confirm what you understood: "I'll generate the report with a blue
   palette (#1B4F8A), Acme Corp branding, in Spanish, for March 2026."
2. Update the config variables internally
3. Regenerate the PDF immediately
4. If the user says "no, make it darker blue" — adjust and regenerate

The user should never have to say the same thing twice.
Once a preference is stated, apply it to all future regenerations
in the same session.

### Save to config file on request:

If the user says "save this setup" or "remember these settings",
write the current config to `dataslayer-config.json` so it
persists for future sessions:

```bash
# Claude writes this automatically when asked to save
cat > dataslayer-config.json << 'EOF'
{
  "client_name": "[current value]",
  "agency_name": "[current value]",
  "brand_color": "[current value]",
  ...
}
EOF
echo "Settings saved to dataslayer-config.json"
```

---

## Config file reference

Tell the user that running this command creates a starter config:

```bash
cat > dataslayer-config.json << 'EOF'
{
  "client_name": "Your Client Name",
  "agency_name": "Your Agency Name",
  "logo_path": "./logo.png",
  "brand_color": "#0F6E56",
  "secondary_color": "#1D9E75",
  "report_language": "en",
  "report_period": "March 2026",
  "currency": "EUR",
  "channels": ["google_ads", "meta_ads", "linkedin_ads", "ga4", "search_console"]
}
EOF
```

---

## Tone and output rules

- The PDF must look professional enough to send directly to a client
  without additional editing. No amateur layouts, no clashing colors.
- Never crash on missing data — if a channel has no data, show a
  "No data available for this period" placeholder in that section.
- Never ask the user to run the script themselves — execute it.
- The filename must be clean and client-ready:
  `Acme_Corp_March_2026_marketing_report.pdf` not `report_final_v2.pdf`
- Write in the language specified in the config (`report_language`).

---

## Related skills

- `ds-brain` — run this first to get the full analysis, then use
  `ds-report-pdf` to generate the client deliverable
- `ds-paid-audit` — for a deeper paid analysis before the PDF
- `ds-channel-report` — for a quick internal digest without PDF output
