---
name: webwright
description: Use when browsing, automating, testing, or extracting from live websites would benefit from Playwright-powered, resettable, evidence-rich execution. Supports lightweight Webwright browsing for noisy/flaky pages and promotion to durable rerunnable scripts with screenshots, logs, and structured results.
version: 1.1.0
author: Hermes Agent + Microsoft Webwright adaptation
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [webwright, playwright, browser, qa, automation, extraction, evidence]
    related_skills: [systematic-debugging, test-driven-development]
---

# Webwright for Hermes

## Overview

Webwright is the browser power mode for Hermes. It uses local Playwright scripts to browse, inspect, extract, verify, and — when justified — produce a durable rerunnable web tool. The browser process is disposable; the durable state is the workspace: plans, scratch scripts, final scripts, logs, screenshots, downloaded artifacts, and `result.json`.

Use Webwright in two modes:

1. **Lightweight browsing mode** — short scratch Playwright scripts used as a better browser for noisy, flaky, multi-step, or extraction-heavy pages.
2. **Durable script mode** — a final rerunnable `final_script.py` with `plan.md`, logs, screenshots, and structured output.

Do not treat Webwright as only an automation deliverable. The efficient operating model is: use the lightest browser layer that gives enough reliability, then promote when the path stabilizes or evidence/reuse demands it.

## When to Use

Use Webwright when:

- normal browser snapshots are noisy, slow, flaky, or missing key data;
- the task spans multiple interactions, result pages, filters, date ranges, or downloads;
- structured extraction is needed from anchors, tables, PDFs, reports, or page metadata;
- selectors, filters, dates, quantities, currencies, or sort controls must be verified exactly;
- the user asks to automate, test, craft, parameterize, make reusable, or audit a browser workflow;
- another agent or human must be able to review the evidence later;
- a recurring cron/pipeline could reuse the browser path.

Do **not** use Webwright for:

- a quick one-page lookup where `browser_navigate` + `browser_snapshot` is enough;
- fuzzy early exploration where the source/task shape is not known and no extraction is needed;
- login-gated or sensitive flows unless the user explicitly authorizes scope and credential handling;
- sites whose terms prohibit automation;
- destructive actions such as purchases, posts, messages, account changes, or trading without explicit human approval immediately before the side effect.

## Decision Ladder

| Level | Use when | Output | Promotion trigger |
|---|---|---|---|
| Native browser tools | One-off, visual, low-stakes lookup | Ephemeral browser state/snapshot | Page is noisy, flaky, multi-step, or extraction-heavy |
| Webwright lightweight browsing | Need a better browser but not a reusable tool yet | Scratch scripts, screenshots, anchor/text dumps | Source path stabilizes, task repeats, or audit-grade evidence is needed |
| Webwright durable script | Repeated, evidence-sensitive, or pipeline-worthy task | `plan.md`, `final_script.py`, logs, screenshots, `result.json` | Parameterize into CLI/cron if reused again |

Rule of thumb: **browse with Webwright when it makes the current task cleaner; promote to a final script when future reuse or auditability justifies the ceremony.**

## Initial Efficiency Lessons From Benchmarks

Initial local Hermes benchmarks on 2026-05-25 suggested substantial wall-clock speedups, but these are **directional results from one environment**, not universal performance guarantees. Treat the ratios as evidence that Webwright can be materially faster in the right task class, not as a claim that every task will see the same multiplier.

| Task | Regular browser path | Webwright path | Directional lesson |
|---|---:|---:|---|
| NVIDIA IR latest 10-Q PDF extraction | ~806s and still needed non-browser extraction | 7.50s clean final run; 9.11s repeat run | Very large speedup in this test, mainly because PDF download/parsing avoided the browser PDF-viewer limitation |
| Five AI articles from AP/CNBC/TechCrunch/The Verge/MIT TR | ~1791s with manual handling/recovery | 99.90s clean final run | Significant speedup in this test, but noisy media pages required source-specific filters/fallbacks |

