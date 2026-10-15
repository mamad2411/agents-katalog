---
name: sa-doc
description: Generate a complete System Analysis & Design document (use cases, sequence/activity/state diagrams, class + ER model, data dictionary, architecture, screens, traceability) from one validated central model — Markdown canonical, PDF optional. Trigger on /sa-doc, "ทำเอกสาร SA", "เขียนเอกสารวิเคราะห์และออกแบบระบบ", "ทำ project report วิชา SA", "generate SA document", "system analysis document", "SA&D report", "SDD", or when the user hands over a brief/requirements/codebase and asks for a full design document. Do NOT use for a single ad-hoc diagram, for explaining a problem interactively (problem-description), or for reviewing an existing document (scrutinize).
argument-hint: "[brief / file path / 'academic'|'professional' / 'pdf'|'md']"
effort: max
---

<!-- generated: third-party requirements -->
> **Requires:** `pip install pyyaml` — this skill's scripts import `yaml`.

# sa-doc — SA&D document generator

One validated model, one consistent document. Every section of the output is
derived from `sa-model.yaml`; a Python validator blocks generation until the
model is referentially consistent. This exists because hand-written SA
documents rot by copy-paste: the reviewed specimen carried 30+ cross-artifact
contradictions (see ADR 0025 at the marketplace root:
`docs/adr/0025-sa-doc-generates-from-central-model.md`).

## The one rule: Source-or-TBD

Every value in the model and every fact in the document must trace to the
user's input. If the input does not state it, the value is `TBD` — never a
plausible-looking default, estimate, or example. The job is a *faithful* SA
document, not a *convincing* one. This covers **every** kind of fact: actors,
entities, fields, numbers, prices, dates, NFR metrics, field sizes and samples,
cardinalities, states and triggers, security controls, architecture
style/components/deployment/environments, budget amounts, citations,
stakeholder interests, frequencies.

The validator **cannot** enforce this — it checks the model's internal
consistency, and never receives the source input, so it can't tell an invented
value from a real one. Faithfulness therefore rests on this rule, not on the
gate. A `TBD` is a correct, tracked answer; an invented-but-reasonable value is
a defect. **When you are unsure whether the input stated something, it did not —
write `TBD` and ask.** Guessing is a defect, not a shortcut; obeying the letter
here is obeying the spirit.

## When NOT to use

- One diagram or one section on demand — just draw it, no model needed.
- Explaining a problem interactively → `problem-description`.
- Reviewing/critiquing an existing SA document → `scrutinize`.

## Flow

### 1. Intake

Gather the input (file paths, pasted text, or the conversation so far).
Detect the input language → document language (an explicit language request
wins). Ask the user, in one round:

1. **Profile** — `academic` (course report: adds literature, Gantt plan,
   budget, bibliography) or `professional` (work SDD: adds security design,
   deployment, test-case seed).
2. **Output** — `md`, `pdf`, or `both`.
3. **Project name** — suggest one from the input.

Working directory: `./SA-<project>/` under the current directory unless the
user names another. Persist the raw input (pasted text, the relevant file
excerpts, or the conversation brief) to `SA-<project>/.source/input.txt` — it is
the audit trail for what the document is allowed to say, and the faithfulness
check in Step 4.5 reads it.

### 2. Build the model

Write `SA-<project>/sa-model.yaml` following `references/model-contract.md`
(the schema lives only there). Fill everything the input answers; for required
slots the input does not answer, ask — grouped, fewest possible questions.
Apply the **Source-or-TBD rule** (top of this file): anything the input is
silent on is `TBD` (tracked), never a plausible value — this holds even where a
validator warning nags you to fill a field (W6/W8/W9) or a profile requires a
section (E8): satisfy the gate with a `TBD`-valued record, never manufactured
content. The bundled example
`${CLAUDE_SKILL_DIR}/scripts/fixtures/sa-model-bookstore.yaml` shows a
complete, clean model.

### 3. Validate — the gate

