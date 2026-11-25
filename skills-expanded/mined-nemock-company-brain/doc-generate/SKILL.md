---
name: doc-generate
description: Generate planning documents from a company-brain vault. Ships 21 generators: full MRD (markdown / html / docx) and one-pager (markdown / html); plus 19 scaffolds for PID, project-charter, stakeholder-register, risk-register, status-report, meeting-minutes, lessons-learned, business-plan, sales-battle-card, competitive-brief, ifu-comparison, decision-log, press-release, investor-update, onboarding-doc, srd, srs, hrs, risk-brainstorm. Profile-aware — medical-device-only docs (risk-register, ifu-comparison, risk-brainstorm) reject non-medical-device vaults. All output is idempotent and lands under <vault>/exports/.
---

# doc-generate

This skill turns the typed vault into planning documents. The vault is the source of truth; the documents are derived artifacts you can regenerate any time and that get committed under `<vault>/exports/`.

You do not write document content by hand. The generators read the schema, pull the right typed nodes, and emit consistent, profile-aware output. Your job is to invoke the right `cb render` command and surface any issues to the user.

## Before any render

1. **Confirm the vault path.** Default: current working directory. Refuse politely if there is no `_system/PROFILE.md` — that's the marker of a vault.
2. **Run `cb validate --path <vault>` first.** A vault with errors will still render, but uncited claims and broken edges will surface in the output. If validate reports errors, tell the user and offer to fix them via `intake` or `atomize` before generating.
3. **Confirm the active profile.** Run `cb describe-profile --path <vault>` to know whether medical-device-only sections will appear. The profile decides which sections render.

## What ships today (21 generators)

### Full implementations (v0.3.0)

| Document | Markdown | HTML | DOCX | Profile |
|---|:-:|:-:|:-:|---|
| Marketing Requirements Document (MRD) | ✅ | ✅ | ✅ | all |
| One-pager | ✅ | ✅ | — | all |

### Scaffolds (v0.4.0)

Runnable templates that query the right typed nodes, fill in what they can, and flag the output as a scaffold in the footer. Adopters fill in the placeholders by hand. Full per-doc implementations land in v1.x.

| Document | CLI name | Profile | Length norm |
|---|---|---|---|
| PID (Project Initiation Document) | `pid` | all | 2–4 pages |
| Project charter | `project-charter` | all | 1 page |
| Stakeholder register | `stakeholder-register` | all | 1–2 pages (table) |
| Risk register (planning) | `risk-register` | **medical-device** | 1–3 pages |
| Status report | `status-report` | all | 1 page |
| Meeting minutes | `meeting-minutes` | all | 1 page (not 12) |
| Lessons learned / close-out | `lessons-learned` | all | 1–2 pages |
| Business plan | `business-plan` | all | 8–15 pages |
| Sales battle card (per competitor) | `sales-battle-card` | all | 1–2 pages |
| Competitive brief | `competitive-brief` | all | 3–5 pages |
| IFU comparison report | `ifu-comparison` | **medical-device** | 2–4 pages |
| Decision log / ADR roll-up | `decision-log` | all | 1–10 pages |
| Press release / launch | `press-release` | all | 1 page |
| Investor update | `investor-update` | all | 1–2 pages |
| Onboarding doc | `onboarding-doc` | all | 3–6 pages |
| System Requirements Document (SRD) | `srd` | all | 5–15 pages |
| Software Requirements Specification (SRS) | `srs` | all | 5–20 pages |
| Hardware Requirements Specification (HRS) | `hrs` | all | 5–20 pages |
| Risk brainstorm | `risk-brainstorm` | **medical-device** | 2–4 pages |

Scaffolds support **markdown** and **html** formats. Docx and xlsx ship per-doc with the v1.x full implementations.

The one-pager does **not** ship a docx writer (PRD §11 — a one-page leave-behind is better as markdown or html).

## Rendering

```
cb render <doc> [--path <vault>] [--out <file>] [--format markdown|html|docx]
```

### MRD

```
cb render mrd                                     # markdown → <vault>/exports/MRD.md
cb render mrd --format html                       # HTML     → <vault>/exports/MRD.html
cb render mrd --format docx                       # DOCX     → <vault>/exports/MRD.docx
cb render mrd --out /tmp/board-mrd.md             # custom path
```

The MRD has the section structure documented in PRD §11. Profile-conditional sections (IFU, Regulatory landscape) are omitted entirely when the active profile isn't medical-device — not rendered empty, not stubbed out.

### One-pager

```
cb render one-pager                                # markdown → <vault>/exports/one-pager.md
cb render one-pager --format html                  # HTML     → <vault>/exports/one-pager.html
```

The one-pager picks: the first product by id, the highest-confidence positive pillar (non-goal-excluded), the first persona, the feature most related to the primary product, and the first customer-interview source. When any of those is missing, the section degrades to a hint like "Run `intake persona` to define one."

### Scaffolds

Every scaffold follows the same shape: `cb render <doc-name> [--format markdown|html]`. Each lands under `<vault>/exports/<doc-name>.<ext>` by default.

