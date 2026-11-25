---
name: web-html-page
description: fast low-token static html reports for codex tasks. use when the user says show html, web report, publish report, what changed, summarize task, show me in browser, agent-web-reporting, or asks for a quick operational summary after a worker run. generate small self-contained offline html under /opt/crypto-web/fast with evidence in ~/.AGENTS-temp. do not create deep dashboards or rich diagrams.
---

# Web HTML Page

Create small, fast, local HTML reports for operational review after Codex work.

Before creating HTML, follow `DESIGN.md` exactly. The required design is
Midnight Compact: dark-only, compact, operational, and never a white/day theme.

## Use this skill for

- Quick task summaries, worker results, lane status, diffs, reviews, and run evidence.
- Prompts containing: `show html`, `web report`, `publish report`, `what changed`, `summarize task`, `show me in browser`.
- Legacy prompts or docs that say `agent-web-reporting`; this skill is the replacement for quick reports.
- Cases where terminal text is hard to scan but a full dashboard would be wasteful.

## Do not use this skill for

- Rich architecture diagrams or visual teaching. Use `visual-explainer`.
- Durable learning dashboards, research, study mode, or DD. Use `deep-work`.
- An Ops deploy presentation with architecture and workflow teaching. Use
  `visual-explainer`; this skill may provide its compact status or evidence
  appendix.

## Output contract

- Publish to `/opt/crypto-web/fast/<slug>/index.html`.
- Return `http://home/fast/<slug>/`.
- Store source and evidence under
  `~/.AGENTS-temp/<project-or-repo>/<current-lane>/web-html-page/`.
- Validate the exact URL with `curl -fsSI` before reporting success.
- Default lifecycle: archive or delete after 7 days unless marked `keep`.
- Keep historical pages in place; never use their paths for new output.
- Use a lowercase path-safe slug without `.html`.

Recommended publish command after rendering `output.html`:

```bash
python3 scripts/publish_html.py output.html \
  --skill web-html-page \
  --project <repo> \
  --slug <slug>
```

## Report shape

Use a compact static page:

1. Title, timestamp, repo/lane, status badge.
2. TL;DR box with 3-6 bullets.
3. What changed.
4. Evidence and checks.
5. Risks or blockers.
6. Next action.

Keep it small. Prefer summary boxes, simple tables, short timelines, and status badges. Use inline SVG only when it improves scan speed.

When the report summarizes a deploy or validation run, include available build
ID, evidence as-of date, source revision, and QA status. Do not invent missing
metadata.

## Safety rules

- Never include secrets, tokens, private keys, session cookies, or credential-like values.
- Sanitize AWS account-sensitive values unless the user explicitly asks to keep them.
- Never invent real AWS IDs. If unknown, write `unknown / needs refresh`.
- No CDN, external JS, remote fonts, or external images.
- HTML must be self-contained and safe for local LAN viewing.

## JSON-spec render path

Prefer deterministic JSON-spec rendering before writing direct HTML.

Use this flow for repeatable reports:

1. Create `report.spec.json` using `references/json-spec-contract.md`.
2. Use only components in `references/component-catalog.json`.
3. Run `scripts/validate_spec.py report.spec.json`.
4. Run `scripts/render_html_from_spec.py report.spec.json output.html`.
5. Run `scripts/validate_html.py output.html`.
6. Publish with `scripts/publish_html.py` only when LAN publishing is requested.

The AI chooses report content, component types, props, and child order. The
renderer owns HTML, CSS, layout, spacing, cards, badges, print CSS, and
escaping.

Direct handwritten HTML is fallback only when the catalog cannot express the
requested page. Fallback HTML must still follow `DESIGN.md` and pass
`validate_html.py`.

## Helper scripts

- Use `scripts/publish_html.py` to copy output into `/opt/crypto-web/fast`,
  write evidence, reject remote assets, back up overwritten output, and print
  the canonical LAN URL.
- Use `scripts/validate_html.py` before publishing when the page contains copied logs or resource identifiers.
- Use `scripts/archive_old_reports.py` for the 7-day lifecycle policy.

See `references/template-guidance.md` and `assets/report-template.html` only when a template is needed.
