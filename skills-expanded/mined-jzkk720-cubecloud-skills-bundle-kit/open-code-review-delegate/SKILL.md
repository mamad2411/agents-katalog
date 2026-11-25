---
name: open-code-review-delegate
description: >
  Delegation mode for open-code-review (OCR). Instead of OCR calling an LLM
  endpoint, this skill instructs the host agent to perform the code review
  itself, using OCR only for deterministic engineering: file selection and
  rule resolution. Use when the host agent should drive the review with its
  own LLM capabilities.
license: Apache-2.0
compatibility: >
  Requires the `ocr` CLI installed (via `npm install -g
  @alibaba-group/open-code-review` or GitHub release binary). Does NOT
  require a configured LLM endpoint — delegation mode is LLM-free on the
  OCR side.
metadata:
  author: alibaba
  homepage: https://github.com/alibaba/open-code-review
  version: "1.0.0"
---

# Open Code Review — Delegation Mode

A skill for performing AI code review where OCR provides deterministic engineering (file filtering, rule resolution) and the host agent performs the actual review using its own intelligence and tools.

## Prerequisites

- `ocr` CLI installed: `npm install -g @alibaba-group/open-code-review`
- No LLM configuration needed on the OCR side — the host agent drives the review

## Workflow

### Step 1: Preview — Determine What to Review

```bash
ocr delegate preview
```

This lists the files that would be reviewed along with stats (file count, changed lines) — no LLM calls, no cost. Useful for checking scope before a full review.

### Step 2: Get Rules for Files

```bash
ocr delegate rule <file1> <file2> ...
```

Returns the review rules that apply to each file. These are deterministic rule groups matched by file path patterns — use them as the review checklist.

### Step 3: Get Diffs

Use `git diff` or the appropriate git command to get the actual changes for each file identified in Step 1.

### Step 4: Review Each File

For each reviewable file:

1. Get its diff (Step 3)
2. Consult its Rule Group (from Step 2) for the review checklist
3. Conduct a thorough review, using appropriate context tools as needed

### Step 5: Format Output

Each comment must follow this structure:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| path | string | yes | Relative file path |
| content | string | yes | Review comment describing the issue |
| start_line | integer | no | Start line in the new file |
| end_line | integer | no | End line in the new file |
| category | enum | no | bug, security, performance, maintainability, test, style, documentation, other |
| severity | enum | no | critical, high, medium, low |

### Step 6: Classify and Report

Group comments by severity:

| Severity | Criteria |
|----------|----------|
| **High** | Bugs, security vulnerabilities, data loss risks, correctness issues |
| **Medium** | Performance problems, maintainability concerns, test gaps, unclear logic |
| **Low** | Style nits, minor naming suggestions, documentation improvements |

Nitpicks and likely false positives are silently dropped. Render a Markdown summary.

### Step 7: Fix (Optional)

If the user said "review **and** fix" (or similar), apply safe fixes to High/Medium items inline. Otherwise ask before touching the code.

## Sub-commands Reference

| Command | Purpose |
|---------|---------|
| `ocr delegate preview` | List files that would be reviewed (dry-run, no LLM) |
| `ocr delegate rule <files>` | Get review rules for specific files |

## Shared Flags

| Flag | Description |
|------|-------------|
| `--from <ref>` | Start of comparison range (default: main) |
| `--to <ref>` | End of comparison range (default: HEAD) |
| `--commit <sha>` | Review a single commit |
| `--repo <path>` | Path to Git repo (default: cwd) |

## Gotchas

- **Delegation mode is LLM-free on the OCR side** — the host agent does all the LLM work. No `ocr config` or API key needed.
- **Rule resolution is deterministic** — `ocr delegate rule` matches file paths against `.ocr-rules.yaml` patterns. If no rules file exists, it returns a default rule set.
- **Preview first** — always run `ocr delegate preview` before a full review to confirm scope and avoid wasted work.