```bash
cb render pid                                      # → <vault>/exports/pid.md
cb render project-charter
cb render stakeholder-register
cb render risk-register                            # medical-device only
cb render status-report
cb render meeting-minutes
cb render lessons-learned
cb render business-plan
cb render sales-battle-card                        # → sales-battle-card-<first-competitor-id>.md
cb render sales-battle-card --competitor competitor-pulseguard-medical
cb render competitive-brief
cb render ifu-comparison                           # medical-device only
cb render decision-log
cb render press-release
cb render investor-update
cb render onboarding-doc
cb render srd
cb render srs
cb render hrs
cb render risk-brainstorm                          # medical-device only
```

**Scaffold conventions:**
- Each output ends with the line: _"v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`."_
- Sections that have populated typed nodes (e.g. `stakeholder-register` finds `stakeholder` nodes) render real content with `[node-id]` citations.
- Sections that have no inputs degrade to bracketed placeholders for adopters to fill in, with a hint pointing at the right `intake` sub-mode.
- Medical-device-only scaffolds (`risk-register`, `ifu-comparison`, `risk-brainstorm`) raise a clear error when invoked under any other profile.
- The sales-battle-card is **per-competitor** — without `--competitor`, the first competitor by id is chosen and embedded in the output filename so multiple cards can coexist.
- Scaffolds support **markdown** and **html**. Docx and xlsx ship per-doc with the v1.x full implementations.

## What this skill does NOT do

- Does not modify vault nodes. For knowledge capture, use the `intake` skill. For document ingestion, use `atomize`.
- Does not push to git. The user (or their team) decides when to commit `exports/`. If they want a commit, ask first and propose a structured message naming what got regenerated.
- Does not bypass the controlled-document boundary. The MRD and one-pager are planning artifacts. When the active profile is `medical-device`, every generated document carries the footer:

  > This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

  Do not strip that footer. If the user asks for a controlled document, refuse and explain — company-brain is for the layer above the QMS.
- Does not invent content. If a section reads sparsely (e.g. "No personas captured yet"), the right answer is to run `intake persona` and re-render, not to hand-edit the output.

## Branding integration

The generators read from `<vault>/_branding/`:

- `colors.yaml` — palette (primary, secondary, accent, text, background, muted) + typography (`font_family_headings`, `font_family_body`). Defaults are used for any field not set.
- `logo.png` / `logo.jpg` / `logo.svg` — picked up if present. The HTML wrapper does not currently embed it; the docx writer does not currently embed it. Both are intentional v0.3.0 simplifications and can be lifted later.
- `templates/<doc>.md.j2` — overrides the bundled template by name. A vault that drops a custom `mrd.md.j2` here gets full control over MRD content shape without changing the codebase.
- `templates/html-wrapper.html.j2` — overrides the bundled HTML shell. A vault can wrap its docs in its own page chrome (header, nav, custom CSS) without touching company-brain.

## Idempotency

Re-running a generator on an unchanged vault produces **byte-identical output modulo the single generation-date line in the footer**. This is the contract:

- The same vault + the same `--date` flag → identical markdown bytes, identical HTML bytes.
- DOCX files are byte-identical too — the writer normalizes the docx core properties (`<dcterms:created>`, `<dcterms:modified>`, author) to the pinned date / a stable string, and re-packs the underlying zip with deterministic entry order and a fixed (1980-01-01) per-entry timestamp.
- This is what makes git diffs on `exports/` meaningful — you can tell what *content* changed by reading the diff, not just "the docs regenerated."

If you generate a doc, the user makes some vault changes via `intake`, and you regenerate, the diff in `exports/MRD.md` shows exactly which sections the new nodes affected. That's the whole point.

## After rendering

- Report the output path and size to the user.
- If `cb validate` had errors before render, remind the user to fix them.
- If the user wants the docs committed, ask first, then `git add exports/ && git commit -m "Regenerate MRD and one-pager"`. Don't push.

## What to do when something goes wrong

- **`cb render` fails with `VaultNotFoundError`.** The path isn't a vault. Confirm `_system/PROFILE.md` exists.
- **`cb render` fails with `template not found`.** A vault override at `_branding/templates/` may have a syntax error; check the file. If no override exists, the bundled template is missing — reinstall company-brain.
- **Output reads sparsely.** The vault is sparse for the doc's input set. Don't paper over it — surface the gaps. For the MRD, the "Uncited claims" subsection in §8 is the authoritative list of nodes lacking sources.
- **A non-goal pillar shows in the wrong section.** Non-goal classification is by `tag: non-goal` (primary) or title prefix `"Non-Goal"` (fallback). If a pillar should be classified as non-goal but isn't, add the tag and re-render.
- **The docx is missing formatting you expected.** The docx writer covers headings, paragraphs, bullets, blockquotes, tables, and inline bold/code. Ordered lists, nested lists, fenced code, and links pass through as plain text. If you need more, raise an issue rather than hand-editing the docx.
