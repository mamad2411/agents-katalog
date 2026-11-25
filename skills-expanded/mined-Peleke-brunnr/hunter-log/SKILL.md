---
name: hunter-log
description: Persistence layer for the hunter product discovery pipeline. Takes PipelineEnvelope JSON from any pipeline skill (signal-scan, decision-log, persona-extract, offer-scope) and saves it as structured, Obsidian-compatible markdown with proper frontmatter, tags, cross-links, session tracking, and kanban board updates.
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F4D2"
---

# Hunter Log

Persistence layer for the hunter product discovery pipeline. Receives structured JSON output wrapped in a PipelineEnvelope, renders it as Obsidian-compatible markdown, and writes it to the vault with frontmatter, wikilinks, session tracking, and kanban board updates.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## When to Use

- After any pipeline skill produces output and it needs to be saved
- When manually saving a PipelineEnvelope payload to the Obsidian vault
- When updating the session log or kanban board for an existing pipeline run
- When appending new results to an existing document in the vault

## Trigger Phrases

- "Save this to the vault"
- "Log this pipeline output"
- "Persist the scan results"
- "/hunter-log {envelope}"
- "Write this decision to Obsidian"

---

## Prerequisites

Before starting, you need exactly one thing:

1. **PipelineEnvelope** -- A JSON object wrapping the output of a pipeline skill. Must conform to the schema in [references/pipeline-envelope-schema.json](references/pipeline-envelope-schema.json).

If the caller provides raw skill output without an envelope, ask for the envelope fields (skill, session_id, timestamp, input_refs) or construct one from context.

---

## Pipeline Context

```
signal-scan --> decision-log --> persona-extract --> offer-scope
                     |                |                  |
               hunter-log       hunter-log         hunter-log
            (persistence)     (persistence)      (persistence)
```

hunter-log sits below every pipeline skill. It does NOT do analysis. It only formats and saves.

---

## Vault Layout

All files are written under the Obsidian vault base path (iCloud-synced):

```
${VAULT}/Admin/Product-Discovery/
```

```
Admin/Product-Discovery/
  Pipeline.kanban.md            # Master kanban board
  _index.md                     # Index with dataview queries
  Signal-Scans/                 # from signal-scan
  Decisions/                    # from decision-log
  Personas/                     # from persona-extract
  Offers/                       # from offer-scope
  Sessions/                     # session logs (one per session_id)
```

---

## Workflow

```
PipelineEnvelope (JSON)
    |
Phase 1: Envelope Parsing -- validate, extract skill type + output
    |
Phase 2: File Path Resolution -- map to directory, generate slug, check collisions
    |
Phase 3: Frontmatter Generation -- schema-driven per document type
    |
Phase 4: Body Rendering -- markdown from JSON using templates
    |
Phase 5: Write to Vault -- create or append
    |
Phase 6: Session Log Update -- create or append session file
    |
Phase 7: Kanban Board Update -- move/create card in Pipeline.kanban.md
    |
Output: confirmation with file path + wikilink
```

---

## Phase 1: Envelope Parsing

Read the PipelineEnvelope and extract:

- `skill` -- determines document type and target directory
- `session_id` -- links to session log
- `timestamp` -- used in frontmatter and append headings
- `input_refs` -- used for "Based On" cross-links
- `output` -- the skill's JSON payload to render

**Validation rules:**
- `skill` must be one of: `signal-scan`, `decision-log`, `persona-extract`, `offer-scope`
- `version` must be `"1.0"`
- `session_id` must match format `session-YYYY-MM-DD-NNN`
- `output` must be present and non-null

If validation fails, report the specific field and stop. Do not write partial files.

---

## Phase 2: File Path Resolution

Map skill type to vault subdirectory:

| Skill | Directory |
|-------|-----------|
| signal-scan | Signal-Scans/ |
| decision-log | Decisions/ |
| persona-extract | Personas/ |
| offer-scope | Offers/ |

**Filename generation:**
- Pattern: `{domain-slug}-{YYYY-MM-DD}.md`
- Domain slug: lowercase, hyphens for spaces, strip special characters
- Example: `devops-education-2025-06-15.md`

**Collision handling:**
- If the file already exists at the resolved path, do NOT overwrite
- Instead, append under a new `## Update: {ISO timestamp}` heading
- Update frontmatter `status` if the new data changes it

---

## Phase 3: Frontmatter Generation

Use the schema for the document type. See [references/templates.md](references/templates.md) for full templates with frontmatter schemas.

### Signal Scan Frontmatter
```yaml
type: signal-scan
domain: string
date: YYYY-MM-DD
session: string
operator_edge: string
top_opportunity: string
top_score: number
opportunity_count: number
status: complete | partial
tags: [hunter/scan, hunter/domain/{slug}]
```

### Decision Frontmatter
```yaml
type: decision
date: YYYY-MM-DD
session: string
domain: string
chosen_opportunity: string
alternatives_considered: [string]
confidence: low | medium | high
revisit_by: YYYY-MM-DD
status: active | superseded | abandoned
signal_scan: string
tags: [hunter/decision, hunter/domain/{slug}]
```

### Persona Frontmatter
```yaml
type: persona
date: YYYY-MM-DD
session: string
domain: string
opportunity: string
persona_name: string
experience_range: string
pain_intensity: number
willingness_to_pay: none | low | medium | high | proven
decision_ref: string
status: complete | partial
tags: [hunter/persona, hunter/domain/{slug}, hunter/opportunity/{slug}]
```

