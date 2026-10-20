---
name: threat-modeling-artefacts
description: Produce threat-modelling deliverables and artefacts — threat model documents, risk registers, kickoff packs, security acceptance criteria, executive summaries, compliance evidence packages, and squad self-serve kickstarts. Use this skill whenever the user asks to *produce*, *draft*, *generate*, *write*, or *create* a threat-modelling artefact — phrases like "draft a threat model document", "generate a risk register", "produce security acceptance criteria", "build a kickoff pack", "create an executive summary of threat model findings", "give me a TM doc for [system]", "help my squad self-serve a threat model on our component". This skill auto-detects available rendering capabilities (docx, pdf, xlsx agent skills, or Python with pandoc/openpyxl) and produces the highest-fidelity output available, falling back to markdown and CSV which work everywhere. Does *not* trigger for analytical asks like "what is STRIDE" or "what threats apply to [system]" — those go to the `threat-modeling` skill.
---

# Threat-modelling Artefacts

This skill turns threat-modelling analysis into shippable deliverables. The companion `threat-modeling` skill teaches you how to *think* about threats systematically; this skill produces the artefacts an appsec engineer or consultant actually ships in a real engagement.

It is a **router**: the SKILL.md body points you at one of seven deliverable workflows. Each workflow is documented in detail in `references/` and shipped with a skeletal template in `assets/templates/` plus a complete worked example in `assets/worked-examples/` using a single fictional system, **Acme Lending**.

## When to use this skill

Use this skill when the user asks for an *artefact*. Trigger words: produce, draft, generate, write, create, build, ship, render, output. Object words: threat model document, TM doc, risk register, kickoff pack, pre-mortem, acceptance criteria, security stories, squad kickstart, executive summary, exec summary, compliance evidence, control mapping, APRA mapping, ASVS evidence, ISO 27001 mapping, NIST CSF mapping.

**Do not use this skill** for analytical asks — "what is STRIDE", "what could go wrong with X", "is OAuth client credentials safe here", "build me a DFD" (the diagram alone is analysis, not a deliverable). Those go to the `threat-modeling` skill.

If the user asks for something that combines both (e.g. *"threat model my partner API and produce the threat model document"*), use the `threat-modeling` skill first to do the analysis, then use this skill to package the output.

## The seven deliverable types

| # | Deliverable | When to produce | Reference |
|---|---|---|---|
| 1 | Threat model document | The canonical engagement deliverable. Run-of-mill output of an appsec review. | `references/threat-model-document.md` |
| 2 | Kickoff pack | Week zero of an engagement. Pre-mortem, first-cut DFD, trust-boundary list, irreversible-decisions list, RACI. | `references/kickoff-pack.md` |
| 3 | Risk register | Operational tracking. Markdown table + CSV (+ XLSX if possible). | `references/risk-register.md` |
| 4 | Security acceptance criteria | Per-feature security requirements for engineering tickets. Gherkin or user-story format. | `references/security-acceptance-criteria.md` |
| 5 | Squad self-serve kickstart | Force multiplier. Squads produce their own first-cut TM on their own component. | `references/squad-self-serve-kickstart.md` |
| 6 | Executive summary | One-pager for CISO / product / board. Top risks, mitigation readiness, compliance posture. | `references/executive-summary.md` |
| 7 | Compliance evidence package | Mapping coverage to APRA CPS 234, OWASP ASVS, ISO 27001:2022 Annex A, NIST CSF 2.0. | `references/compliance-evidence-package.md` |

Each reference file documents the deliverable's purpose, required sections, customisation points, and rendering options. Each pairs with a skeletal template and a complete Acme Lending worked example so you can see the bar before you start filling in.

## Capability detection — run this before producing any rendered output

Markdown and CSV outputs work everywhere with no tooling. DOCX, PDF, and XLSX require either an installed agent skill (`docx`, `pdf`, `xlsx`, `pptx`) or Python with pandoc / openpyxl on the host.

**Run this probe before producing any rendered-output deliverable**, in this order:

1. **Inspect `available_skills`** in the current session. If `docx`, `pdf`, `xlsx`, or `pptx` is present, prefer the agent skill for that format — they produce the cleanest output and route through the platform's sanctioned pipeline.
2. **Probe Python.** On Windows, the canonical command is `python`. On macOS and Linux, it is usually `python3`, sometimes `python`. Try `python --version`; if that fails, try `python3 --version`. If either succeeds, the bundled scripts under `scripts/` can be used.
3. **Probe pandoc** (`pandoc --version`) if DOCX or PDF rendering is needed. Pandoc is the dependency for `render_to_docx.py` and `render_to_pdf.py`.
4. **Probe openpyxl** (`python -c "import openpyxl"`) if XLSX rendering is needed via the bundled script.

