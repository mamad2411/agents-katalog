---
name: generate-brief
description: Use when workspace material must become a document someone else reads — drafts in markdown from the analyses, sources, and register already on disk, then typesets it, keeping the source file beside the output so it can be re-rendered. Triggers - "write the brief", "generate a case memo", "produce the investigation report".
allowed-tools: Bash(typst *), Bash(command *), Bash(mkdir *), Bash(date *), Bash(find *), Read, Write
---

# Generate Brief

Turn workspace material into a document someone else reads, and keep the source beside
the output so it can be re-rendered rather than retyped.

## When to use

- The analyses and findings are ready to become a memo, brief, or report.
- Producing something for an external reader.

## Inputs

- Topic or framing. Required.
- `--type <case-memo|legal-brief|evidence-report|osint-report|document-review>` —
  defaults from the workspace variant.
- `--confidential <none|internal|privileged|confidential>` — footer marker.
- `--out <path>` — defaults to `exports/<slug>-<date>.pdf`.

## Procedure

### 1. Pick the type

From the flag, or from the variant: `legal-research` gives a case memo, an investigation
gives an OSINT report, a document review gives a document review. A brief over an
evidence register gives an evidence report.

### 2. Gather from what exists

Read `context/`, `research/` or `analyses/`, `findings/`, `timeline/`, `entities/`, and
the evidence register if the companion evidence agent has created one. Anything asserted
in the output must trace to something on disk. If a section has no material behind it,
leave the section out rather than filling it.

### 3. Draft in markdown first

Structure, adapted per type:

1. Header — matter, jurisdiction if relevant, date, author, confidentiality.
2. Summary — what the reader needs if they read nothing else.
3. Background — the facts, cited to their source.
4. Analysis — the reasoning, with each step tied to the material it rests on.
5. Exhibits or sources — a table, with identifiers and hashes where the evidence
   register supplies them.
6. Conclusions — and what would change them.
7. Citations to verify — everything still marked `[verify]`, gathered in one place.
8. Disclaimer, unless the workspace explicitly suppresses it.

Section 7 is not optional and is never quietly dropped. A brief that has no unverified
citations says so; it does not omit the heading.

### 4. Typeset

```bash
typst compile "$OUT.typ" "$OUT.pdf"
```

Use a workspace template under `context/typst/` if one exists. Otherwise a plain layout
with page numbers and the confidentiality marker in the footer. Keep the `.typ` file
beside the PDF — the source is the reproducible artifact; the PDF is a rendering of it.

If `typst` is unavailable, write the markdown and say the PDF was not produced. Do not
substitute a different renderer without saying so.

### 5. Index it

Append a line to `exports/index.md` with the date, type, output path, and topic, so the
history of what was produced is on the record.

## Output

- A PDF and its `.typ` source under `exports/`.
- An updated export index.

## Notes

- Never invent a citation to complete a sentence. Mark it `[verify]` and let it appear in
  section 7.
- The confidentiality marker goes in the footer of every page, not only the first.
- Regenerate rather than edit the PDF. An edited PDF no longer matches its source.
