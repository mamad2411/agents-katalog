---
name: project-indexer
description: Run once on any new construction project to build the full 3-layer context system. Creates the 0.ai-context folder with Claude.md, project.md, drawings.md, and memory.md files. Processes all construction documents into lightweight text indexes. Pulls business context rules from Notion or connected data source. After this runs, every Co-work chat for this project uses 20-40x fewer tokens and gets consistent, accurate answers. Trigger on phrases like "run project indexer", "set up this project", "index my project", "set up co-work for this project", or any request to initialise a new construction project in Co-work.
---

# Project Indexer Skill

Runs once when you start a new construction project in Co-work. Builds the full context system so every future chat is faster, cheaper, and more accurate.

## What this skill produces

```
project-folder/
└── 0.ai-context/
    ├── claude.md        # Rules and architecture for every chat in this project
    ├── project.md       # Full project snapshot: contract, parties, key dates, payment terms
    ├── drawings.md      # Master drawing register with cross-references
    ├── memory.md        # Running project memory (updated after each chat)
    └── processed/
        ├── SHEET-001.txt   # Text extraction from each drawing
        ├── SHEET-001.png   # Rendered image of each sheet
        └── ...
```

---

## Phase 1: Connect and read business context

Before processing any project documents, pull the business context from the connected data source.

**Check which connector is available:**
- Notion MCP → read the business context database
- Google Drive → read the business context folder
- GitHub repository → read the CONTEXT.md file

**Pull these specific items from business context:**
1. Company background (who you are, types of work, typical clients)
2. Standard contract positions (DLP period, payment terms, clauses you accept/reject)
3. Estimating principles and production rate library
4. Standard markup and margin ranges
5. Writing standards and voice rules (especially: be concise, no waffle)
6. Decision rules (when to proceed vs when to ask for approval)

If business context is not connected, ask the user:
"I cannot find your business context. Please either connect Notion/Google Drive or paste your key business rules so I can include them in this project setup."

---

## Phase 2: Scan and classify all project documents

Scan everything in the project folder. Do not process yet — just build a complete inventory.

For each file found, record:
- File name and path
- File type (PDF, Excel, Word, CSV, image)
- Apparent document type (see `references/document-types.md`)

Document types to classify:
- Construction drawings (PDF)
- Contract / subcontract
- Specification
- Programme / Gantt chart
- Bill of Quantities / Schedule of Rates
- Subcontractor correspondence
- RFI register
- Variation register
- Meeting minutes
- Scope of works
- Insurance / bonds documentation
- Other

Output: internal inventory list. Do not show to user yet.

---

## Phase 3: Process construction drawings

Run the drawing processing script on all PDFs classified as construction drawings.

```
scripts/process_drawings.py
```

For each drawing sheet:
1. Split merged PDF into individual sheet files
2. Extract text/vector layer → save as `.txt`
3. Render as image → save as `.png`
4. Classify sheet type using `references/drawing-types.md`
5. Extract symbol legends and abbreviations
6. Map cross-references to other sheets

**Important:** Use Claude vision to classify drawing types. Do not use pattern-matching scripts for classification — construction drawing formats vary too much.

Output: all processed sheets saved to `0.ai-context/processed/`

---

## Phase 4: Build drawings.md

Read all processed drawing sheets and build the master drawing register.

Output file: `0.ai-context/drawings.md`

Include:
1. **Project drawing summary** — total sheets, drawing disciplines present, drawing set date
2. **Sheet register** — one row per sheet: sheet number, title, type, scale, key elements, cross-references
3. **Symbol library** — all symbols, line types, and abbreviations extracted from legends
4. **Cross-reference matrix** — which drawings reference which other drawings and why
5. **Query instructions** — brief note on how to use this file when answering drawing questions

Target size: under 15KB. This is loaded on every drawing-related query.

---

## Phase 5: Process contract and key documents

For each non-drawing document, extract structured information.

**Contract / subcontract:** Extract:
- Contracting parties and ABN/company numbers
- Contract sum and basis (lump sum / schedule of rates / cost plus)
- Programme: commencement date, practical completion date, milestones
- Payment terms: claim dates, payment period, retention rate and cap
- Defects liability period
- Liquidated damages rate
- Key insurance requirements
- Key special conditions or non-standard clauses
- Any pay-when-paid provisions (flag immediately)

**Specification:** Extract:
- Project description and scope summary
- Quality standards referenced
- Testing and inspection requirements
- Hold points
- Substitution rules

**Programme / Gantt:** Extract:
- Critical path summary
- Key milestones
- Float on critical activities (if shown)
- Any external dependencies

