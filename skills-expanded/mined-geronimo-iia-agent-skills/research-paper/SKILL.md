---
name: research-paper
description: >-
  Process an academic paper (PDF or URL) into the agent-knowledge repository.
  Extracts text, produces a confidence-annotated structured analysis, and integrates
  findings into the appropriate topic. Use when asked to read, analyse, or integrate
  a research paper into the knowledge base. Do NOT use for general web pages or blog
  posts. For multi-source deep extraction, use research-extraction instead.
metadata:
  version: "0.5.0"
---

# Research Paper Processing

Processes an academic paper into the knowledge repository following the
`sources → extract → analysis → studies → synthesis` pipeline.
Produces confidence-annotated claims traceable to exact source sections.

Apply `kb-conventions` skill for annotation markers, KB directory layout,
frontmatter schema, and synthesis impact rules.

## Prerequisites

Add to `.claude/settings.json` before running:

```json
{
  "permissions": {
    "allow": [
      "Bash(xberg *)",
      "Bash(uvx marker-pdf *)",
      "Bash(curl *)",
      "Bash(mkdir *)",
      "Bash(cp *)"
    ]
  }
}
```

## When to use

- Single paper (PDF or URL) to integrate into a topic KB
- Need structured analysis with traceable claims
- Want synthesis impact assessment against existing KB

For multiple sources requiring multi-axis extraction, use `research-extraction` instead.

## Step 1 — Identify paper and topic

Ask the user (or infer from context):
- Paper source: URL or local PDF path
- Target topic directory within the knowledge base
- Create the topic directory if it does not exist (see `kb-conventions` for layout)

## Step 2 — Acquire the source

### URL

```bash
mkdir -p "<topic>/sources/<slug>"
curl -L "<url>" -o "<topic>/sources/<slug>/original.pdf"
```

Skip if file already exists.

### Local PDF

Copy to `<topic>/sources/<slug>/original.pdf` if not already there.

### Create source.md

Create `<topic>/sources/<slug>/source.md` using the template from `kb-conventions`.
Fill `title`, `type`, `summary`, `tags`, `status: draft`, `last_updated` from what is already known (title page, URL, user context).
Leave `tldr`, `claims`, `concepts` empty — populated after Step 4.

## Step 3 — Extract text

Use the `pdf-parse` skill to extract text. It selects the right tool automatically
(xberg for machine-readable, marker-pdf via uvx for scanned) and handles tool installation.

For academic papers, pass `--use_llm --force_ocr` to the `pdf-parse` skill for best quality on scanned sources.

Output goes to `<topic>/sources/<slug>/extracted.md`.

## Step 4 — Produce a structured analysis

Read `<topic>/sources/<slug>/extracted.md` and any existing KB documents in
`<topic>/synthesis/` and `<topic>/analysis/`. Write the analysis to
`<topic>/analysis/<slug>.md` using the frontmatter schema from `kb-conventions`.

### Required sections

1. **Publication details** — title, authors, year, venue, DOI
2. **Core thesis** — main research question and central claim in 2–3 sentences `[DIRECT]`
3. **Key contributions** — bullet list, each with `[DIRECT]`, `[INFERRED]`, or `[SPECULATIVE]` citation
4. **Mathematical foundations** — equations, proofs, formal definitions (if present)
5. **Algorithms** — pseudocode or step-by-step for all algorithms, each with section reference
6. **Architecture / system design** — component relationships, diagrams described in prose
7. **Experimental results** — datasets, metrics, key findings with `[DIRECT]` citations
8. **Limitations and open problems** — what the paper acknowledges as unsolved
9. **Relation to existing KB** — cross-reference with `<topic>/analysis/` and `<topic>/synthesis/`; use blockquote markers `> ⚠ DIVERGES FROM KB:` or `> ✦ NEW:` where relevant
10. **Glossary** — domain-specific terms introduced, each with `[DIRECT]` definition

## Step 4b — Apply anti-slop

Apply the `anti-slop` skill to `<topic>/analysis/<slug>.md` before proceeding.
Do NOT modify citation markers, confidence annotations, blockquotes, or code blocks — prose quality only.

## Step 4c — Update source.md

After completing the analysis, update `<topic>/sources/<slug>/source.md`:

- `tldr`: one-sentence key takeaway derived from the Core thesis section
- `status`: `active` (was `draft`)
- `concepts`: slugs of any `<topic>/synthesis/` pages this source informs
- `sources`: slugs of cited papers if this is a survey
- `confidence`: 0.8–1.0 if claims are verified `[DIRECT]`; 0.5–0.7 if mostly `[INFERRED]`; 0.1–0.4 if mostly `[SPECULATIVE]`
- `claims`: add 3–7 key claims from the analysis using the claim schema in `kb-conventions`

## Step 5 — Update analysis index

See `kb-conventions` for index format. Add entry to `<topic>/analysis/README.md`;
create it if absent.

## Step 6 — Assess synthesis impact

See `kb-conventions` for synthesis impact rules and divergence markers.

## Output summary

```
✓ Source:    <topic>/sources/<slug>/original.pdf
✓ Extract:   <topic>/sources/<slug>/extracted.md
✓ Metadata:  <topic>/sources/<slug>/source.md
✓ Analysis:  <topic>/analysis/<slug>.md
✓ Index:     <topic>/analysis/README.md
~ Synthesis: <NEW / DIVERGES / no impact>
```
