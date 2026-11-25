---
name: redact-content
description: Use when material must leave the workspace with names or identifiers protected — applies user-directed redaction using a stable alias mapping, per-document random replacement, or declared patterns, always writing new files and never touching the input. Triggers - "redact this before disclosure", "pseudonymise these documents", "strip names from this export".
allowed-tools: Bash(pdftotext *), Bash(qpdf *), Bash(exiftool *), Bash(mat2 *), Bash(command *), Bash(mkdir *), Bash(cp *), Bash(date *), Read, Write
---

# Redact Content

Produce copies with names and identifiers protected, under the user's direction, with
every replacement logged.

## When to use

- Preparing a disclosure set.
- Sharing material with someone who should not see identities.
- Publishing an example drawn from real material.

This is not an automatic detector. The user says what to protect.

## Inputs

- Path to a file or directory. Required.
- `--mode <alias|random|pattern>` — defaults to `alias`.
- `--mapping <path>` — alias map. Defaults to `aliases/active_mapping.json`.
- `--scrub-metadata` — also strip metadata from the outputs.
- `--out <dir>` — defaults to `output/`.

## Procedure

### 1. Understand what visual redaction means here

Say this before starting, every time, because the difference decides whether the output
is safe to release:

- Replacing text in a **text layer** changes what is extracted and searched. If the
  original text remains anywhere in the file — a second layer, an annotation, an
  embedded thumbnail, revision history — it is still recoverable.
- **True visual redaction** removes the underlying content, normally by rasterising the
  page or by using a tool built for the purpose.

This skill does the first. It does not guarantee the second. Where the stakes require
irreversible removal, say so and recommend rasterisation or a purpose-built tool.

### 2. Choose the mode deliberately

- **alias** — a stable mapping, so the same real name is always the same pseudonym
  across every document. Correct for a disclosure set that must stay internally
  consistent. It also means one leaked mapping unmasks everything.
- **random** — a fresh mapping per document, never reused. Correct when documents must
  not be linkable to each other. Cross-document consistency is lost by design.
- **pattern** — declared patterns for emails, phone numbers, and identifiers, replaced
  with labelled placeholders. Best-effort assistance, never a substitute for reading.

### 3. Confirm the mapping before writing

Show every real value and its replacement. Ask for the ones not yet mapped. Write
nothing until the mapping is agreed. Storing a mapping is what makes redaction auditable
and reversible by the holder — treat the mapping file as more sensitive than the
documents, and say so if the workspace has a remote.

### 4. Apply

Text and markdown: replace with word-boundary matching, and check for the value
appearing in a different case or with different spacing before declaring completeness.

PDFs: extract the text layer, apply replacements, and re-render. Report that the output
is a re-rendered document, not the original with boxes drawn on it.

Images: no visual redaction is attempted. A cropped or blurred image can often be
reversed, and shipping the original alongside a redacted copy defeats the exercise
entirely. Say what would need to happen instead.

### 5. Scrub metadata if asked

```bash
exiftool -all= "$OUTPUT"
mat2 --inplace "$OUTPUT"
```

Only ever on outputs. Never on an input, and never on anything under an originals
directory.

### 6. Log every run

Append to `logs/redaction-<timestamp>.jsonl`: input path, output path, mode, mapping
file, replacement count per value, and every warning raised.

### 7. Report what was not covered

State plainly what the redaction did not reach: images, scanned pages, embedded
attachments, metadata if not scrubbed. An honest gap list is the deliverable as much as
the files are.

## Output

- Redacted copies under the output directory.
- An updated mapping file and a JSON Lines log.
- A statement of what remains unredacted.

## Notes

- Inputs are never modified.
- In random mode, never reuse an identifier across documents — that reintroduces exactly
  the linkage the mode exists to prevent.
- Anything with legal consequence needs human review before release. Say it, do not
  assume it is understood.