**BOQ / Schedule of Rates:** Extract:
- Trade sections and their total values
- Any PC sums or provisional quantities
- Items where quantities are to be provided by tenderer

---

## Phase 6: Build project.md

Output file: `0.ai-context/project.md`

Structure:

```
# Project Snapshot

## Project overview
[Name, address, client, type of work, contract type]

## Key parties
[Client, head contractor, consultants, key subcontractors]

## Contract summary
[Sum, basis, key dates, payment terms, LD rate, DLP, retention]

## Programme summary
[Start, finish, key milestones]

## Scope summary
[2-3 paragraphs on what the project involves]

## Key risks and flags
[Any non-standard clauses, pay-when-paid provisions, unusual requirements]

## Document inventory
[List of all project documents with file paths]

## Last updated
[Date this file was generated]
```

---

## Phase 7: Build claude.md

This is the most important file. Claude reads it at the start of every chat in this project.

Output file: `0.ai-context/claude.md`

Pull the template from `templates/claude-md-template.md` and populate it with:
- Project name and type
- Where each type of information lives (drawings → drawings.md, contract → project.md, rates → Notion/business context)
- Business context rules pulled in Phase 1 (writing standards, decision rules, contract positions)
- Project-specific operating rules

The claude.md file tells Claude:
1. What this project is
2. Where to find any type of information it might need
3. How to behave (concise, ask before deleting, check before big decisions)
4. What business rules to apply (standard contract positions, markup ranges, etc.)

---

## Phase 8: Create memory.md

Output file: `0.ai-context/memory.md`

Initial structure:

```
# Project Memory

## Purpose
This file is updated at the end of each Co-work chat session.
It captures key decisions, open items, and context that should carry
forward into future chats.

## Project decisions log
[Empty — populated as project progresses]

## Open items
[Empty — populated as project progresses]

## Key contacts and context
[Empty — populated as project progresses]

## Session history
[Empty — populated as chats are completed]
```

Instruct the user: at the end of each chat session, run:
"Update memory.md with any key decisions or open items from this chat."

---

## Phase 9: Completion report

Report to user:

```
Project indexer complete.

Files created:
  0.ai-context/claude.md       [X KB] — reads on every chat
  0.ai-context/project.md      [X KB] — full project snapshot
  0.ai-context/drawings.md     [X KB] — drawing register and symbol library
  0.ai-context/memory.md       [X KB] — running project memory

Drawings processed: X sheets
  CAD-exported (text layer): X
  Scanned (image only): X

Documents processed: X files
  Contract: [found / not found]
  Specification: [found / not found]
  Programme: [found / not found]
  BOQ: [found / not found]

Business context: [pulled from Notion / Google Drive / GitHub / not found]

Flags for your attention:
  [Any pay-when-paid clauses found]
  [Any scanned drawings flagged as low-accuracy]
  [Any documents that could not be processed]

Estimated token saving vs raw PDF querying: 20-40x per query.

To start working on this project, go to the Co-work Projects tab,
select this project folder, and start a new chat.
Good prompts to try:
  "Review the contract against my standard terms in Notion"
  "Prepare a conceptual estimate using my cost library in Notion"
  "What structural drawings do we have and what do they show?"
```

---

## How Co-work should use the indexes after setup

When answering any project question after the indexer has run:

1. **Read `0.ai-context/claude.md` first** — understand rules and where information lives
2. **Check `0.ai-context/project.md`** — for any contract, programme, or scope question
3. **Check `0.ai-context/drawings.md`** — for any drawing question, then target the specific processed sheet
4. **Check `0.ai-context/memory.md`** — for any context from previous chats
5. **Check business context in Notion/connected source** — for rates, contract positions, writing standards
6. **Only open raw PDF files if the processed indexes are insufficient**

### Prompting rules (include these in claude.md)

Good prompts always say where to find the information:
- "Review the contract **against my standard terms in Notion**"
- "Prepare a conceptual estimate **using my cost library in Notion**"
- "What is the LD rate? Check **project.md**"
- "What is shown on the structural drawings? Check **drawings.md**"

Bad prompts:
- "Review the contract" (Claude does not know which contract position to apply)
- "Prepare an estimate" (Claude does not know which rates to use)
- "Summarise the drawings" (Claude will process raw PDFs instead of using drawings.md)

---

## Reference files

- `references/document-types.md` — construction document types and what to extract from each
- `references/drawing-types.md` — construction drawing types and classification guide
- `templates/claude-md-template.md` — template for the claude.md file
- `templates/project-md-template.md` — template for the project.md file