### Offer Frontmatter
```yaml
type: offer-spec
date: YYYY-MM-DD
session: string
domain: string
opportunity: string
product_name: string
format: string
price_point: string
ship_time: string
persona_ref: string
decision_ref: string
status: spec | building | shipped | killed
tags: [hunter/offer, hunter/domain/{slug}, hunter/format/{type}, hunter/price/{range}]
```

### Session Frontmatter
```yaml
type: session
date: YYYY-MM-DD
session_id: string
domain: string
pipeline_steps_completed: [string]
steps_remaining: [string]
artifacts: [string]
status: in-progress | complete
tags: [hunter/session]
```

---

## Phase 4: Body Rendering

Render the document body from the envelope's `output` field using the templates in [references/templates.md](references/templates.md).

**Rendering rules:**

- Use Obsidian-compatible markdown: `[[wikilinks]]`, `> [!note]` callouts, standard tables
- Include a `## Based On` section with wikilinks to upstream artifacts (from `input_refs`)
- Tables, lists, and formatted data should come directly from the output JSON
- Do not invent or embellish data -- render exactly what the output contains
- For signal scans: include opportunity ranking table, signal highlights, ship candidates
- For decisions: include rationale, alternatives table, next steps
- For personas: include demographics, pain points, willingness-to-pay evidence
- For offers: include spec table, persona fit, distribution plan

---

## Phase 5: Write to Vault

**Base path:** `${VAULT}/Admin/Product-Discovery/`

**New file:**
- Write complete document: YAML frontmatter block + rendered body
- Confirm the file path in output

**Existing file (append):**
- Read existing file first
- Append under `## Update: {ISO timestamp}` heading
- Update frontmatter `status` field if the new data changes it (e.g., partial -> complete)
- Do not duplicate existing content

---

## Phase 6: Session Log Update

Session files live at `Sessions/{session_id}.md`.

**If session file does not exist:**
- Create it with session frontmatter (see Phase 3)
- Add the current artifact as the first entry in the artifacts list
- Set `pipeline_steps_completed` to `[{current skill}]`
- Set `steps_remaining` to the skills not yet completed

**If session file exists:**
- Read it
- Append the new artifact wikilink to the `artifacts` list in frontmatter
- Add the current skill to `pipeline_steps_completed`
- Remove it from `steps_remaining`
- If all four steps are complete, set `status: complete`
- Append a log line to the body: `- {timestamp}: Saved {skill} output -> [[{filename}]]`

---

## Phase 7: Kanban Board Update

The kanban board lives at `Pipeline.kanban.md`.

**Column mapping:**

| Skill | Target Column |
|-------|--------------|
| signal-scan | Signal Scanned |
| decision-log | Decision Made |
| persona-extract | Persona Researched |
| offer-scope | Offer Scoped |

**If card exists** (match by domain name):
- Move the card from its current column to the target column
- Update the card's details (score, opportunity, wikilink)

**If card does not exist:**
- Create a new card in the target column

**Card format:**
```markdown
- [ ] **{Domain}** #hunter/domain/{slug}
  Score: {X}/10 | Top: {opportunity}
  [[{subdir}/{filename}]]
```

**Board structure** (see [references/templates.md](references/templates.md) for the full kanban template):
```markdown
---
kanban-plugin: basic
---

## Signal Scanned
## Decision Made
## Persona Researched
## Offer Scoped
## Building
## Shipped
## Killed
```

---

## Output

After completing all phases, return a confirmation containing:

- File path written (absolute)
- Wikilink for cross-referencing: `[[Admin/Product-Discovery/{subdir}/{filename}]]`
- Session log status (created or updated)
- Kanban board status (card created or moved)
- Any warnings (e.g., file appended instead of created, missing optional fields)

---

## Resources

### references/

- `pipeline-envelope-schema.json` -- JSON Schema for the PipelineEnvelope wrapper. Load when validating inbound envelopes.
- `templates.md` -- Markdown rendering templates for each document type (signal scan, decision, persona, offer, session) plus the kanban board format. Load when rendering output.

---

## Quality Checklist

Run this checklist before confirming the write:

- [ ] Envelope validates against `references/pipeline-envelope-schema.json`
- [ ] Frontmatter matches the schema for the document type
- [ ] All wikilinks use correct relative paths within Product Discovery/
- [ ] Tags follow the `hunter/` hierarchy (hunter/scan, hunter/domain/{slug}, etc.)
- [ ] Session log created or updated with new artifact
- [ ] Kanban card moved to correct column (or created if new)
- [ ] Existing files appended with timestamp heading, not overwritten
- [ ] Filename slug is URL-safe and descriptive
- [ ] No data was invented -- only what the envelope output contains
- [ ] Frontmatter values are strings, arrays, or numbers -- no nested objects

---

## Important Notes

- This skill does NOT do analysis -- it only formats and saves
- It should be called by other skills at the end of their workflow
- It can also be called directly with a PipelineEnvelope payload
- Always use wikilinks `[[]]` for cross-references, not markdown links
- Keep frontmatter values as strings, arrays, or numbers -- no nested objects
- The vault base path is `${VAULT}/Admin/Product-Discovery/`
- Dataview, kanban, and tasks plugins are available in the vault
