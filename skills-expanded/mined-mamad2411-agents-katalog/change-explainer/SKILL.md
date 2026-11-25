---
name: change-explainer
description: Explain what changed and why it matters for code, infra, AWS, Terraform, scripts, worker goals, task execution, and validation. Use when Amit asks "show change txt", "explain change", "what changed", "show me the change", "change explainer", "show change html", "html change explainer", "visual change", or "make change cockpit". Defaults to terminal TXT evidence; HTML only when requested.
---

# Change Explainer

Explain a task/repo change in a human-readable way.

Default mode is **terminal TXT**:

- print concise terminal-friendly output
- save the same output as evidence by default
- when color is available, recommend the `.ansi` artifact as the file Amit
  should `cat`
- use current git diff plus task/session evidence
- answer first: **why this change matters**

Use HTML only when Amit asks for browser/HTML/cockpit output.

## Modes

- TXT: default. Use `scripts/change_explainer.py txt`.
- TXT detail: only when Amit asks `show change txt detail` or `show change txt
  big`. Use `scripts/change_explainer.py txt --detail`.
- HTML: requested only. Use `scripts/change_explainer.py html`.
- Both: use `scripts/change_explainer.py both`.

## Required Shape

Default TXT/ANSI output should use 3-5 panels:

1. Why this change matters.
2. What changed: before/after plus the most relevant files.
3. Evidence and validation.
4. Risk/gate footer: rollback, blast radius, PROD boundary, secrets.

Detail/big output may add:

- causal spine: trigger -> change -> effect -> evidence -> gate
- fuller reach map
- code/repo delta table with repo path and action markers
- AWS/resource/evidence table with added, updated, deleted, verified, warning,
  and blocked markers
- goal execution
- task improvement
- longer validation ledger

For exact terminal patterns, read `references/txt-mode.md`.
For HTML cockpit expectations, read `references/html-mode.md`.

When a change explanation feeds an Ops deploy presentation, use the shared
`PROVEN`, `IMPLEMENTED`, `BLOCKED`, and `FUTURE` vocabulary from
`docs/OPS_DEPLOY_PRESENTATION_GUIDE.md`. A successful command or green diff is
validation evidence, but does not by itself prove runtime behavior.

## Scope Rules

Default scope:

- current git diff
- changed files
- evidence files from this task/session
- validation output
- AWS/infra evidence when present
- worker markers/result packets when present

Do not paste long raw diffs into chat. Save detail under `~/.AGENTS-temp/<repo>/`.

## Tool Policy

MVP must work with standard Python + git.

Renderer policy:

- Python `rich` is the default renderer for `.ansi` and readable terminal
  panels.
- Plain TXT remains the fallback evidence format.

Optional helpers when they add value:

- `difft` / difftastic for structural code-diff sidecars.
- `delta` for colored raw-diff sidecars.
- `glow` for viewing Markdown evidence if Markdown output is added later.
- `termaid` or `mermaid-ascii` for small terminal diagrams only when native
  Rich boxes are not enough.
- `bat` for syntax-highlighted snippets.
- `revdiff` or `hunk` only for optional human-in-the-loop review mode, not as
  the core explainer

No external tool is required for TXT output.

## Design Notes

Keep the core simple:

- Rich renderer is the default implementation.
- Plain TXT remains evidence-safe fallback.
- `.ansi` is the preferred terminal review artifact when available.
- `difftastic`, `delta`, `glow`, `termaid`, and `mermaid-ascii` may improve
  future views, but they should feed the explainer; they should not replace the
  saved explanation or appear as a noisy report section.
- Interactive tools such as `revdiff`, `hunk`, or `sigil` are useful for manual
  review loops, but are overkill for the default MVP.

## Output Contract

TXT evidence path default:

`~/.AGENTS-temp/<repo>/change-explainer/change-explainer-YYYYMMDD-HHMMSS.txt`

Colored ANSI path when Rich is available:

`~/.AGENTS-temp/<repo>/change-explainer/change-explainer-YYYYMMDD-HHMMSS.ansi`

The latest ANSI/TXT terminal artifact is also copied to:

`/tmp/change.ansi`

HTML path when requested:

- Publish to `/opt/crypto-web/demos/<slug>/index.html`.
- Return `http://home/demos/<slug>/`.
- Keep TXT/ANSI evidence under
  `~/.AGENTS-temp/<repo>/change-explainer/`.
- Validate the exact URL with `curl -fsSI` before reporting success.
- Keep historical pages in place; never use their paths for new output.

Return the TXT evidence path and HTML LAN URL when created.

For terminal review, prefer returning one primary file:

`recommended_cat=<path-to-.ansi>`

Fall back to `.txt` only when ANSI/color output is unavailable.

Do not render a final "Run / Mode / Saved file" panel inside the ANSI/TXT
report. Put those instructions in the Codex chat response instead.

## Publishing

- Use HTML only when requested; TXT/ANSI remains the default.
- Publish HTML through `scripts/change_explainer.py`.
- Keep TXT/ANSI evidence under `~/.AGENTS-temp/<repo>/change-explainer/`.
- Keep `/tmp/change.ansi` behavior unchanged for terminal review.
