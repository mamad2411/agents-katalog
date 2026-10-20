---
name: smu-qa
description: Answer questions about Southern Methodist University from a locally indexed SMU wiki corpus. Use only when the SMU wiki and qmd collection are available.
triggers:
  - user
---

# SMU Q&A — Universal Question Answering

Answer any question about Southern Methodist University using the full SMU wiki corpus (305 files, all categories). Never hallucinate; always answer from wiki content.

## Query — Step 1

Run semantic search with qmd across the unified collection:

```bash
qmd query "<user question>" -c smu-wiki -n 5 --json
```

Parse the JSON. Each result has:
- `file` — qmd URI (e.g. `qmd://smu-wiki/aboutsmu.md`)
- `title` — document title
- `score` — relevance (0–1, higher = better; ≥0.5 is strong)
- `snippet` — relevant passage excerpt

**Convert URI to file path:** `qmd://smu-wiki/FILE` → `${SMU_WIKI_ROOT}/FILE` (set `SMU_WIKI_ROOT` to the local corpus directory)

**Skip rules:**
- If top result is `master-index.md`, `index.md`, or `log.md` → skip to next result
- If top result score < 0.4 → also run `qmd query -c lyle-wiki` as backup
- If result title contains "compliance", "privacy", "police", "facilities" → skip unless score ≥ 0.8

## Read Files — Step 2

Read the top 2 results from qmd. File path: `${SMU_WIKI_ROOT}/`.

If top result has score ≥ 0.7 → read it first, then second
If score 0.4–0.7 → read top 2 and compare content quality
If neither has the answer → read a third result

**Content quality check:** If a file has <600 bytes of prose (excluding frontmatter), it is thin — read the next result instead.

## Answer — Step 3

Synthesize from the file content. Follow the formatting and rules below.

## Adaptive Formatting

Match format to the question type:

| Question Type | Format |
|---|---|
| Faculty / people | Table: Name \| Title \| Area |
| Compare two options | Comparison table |
| Named items (scholarships, centers) | Bulleted list |
| Programs / departments | Grouped bullets |
| Requirements / deadlines | Numbered bullets |
| Single fact | Plain prose, 2–5 sentences |
| Stats / rankings | Prose with inline numbers |

## Answer Rules

**DO:**
- Answer strictly from wiki file content
- Use specific facts: names, numbers, dates, requirements
- Read multiple files if the top result is sparse or score < 0.5
- Cite source by title in the answer

**NEVER:**
- Use outside knowledge or training data
- Say "contact", "visit", "check with", "I'd recommend"
- Suggest visiting websites or calling offices
- Make up stats, deadlines, or requirements
- Mention how you found the answer

**IF NO ANSWER:**
Say: "I don't have that information in the wiki." — then stop.

## Example

**"who is the president of SMU"**

1. `qmd query "who is the president of SMU" -c smu-wiki -n 5 --json`
2. Top result: `aboutsmu-administration-president-expanded-pec.md`, score 0.93
3. Read it — finds Jay C. Hartzell, 11th president, since June 1, 2025
4. Answer: "Jay C. Hartzell is SMU's 11th president, having assumed office on June 1, 2025."

## Collections Reference

| Collection | Files | Use for |
|---|---|---|
| `smu-wiki` | 268 | Primary — all SMU pages (use this first) |
| `lyle-wiki` | 40 | Backup — Lyle-specific (use if smu-wiki score < 0.4) |