Interpretation:

- Webwright is strongest when the answer crosses a browser boundary: PDFs, downloads, filings, reports, tables, or structured artifacts.
- Webwright can help on noisy media pages, but source-specific candidate filters and fallbacks matter.
- Initial authoring may consume model tokens; deterministic Playwright reruns consume effectively **0 LLM tokens** unless the agent inspects results.
- Reuse is where token ROI compounds: first pass builds the tool, future runs are local browser/script execution.

## Prerequisites

One-time runtime setup in the active Hermes environment:

```bash
python -c "import playwright; print('playwright ok')"
playwright install firefox
```

Firefox is the default engine because some protected sites reject Playwright Chromium. Use:

```python
browser = await p.firefox.launch(headless=True)
```

No separate Webwright LLM API key is required for this Hermes skill. Hermes writes, runs, and verifies the Playwright scripts with normal tools: `terminal`, `write_file`, `read_file`, `patch`, and `vision_analyze`.

## Workspace Contract

Use an isolated workspace for each task:

```text
.tmp/webwright/<slug>/
├── plan.md                         # required for durable mode
├── scratch/                        # lightweight exploration scripts/outputs
├── screenshots/                    # exploration screenshots
├── before_usage.json               # for benchmarks, if token accounting is requested
├── after_usage.json                # for benchmarks, if token accounting is requested
└── final_runs/
    └── run_1/
        ├── final_script.py
        ├── final_script_log.txt
        ├── result.json
        ├── downloaded_artifact.pdf
        └── screenshots/
            └── final_execution_<step>_<action>.png
```

Rules:

- Work inside the selected workspace; do not scatter scratch files across the repo.
- Use `viewport={"width": 1280, "height": 1800}`.
- Prefer Firefox unless the target requires another engine.
- Do not use `page.screenshot(full_page=True)` for proof screenshots; capture the visible state actually verified.
- For final runs, each clean execution gets a fresh `final_runs/run_<id>/` folder.
- If a run fails after producing partial artifacts, patch into a new run folder or clearly reset the folder before rerun.

## Workflow

### 1. Lightweight Webwright Browsing

Use this as a better browser before committing to a final reusable script.

Scratch script should usually:

- launch a clean Playwright context;
- visit the target page;
- print URL and title;
- dump visible text, ARIA snapshot, or anchors;
- save one or more screenshots;
- collect candidate links/data into JSON when useful;
- close the browser cleanly.

Minimal pattern:

```python
import asyncio, json
from pathlib import Path
from playwright.async_api import async_playwright

WORKSPACE = Path('.tmp/webwright/example')
SCRATCH = WORKSPACE / 'scratch'
SCREENSHOTS = WORKSPACE / 'screenshots'
SCRATCH.mkdir(parents=True, exist_ok=True)
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 1800})
        page = await context.new_page()
        await page.goto('https://example.com', wait_until='domcontentloaded')
        await page.screenshot(path=str(SCREENSHOTS / 'explore_1_start.png'))
        anchors = await page.locator('a').evaluate_all("""
            els => els.slice(0, 200).map(a => ({
                text: (a.innerText || '').trim(),
                href: a.href
            }))
        """)
        print('URL:', page.url)
        print('TITLE:', await page.title())
        print(json.dumps(anchors[:30], indent=2))
        await browser.close()

asyncio.run(main())
```

Promote from lightweight browsing to durable script only when the source path is stable, the task repeats, the answer needs audit-grade proof, or the browser work should become a reusable mini-tool.

### 2. Plan Durable Mode

Write `plan.md` before final automation. Include the original task and critical points (CPs):

```markdown
# Task
<verbatim user task>

# Critical Points
- [ ] CP1: <exact source, filter, sort, selection, or required datum>
- [ ] CP2: <another independently verifiable requirement>
```

Every explicit constraint becomes a CP. Numeric, date, quantity, currency, and unit constraints must be exact. Ranking words like “cheapest”, “highest rated”, “latest”, or “most reviewed” must be grounded in site controls or an explicit extraction/sort method, not a casual model judgment.

