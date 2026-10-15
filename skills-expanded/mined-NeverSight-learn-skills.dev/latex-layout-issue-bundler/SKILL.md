---
name: latex-layout-issue-bundler
description: Create repo-local LaTeX layout issue bundles from a PDF page, crop, source snippet, and compile log. Use when the user wants to avoid manual PDF screenshots, capture page-specific layout problems, or hand Codex/Claude Code a reproducible paper layout debugging artifact.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# LaTeX Layout Issue Bundler

Create a reproducible layout issue bundle instead of relying on one-off manual screenshots.

Use this skill when:

- the user has a rendered PDF page with a layout problem
- a screenshot would normally be sent to the agent
- the issue is page/object specific: float gaps, awkward page breaks, algorithm/table/figure placement, overfull/underfull lines, short lines, or local spacing
- the agent needs enough artifact context to debug layout without seeing the full conversation

This skill produces evidence for another skill to consume; it does not directly fix the paper.

## Output Shape

Bundles live under the paper repo:

```text
.agent/layout-issues/<issue-id>/
├── prompt.md
├── manifest.json
├── page-<NN>.png                  # when a PDF renderer is available
├── crop.png                       # when rendering and crop tools are available
├── page-<NN>.txt                  # when pdftotext is available
├── source-snippet.tex             # when a source file and line range are provided
└── compile-log-excerpt.txt        # when a log path is provided or detected
```

These are agent-private artifacts by default. Do not commit them to author-visible, anonymous-submission, arXiv, camera-ready, or publisher-visible paper source unless the user explicitly wants a sanitized debug artifact published.

## Quick Command

Resolve the installed skill directory, then run:

```bash
python3 <latex-layout-issue-bundler-skill-dir>/scripts/create_layout_issue_bundle.py \
  --paper-dir "$PAPER_DIR" \
  --pdf "$PAPER_DIR/main.pdf" \
  --page 7 \
  --title "Algorithm 2 bottom gap" \
  --problem "Large blank space after Algorithm 2 before the following paragraph." \
  --object "Algorithm 2 and lines 247-255" \
  --source "$PAPER_DIR/sections/method.tex:247-255" \
  --crop bottom
```

The script prints the bundle path.

## Inputs

- `--paper-dir`: paper repo root or paper worktree root.
- `--pdf`: rendered PDF path.
- `--page`: 1-indexed PDF page number.
- `--title`: short issue title used for the issue id when `--issue-id` is omitted.
- `--problem`: what looks wrong visually.
- `--object`: affected object or paragraph, such as `Algorithm 2`, `Table 1`, or `lines 247-255`.
- `--source`: optional `path:start-end` source pointer.
- `--crop`: optional crop preset or rectangle:
  - `top`, `bottom`, `left`, `right`, `center`
  - `x,y,w,h` in pixels
- `--log`: optional compile log path. If omitted, the script tries `<pdf-stem>.log`.

## Workflow

1. Identify the page and local object from the PDF viewer, Overleaf preview, Skim, or SyncTeX.
2. Run the bundler with the page, problem, object, optional source line range, and optional crop.
3. Inspect `.agent/layout-issues/<issue-id>/prompt.md`.
4. Give that bundle path to `submit-paper`, `paper-writing-assistant`, or a fresh reviewer/sidecar session.
5. The fixing agent should make one small local change, compile through the configured backend, and compare the same page again.

## Tool Behavior

The script uses tools only when available:

- `pdftoppm` renders a PDF page to PNG.
- `pdftotext` extracts page text.
- ImageMagick `magick` or `convert` crops the rendered PNG.

Missing tools are recorded in `manifest.json`; they are not treated as fatal if the bundle still has useful context.

Do not record local absolute tool paths or machine-specific TeX installation facts in the paper repo. Tool availability is runtime state.

## Fixing Policy For Consumers

When consuming a bundle, follow the `submit-paper` layout debugging policy:

- localize the page and object first
- prefer prose and local float/page-break fixes over global layout settings
- change one object at a time
- avoid broad `\sloppy`, `\emergencystretch`, global paragraph, or global float-spacing changes unless the whole paper has a documented style issue
- verify the same page visually after each change