If neither path is available, **produce markdown and CSV only**. Tell the user briefly what was used and what wasn't — e.g. *"Produced markdown only — DOCX rendering wasn't available in this environment (neither the `docx` agent skill nor pandoc was found)."*

Full algorithm and code snippets: `references/capability-detection.md`.

## The fallback hierarchy by format

| Format | First choice | Second choice | Floor |
|---|---|---|---|
| Markdown (`.md`) | direct write | — | guaranteed |
| CSV (`.csv`) | direct write | — | guaranteed |
| DOCX | `docx` agent skill | `scripts/render_to_docx.py` (Python + pandoc) | markdown only |
| PDF | `pdf` agent skill | `scripts/render_to_pdf.py` (Python + pandoc) | markdown only |
| XLSX | `xlsx` agent skill | `scripts/render_to_xlsx.py` (Python + openpyxl) | CSV only |
| Mermaid lint | `scripts/validate_mermaid.py` | inline regex check | acceptable to skip |
| Threat-ID lint | `scripts/threat_id_check.py` | inline check | acceptable to skip |

The Python scripts are **optional fallbacks**, not the default path. They exist for environments where agent skills aren't available but Python is. Markdown and CSV outputs are guaranteed regardless of environment.

## Dependency on the `threat-modeling` skill

This skill is a soft dependency on `threat-modeling`. If that skill is installed in the session, route analytical content (STRIDE letters, OAuth threats, GraphQL hardening, OWASP API Top 10, MITRE ATLAS, OWASP LLM Top 10, etc.) through it rather than restating the analysis here.

**Detection**: check whether `threat-modeling` appears in `available_skills`. If yes, in any reference that needs analytical content, point to the right file in that skill — e.g. *"For STRIDE detail, see `threat-modeling/references/stride.md`"*. If no, fall back to `references/analytical-fallback.md` which carries a minimal analytical summary so this skill still works standalone.

The fallback is intentionally minimal — it's a safety net, not a replacement. The output the user gets is richer when both skills are present.

## Workflow per deliverable type

For every deliverable, follow this sequence:

1. **Read the reference** for that deliverable type (e.g. `references/threat-model-document.md`).
2. **Load analytical content** from the `threat-modeling` skill (when present) or from `references/analytical-fallback.md` (when not). Anything STRIDE-related, OAuth threat catalogues, GraphQL threats, ML pipeline threats, etc. flows through that route.
3. **Look at the worked example** (`assets/worked-examples/`) for the same deliverable type. The Acme Lending examples are the shipping bar.
4. **Run capability detection** (above) if a rendered-output format is requested.
5. **Fill in the template** (`assets/templates/`). Templates have `<!-- INSTRUCTION: ... -->` and `<!-- HOUSE STYLE: ... -->` markers that explain section purpose and customisation points.
6. **Render** through the highest available path in the fallback hierarchy.
7. **Validate** with the bundled lints where applicable — `validate_mermaid.py` on any DFD, `threat_id_check.py` across the artefact set.
8. **Output to the user** with a one-sentence note describing the capability path used.

## Customisation — house style

Templates default to common patterns (Mermaid, markdown, CSV, the canonical sections in the references). They are not meant to be opinionated — different organisations have different house styles. Customisation points are marked inline with `<!-- HOUSE STYLE: ... -->` comments.

Common house-style customisations and where to make them: `references/house-style-customisation.md`.

## Critical rules

- **Australian English** throughout (organisation, analyse, behaviour, defence, customise, prioritise, authorise, artefacts).
- **Imperative tone** in references; declarative tone in templates and worked examples.
- **Threat IDs are required.** Format: `TM-[component]-[number]` — e.g. `TM-AUTH-001`, `TM-WEBHOOK-014`. Every threat in a template, worked example, or generated artefact has one. Acceptance criteria back-reference threat IDs. Risk register entries reference threat IDs. Compliance mappings reference threat IDs.
- **Cross-reference, don't duplicate.** Analytical content sits in the `threat-modeling` skill or in `analytical-fallback.md`. Don't restate STRIDE letters or OWASP categories here.
- **Capability detection runs before rendered-output deliverables.** Don't assume DOCX or XLSX is available; probe and adapt.
- **Markdown and CSV are floors.** Always produce these when relevant. DOCX, PDF, and XLSX are quality-of-life additions when the environment supports them.
- **Acme Lending is fictional.** The worked examples are illustrative. Never attribute Acme Lending content to a real organisation.
- **No bullet points in declines or warnings.** Use prose for those.