```
python ${CLAUDE_SKILL_DIR}/scripts/validate_model.py SA-<project>/sa-model.yaml
```

- **Errors block generation.** Fix the model; ask the user when the fix is a
  domain decision. Re-run until exit 0.
- **Warnings** are shown to the user and either fixed or explicitly accepted —
  never silently ignored.
- The TBD inventory is carried into the final summary.

Never write the document while the validator reports errors.

### 4. Generate the document

Write `SA-<project>/SA-<project>.md` from the model using
`references/template-core.md` plus the profile file
(`references/template-academic.md` / `references/template-professional.md`).
Rules:

- Facts come from the model only; prose connects, never introduces.
- **Provenance self-check before writing:** for every filled model leaf, name
  the input span it came from; any leaf you cannot trace, flip to `TBD`. STOP
  words that usually mark a guess — "probably / typically / usually / standard /
  e.g. / assume / should be", plus round-number metrics, sample data, prices,
  dates, environments, or security mechanisms with no input source. (Class-vs-
  instance: a concrete sourced value that merely contains such a word is fine —
  the target is invented content, not a literal word ban.)
- Diagrams follow `references/diagram-convention.md` —
  one Mermaid overview at the top, type-matched section diagrams
  (`sequenceDiagram`, `classDiagram`, `erDiagram`, `flowchart TD`,
  `stateDiagram-v2`). The data model carries both a `classDiagram` (OO/domain
  view) and an `erDiagram` (database view).
- Emit the document-furniture markers the core template specifies
  (`<!-- sa-doc:toc -->`, `<!-- sa-doc:pagebreak -->`) so the render step can
  build the contents page and page breaks.
- The 13-field use case semantics in the core template are non-negotiable
  (postcondition = guaranteed state; extensions anchored to steps; no
  boilerplate).

### 4.5 Faithfulness check — the anti-fabrication gate

```
python ${CLAUDE_SKILL_DIR}/scripts/check_doc_provenance.py SA-<project>/SA-<project>.md SA-<project>/sa-model.yaml
```

Traces every hard fact in the generated document (numbers, money, percentages,
dates) back to a model value — enforcing "prose connects, never introduces"
mechanically, because the validator cannot (it never sees the source). Pass
`--source SA-<project>/.source/input.txt` to also accept a token that is in the
input but not yet in the model. Structural numbers (section/figure/table/FR/TC
ids, list markers) are exempt. Each flagged token is either a fabrication to
remove, or a real value missing from the model — add it to `sa-model.yaml` and
regenerate. This is a report, resolved or justified like a validator warning,
not a hard block.

### 5. Render (pdf/both only)

```
python ${CLAUDE_SKILL_DIR}/scripts/render_doc.py SA-<project>/SA-<project>.md --pdf
```

Produces a self-contained HTML and prints it to PDF with headless Edge/Chrome.
The renderer builds the table of contents from the `<!-- sa-doc:toc -->`
marker, honours `<!-- sa-doc:pagebreak -->`, and auto-numbers figures/tables in
the document language (auto-detected; override with `--lang th|en`). Add
`--page-numbers` for an academic report that needs a page footer (it keeps
Chrome's footer at the cost of also showing the date/URL). No browser found →
the script says so and the HTML plus print instructions is the deliverable; do
not treat that as a failure. Offline machines: pass `--marked-js` /
`--mermaid-js` with local copies.

## Wrap-up

Summarize: file paths, warnings the user accepted, the TBD inventory (what is
still unknown), and offer next steps — `generating-test-cases` for a test
suite from the use cases, or the backlog pipeline to file open TBDs as work
items. To change the document later, edit `sa-model.yaml`, re-validate,
regenerate — never patch the generated file by hand.

## Rules

- Never generate while the validator reports errors.
- Source-or-TBD (top of this file): never invent a domain fact of any kind —
  when the input is silent, record `TBD` and ask; never fill a plausible value.
- Never patch the generated document directly — the model is the source of truth.
- The schema is defined only in `references/model-contract.md`; do not restate
  it elsewhere.
