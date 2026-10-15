---
name: cc-canary-html
description: HTML-rendered version of /cc-canary — produces a long-form nerf-detection report as a standalone dark-theme HTML file and auto-opens it in the browser. Same analysis as /cc-canary (forensic markdown writeup), same narrative placeholders, but the output is a styled HTML page suitable for viewing, sharing, or printing. Writes `./cc-canary-<YYYY-MM-DD>.html` to the current directory.
argument-hint: "[window, default 60d]"
allowed-tools: Read Write Bash(python3 *) Bash(date *) Bash(ls *) Bash(open *) Bash(xdg-open *) Bash(start *) Bash(uname *)
model: sonnet
---

# cc-canary-html — HTML nerf-detection report

**Same analysis as `/cc-canary`, rendered as HTML.**

Bundled script `scripts/compute_stats.py` does the work in ~2.5s: scans
JSONLs, runs inflection + transition-day detection, builds pre/post
aggregates, cross-version comparison, hour-of-day, word frequency,
three-period thinking depth, visibility transition, per-turn rates, and
abnormalities — then renders a complete HTML skeleton with every table
filled and ASCII bar charts preserved in monospace `<pre>` blocks.
Narrative slots are marked `<!-- C: ... -->`.

Default window: `60d`. Accept `7d / 14d / 30d / 60d / 90d / 180d`.

## Your 4-step job

### 1. Run the script

```
Bash(python3 <SKILL_DIR>/scripts/compute_stats.py --window {window} --render-html /tmp/cc-canary-skeleton-{window}.html > /dev/null 2>&1)
```

`<SKILL_DIR>`: `.claude/skills/cc-canary-html/` → fallback to `~/.claude/skills/cc-canary-html/`.

Flags: `--window {Nd}` (required); `--include-agents`; `--min-user-words N`.

If the script fails: report error, retry once with `--include-agents`, else stop. Never fall back to hand-computation.

### 2. Read the HTML skeleton

```
Read /tmp/cc-canary-skeleton-{window}.html
```

### 3. Fill every `<!-- C: ... -->` placeholder and save

Replace each placeholder comment with HTML-safe narrative text. Escape
`<`, `>`, `&` in anything you write. Keep all tables, `<pre>` bar
charts, and existing HTML untouched. Save as:

```
Write ./cc-canary-{YYYY-MM-DD}.html
```

### 4. Open in the browser

Detect platform via `Bash(uname)`:

- `Darwin` → `Bash(open ./cc-canary-{YYYY-MM-DD}.html)`
- `Linux` → `Bash(xdg-open ./cc-canary-{YYYY-MM-DD}.html)`
- anything else → `Bash(start ./cc-canary-{YYYY-MM-DD}.html)`

If the open command fails, just print the absolute path — don't error.

End your message with: `Wrote /Users/.../cc-canary-{date}.html — opened in browser.` (or `… open manually.` if open failed).

## Narrative placeholders

Same set as `/cc-canary`:

- `verdict-line` — HOLDING / SUSPECTED REGRESSION / CONFIRMED REGRESSION / INCONCLUSIVE + brief justification
- `summary` — 1–2 sentences, terse: what moved and by how much
- `timeline` — 1–2 paragraphs
- `xv-para` — 1 paragraph on cross-version (if §2 is present)
- `finding-N-class` × up to 5 — inline classification: model-side | user-side | ambiguous
- `finding-N-reason` × up to 5 — 2–3 sentences max, evidence-first
- `root-cause` — 3–5 paragraphs
- `what-would-help` — 2–4 concrete bullets
- `appendix-a1…a4, b, c, d, e, f, g, h` — 1 paragraph each
- `meta-note` — 2–5 sentences, first person, honest

## Verdict calibration

- **HOLDING**: ≤1 model-side signal
- **SUSPECTED REGRESSION**: 2–3 model-side signals
- **CONFIRMED REGRESSION**: ≥3 model-side signals + non-empty cross-version showing decline + `session_count ≥ 15` + ≥2 models + `inflection.gap_sigma ≥ 1.0`
- **INCONCLUSIVE**: `session_count < 15` OR `inflection.method == "fallback_split_half"` with overlapping confounds

Cap at SUSPECTED when: only one model; <15 sessions; single-project with project starting mid-window; inflection coincides with a visible user-side event.

## Hard rules

- **Never** read, grep, or glob `~/.claude/projects/**/*.jsonl`. Never run `jq`/`awk`/`wc` on session files. Script owns all that.
- **Never** touch existing HTML, tables, or `<pre>` blocks — they came from real data.
- **HTML-escape** any narrative text you insert (`<`, `>`, `&` → entities).
- **Every** finding gets a classification label.
- **Hedge** when cross-version is empty or `session_count < 15`.
- **Do not** verdict CONFIRMED REGRESSION without the full checklist.
- **Do not** save the skeleton as-is — replace every `<!-- C: ... -->` first.

## Failure modes

- Script import error → check `python3 -V` ≥ 3.8; retry once with `--include-agents`; else stop.
- Skeleton < 5KB → likely no sessions in window.
- `inflection.method == fallback_split_half` → state it; cap at SUSPECTED.
- Cross-version Δ `None` → div-by-zero when model-A value is 0; note the confound.
- Browser-open command fails → don't error; print the path and move on.