## Quick reference — what to read for each deliverable

| Ask | Reference | Template(s) | Worked example |
|---|---|---|---|
| Draft a threat model document | `references/threat-model-document.md` | `assets/templates/threat-model-document.md`, `threat-model-document-concise.md` | `assets/worked-examples/acme-lending-threat-model.md` |
| Build a kickoff pack | `references/kickoff-pack.md` | `assets/templates/kickoff-pack.md`, `pre-mortem.md` | `assets/worked-examples/acme-lending-kickoff-pack.md` |
| Generate a risk register | `references/risk-register.md` | `assets/templates/risk-register.md`, `risk-register.csv` | `assets/worked-examples/acme-lending-risk-register.md`, `.csv` |
| Produce security acceptance criteria | `references/security-acceptance-criteria.md` | `assets/templates/security-acceptance-criteria-gherkin.md`, `security-acceptance-criteria-user-stories.md` | `assets/worked-examples/acme-lending-security-acceptance-criteria.md` |
| Hand a squad a self-serve kickstart | `references/squad-self-serve-kickstart.md` | `assets/templates/squad-self-serve-questionnaire.md`, `squad-escalation-decision-tree.md` | `assets/worked-examples/acme-lending-squad-kickstart-completed.md` |
| Write an executive summary | `references/executive-summary.md` | `assets/templates/executive-summary.md` | `assets/worked-examples/acme-lending-executive-summary.md` |
| Produce a compliance evidence package | `references/compliance-evidence-package.md` | `assets/templates/apra-cps-234-mapping.md`, `owasp-asvs-evidence.md`, `iso-27001-annex-a-mapping.md`, `nist-csf-2-mapping.md` | `assets/worked-examples/acme-lending-compliance/` (four files) |

## Detail references

| Reference | What it covers |
|---|---|
| `references/threat-model-document.md` | Sections, length, naming, residual-risk language, sign-off |
| `references/kickoff-pack.md` | Five one-pagers, irreversible decisions, RACI seed |
| `references/risk-register.md` | Columns, severity matrix, status values, Jira import flow |
| `references/security-acceptance-criteria.md` | Gherkin vs user-story choice, threat-ID back-references, ticket integration |
| `references/squad-self-serve-kickstart.md` | Questionnaire pattern, escalation decision tree, simplified TM template |
| `references/executive-summary.md` | One-page structure, audience, language constraints |
| `references/compliance-evidence-package.md` | Per-framework mapping format, coverage status values |
| `references/dfd-with-mermaid.md` | Mermaid flowchart for DFDs, trust-boundary subgraph pattern, alternatives (PlantUML, draw.io) |
| `references/risk-scoring.md` | Severity × likelihood matrix (default), FAIR (alternative), DREAD (historical), why CVSS is not used |
| `references/house-style-customisation.md` | Common org-level overrides and where to apply them |
| `references/capability-detection.md` | Full algorithm and code snippets for the runtime probe |
| `references/analytical-fallback.md` | Minimal STRIDE / OWASP / threat content for when `threat-modeling` isn't installed |

## Template index

| Template | Purpose |
|---|---|
| `assets/templates/threat-model-document.md` | Full threat model document |
| `assets/templates/threat-model-document-concise.md` | Shorter variant for simple systems / feature-level TMs |
| `assets/templates/kickoff-pack.md` | Kickoff pack wrapper |
| `assets/templates/pre-mortem.md` | Pre-mortem one-pager |
| `assets/templates/risk-register.md` | Risk register, markdown table |
| `assets/templates/risk-register.csv` | Risk register, CSV with headers (Jira-import-ready) |
| `assets/templates/security-acceptance-criteria-gherkin.md` | Gherkin variant |
| `assets/templates/security-acceptance-criteria-user-stories.md` | User-story variant |
| `assets/templates/squad-self-serve-questionnaire.md` | Squad questionnaire |
| `assets/templates/squad-escalation-decision-tree.md` | Squad escalation decision tree (Mermaid) |
| `assets/templates/executive-summary.md` | Exec summary one-pager |
| `assets/templates/apra-cps-234-mapping.md` | APRA CPS 234 control mapping |
| `assets/templates/owasp-asvs-evidence.md` | OWASP ASVS evidence template |
| `assets/templates/iso-27001-annex-a-mapping.md` | ISO 27001:2022 Annex A mapping |
| `assets/templates/nist-csf-2-mapping.md` | NIST CSF 2.0 mapping |
| `assets/templates/dfd-mermaid.md` | Mermaid DFD scaffold with trust-boundary subgraphs |
| `assets/templates/threat-table-row.md` | Reusable per-threat row format |