### 3. Author `final_script.py`

The final script must run from scratch without hidden browser state. Include:

- `RUN_DIR = Path(__file__).parent`
- `SCREENSHOTS = RUN_DIR / 'screenshots'`
- `LOG = RUN_DIR / 'final_script_log.txt'`
- `RESULT = RUN_DIR / 'result.json'`
- a `log(step, msg)` helper that resets/appends to `final_script_log.txt`;
- screenshots for each CP using `final_execution_<step>_<action>.png`;
- explicit waits and assertions for expected state;
- structured `result.json`;
- `FINAL_RESPONSE:` in the log if the user asked for a final datum.

Prefer accessible selectors (`get_by_role`, `get_by_label`, `get_by_text`, `locator('[aria-label=...]')`). Avoid brittle generated CSS class names unless no stable alternative exists.

### 4. Execute, Iterate, and Self-Verify

Run the final script. If it fails, diagnose the concrete failure, patch, and rerun in a clean final run folder.

For each CP, cite evidence from current-run logs, screenshots, or artifacts. Use `vision_analyze` when visual proof matters. Do not mark a CP complete from memory, old screenshots, or hidden UI state.

### 5. Report

Return:

- final answer/datum, if requested;
- workspace path;
- final run path;
- key script path;
- `result.json` path;
- evidence screenshots/log lines per CP;
- blockers or limitations;
- token/time accounting if this is a benchmark.

Include `MEDIA:/absolute/path/to/screenshot.png` for important screenshots when reporting in Discord.

## Source-Specific Patterns

### Financial IR / SEC / PDF Reports

Use Webwright strongly here. Recommended pattern:

1. Use Playwright/browser to prove official source provenance and extract the report link.
2. Download the linked PDF/report into the run folder.
3. Run `pdfinfo` first; parse `Subject`, `Title`, page count, and creation metadata.
4. Run `pdftotext -f 1 -l 2` for cover-page title, period, registrant, and date checks.
5. Cross-check date labels: `filed on`, `period ending`, `shares outstanding as of`, press-release date, and report date are different facts.
6. Save downloaded artifact, extracted text, and metadata alongside `result.json`.

Avoid relying on browser PDF viewer DOM text. In the NVIDIA benchmark, the PDF viewer exposed almost no useful document text to snapshots, while local artifact parsing succeeded.

### Multi-Source News / Article Harvests

Use lightweight Webwright browsing first, then durable mode once source specs are stable.

Start with an explicit source spec:

| Field | Meaning |
|---|---|
| `source` | Human-readable source name |
| `start_url` | Search/topic/source URL |
| `allowed_hosts` | Hosts that can produce valid results |
| `article_url_pattern` | Regex or predicate for valid article URLs |
| `topic_regex` | Topic text matcher |
| `text_excludes` | Reject visible text/title patterns only |
| `url_excludes` | Reject URL/path patterns only |
| `fallback_url` | Backup route if primary page fails |

Keep `top_candidates` in `result.json` so wrong selections are auditable. Candidate scoring is safer than first-match extraction.

## Common Pitfalls

1. **Overbuilding too early.** Do not create a full final script for a trivial one-page answer. Use native browser or lightweight Webwright first.

2. **Underusing Webwright as a browser.** If browser snapshots are noisy or flaky, use scratch Playwright browsing instead of repeatedly clicking through an unstable session.

3. **Mixing text and URL filters.** Applying publisher-name exclusions to `text + href` can reject every valid same-domain link. Keep `text_excludes` and `url_excludes` separate.

4. **Broad regexes.** Raw `AI` can match unintended substrings such as `details`. Prefer `\bAI\b` plus explicit topic terms like `OpenAI`, `Anthropic`, `Google`, `Nvidia`, `chatbot`, `LLM`, and `artificial intelligence`.