## Worked-example index — Acme Lending

`assets/worked-examples/README.md` describes the fictional Acme Lending scenario. The seven primary worked examples plus four compliance mappings demonstrate the deliverable shape and quality bar:

| File | Demonstrates |
|---|---|
| `acme-lending-threat-model.md` | Full TM document |
| `acme-lending-kickoff-pack.md` | Five-component kickoff pack |
| `acme-lending-risk-register.md` | Risk register in markdown |
| `acme-lending-risk-register.csv` | Same content, CSV / Jira-importable |
| `acme-lending-security-acceptance-criteria.md` | Mixed Gherkin + user-story criteria |
| `acme-lending-squad-kickstart-completed.md` | Completed squad self-serve |
| `acme-lending-executive-summary.md` | One-page exec summary |
| `acme-lending-compliance/apra-cps-234.md` | APRA mapping for Acme Lending |
| `acme-lending-compliance/owasp-asvs.md` | OWASP ASVS evidence |
| `acme-lending-compliance/iso-27001.md` | ISO 27001:2022 Annex A mapping |
| `acme-lending-compliance/nist-csf-2.md` | NIST CSF 2.0 mapping |

Threat IDs are reused consistently across the worked examples — `TM-API-003` in the threat model document is the same `TM-API-003` referenced in the risk register, the acceptance criteria, and the compliance mappings.

## Scripts (optional fallback)

| Script | Purpose | Dependencies |
|---|---|---|
| `scripts/render_to_docx.py` | Markdown → DOCX via pandoc | Python, pandoc |
| `scripts/render_to_pdf.py` | Markdown → PDF via pandoc | Python, pandoc, LaTeX or wkhtmltopdf |
| `scripts/render_to_xlsx.py` | CSV → XLSX via openpyxl | Python, openpyxl |
| `scripts/prerender_mermaid.py` | Pre-render Mermaid blocks to PNG and substitute image references — chain with `render_to_docx.py` or `render_to_pdf.py` to embed diagrams inside DOCX / PDF | Python, Mermaid CLI (`mmdc` or `npx -p @mermaid-js/mermaid-cli mmdc`), Chrome/Edge for headless rendering |
| `scripts/validate_mermaid.py` | Lint Mermaid blocks for syntax errors | Python only |
| `scripts/risk_register_to_jira_csv.py` | Reshape risk register markdown/CSV → Jira-import CSV | Python only |
| `scripts/threat_id_check.py` | Validate threat-ID uniqueness and resolution across artefacts | Python only |

Each script supports `--help`, performs a dependency check at startup, and exits non-zero with a clear message if a dependency is missing — so a failed fallback degrades to markdown/CSV gracefully.

**Embedding Mermaid diagrams in DOCX / PDF.** Pandoc on its own embeds Mermaid blocks as fenced code, not as rendered diagrams. To get diagrams *inside* a Word doc or PDF, chain the two scripts: `python scripts/prerender_mermaid.py input.md --output input-rendered.md` then `python scripts/render_to_docx.py input-rendered.md`. The chain is designed for **graceful degradation** — if Mermaid CLI / Node / npx / a browser isn't available, `prerender_mermaid.py` copies its input to its output unchanged and exits 0, so the next step still produces a valid DOCX (with Mermaid blocks shown as fenced code rather than diagrams). When a single block fails to render, the others still render and the failed block stays as fenced code. Pass `--strict` to fail fast instead. Default output format is PNG at 3200px width and 2x scale — high enough that Word's downsample stays sharp. See `references/capability-detection.md` for the full contract, including when to switch to `--format svg` (PDF / HTML targets, or DOCX with rsvg-convert installed).

## Notes on framework currency

The compliance evidence templates reference specific framework versions and clauses. If any of the version numbers look out of date, run the `update-threat-modeling-resources` skill, which keeps the threat-modelling reference material and its sister skills current.