5. **Trusting first-page dates.** In filings, a visible date may be a shares-outstanding date, not the filing date. Parse metadata and label-specific text.

6. **Assuming PDF viewer text is extractable.** Browser PDF viewers often hide document text from DOM/accessibility snapshots. Download and parse artifacts locally.

7. **Assuming query strings prove filters.** If the site has explicit filter/apply controls, use and screenshot those controls or visible filter chips.

8. **Losing auditability.** Always save selected result plus candidate evidence. `result.json` should explain enough that a reviewer can spot bad selection logic.

9. **Credential leakage.** Never put secrets in scripts, logs, screenshots, or `plan.md`. For authenticated flows, use scoped environment variables and redact outputs.

10. **Benchmarking without token deltas.** Record before/after Hermes session usage for benchmarks. Distinguish deterministic script execution tokens (`0` LLM tokens) from agent authoring/review tokens.

## CLI Tool Mode

If the user asks to craft, parameterize, make reusable, or turn the flow into a CLI, produce a parameterized script instead of a one-shot script.

Additional requirements:

- Add a `# Parameters` table to `plan.md` with name, type, source phrase, default, and allowed/format.
- Put the browser flow inside one reusable function with a Google-style `Args:` docstring.
- Add `argparse` under `if __name__ == '__main__':`.
- Running `python final_script.py` with no arguments must reproduce the original task.
- First log line must be `step 0 params: name=value ...`.
- Verify import safety: importing the module must not launch a browser, write files, or hit the network.

Import-safety check:

```bash
python - <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location('fs', 'final_runs/run_1/final_script.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print([n for n in dir(mod) if not n.startswith('_')])
PY
```

## Benchmark / Token Accounting

For benchmark tasks, capture usage before and after the phase when possible. Hermes records session totals in `~/.hermes/profiles/<profile>/state.db`.

Report at least:

- wall-clock time;
- script runtime;
- final run success/failure;
- number of script iterations;
- agent session input/output/cache-read/reasoning tokens if available;
- whether the script itself calls an LLM API.

Remember: a deterministic Playwright script that does not call an LLM API has **0 script-execution LLM tokens**. The token cost is in authoring, inspection, and verification.

## Verification Checklist

- [ ] Frontmatter and structure follow official Hermes skill conventions.
- [ ] Playwright imports successfully and Firefox is installed in the active environment.
- [ ] Workspace is isolated under `.tmp/webwright/<slug>/` or another declared folder.
- [ ] Lightweight exploration saved URL/title/anchors/text and screenshots when used.
- [ ] Durable mode has `plan.md` with task and CP checklist.
- [ ] `final_runs/run_<id>/final_script.py` exists and runs cleanly from scratch.
- [ ] `final_script_log.txt` contains all constraint-relevant steps and final datum if applicable.
- [ ] `result.json` contains selected outputs and candidate/audit data where relevant.
- [ ] Each CP is checked off only after current-run evidence is cited.
- [ ] Key screenshots were inspected with `vision_analyze` when visual state mattered.
- [ ] Downloaded PDFs/reports are parsed locally, not only through browser snapshots.
- [ ] Benchmarks include time and token accounting when available.

## References

- Upstream repository: https://github.com/microsoft/Webwright
- Upstream architecture: code-as-action Playwright browser agent; local workspace is state; screenshots/logs are first-class artifacts.
- `references/hermes-adaptation-smoke-2026-05-25.md` — Hermes-native adaptation notes and smoke-test recipe.
- `references/benchmark-nvda-ir-2026-05-25.md` — NVIDIA IR quarterly-report benchmark; PDF viewer limitation and `pdfinfo` / `pdftotext` pattern.
- `references/benchmark-ai-articles-2026-05-25.md` — multi-source AI article benchmark; candidate filtering and source fallback lessons.
- `references/playwright-patterns.md` — reusable Playwright snippets.
- `references/verification-template.md` — evidence report template.
- `references/cli-tool-mode.md` — parameterized CLI script pattern.
