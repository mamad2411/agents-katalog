---
name: documents-orchestrator
description: "Route a document task to the right skill among the documents specialists — office formats (DOCX/PDF/PPTX/XLSX), docs sites, changelogs, OCR extraction, natural-language PDF edits, NotebookLM, and diagram authoring. USE WHEN a user wants to create, edit, extract from, convert, or publish a document but hasn't named the specific tool or format."
cluster: documents
version: 1.0.0
---

# Documents Orchestrator

The single entry skill for document work. It locates the task on the **format × intent** map and
delegates to one of 8 specialist spokes. The cross-cutting decision every document task shares —
whether you need the **editable source** (round-trippable, structure preserved) or a **rendered
artifact** (pixel-fidelity output you cannot edit back) — lives in `documents-core`; read it
before you pick a tool, because the choice locks which spoke can touch the file next.

## Cluster map (routing by intent → spoke + role)

**Office documents (create / edit / extract / convert)**
- Word, PDF, PowerPoint, Excel — the full editable engine → `documents` *(bundles `docx/`, `pdf/`, `pptx/`, `xlsx/` subskills + a Playwright HTML→PDF report pipeline)*
- Quick natural-language PDF tweaks ("rotate page 3", "redact this") → `nano-pdf`

**Extract & ingest (document → data)**
- Scanned/image PDF → text + structured data with confidence flags → `deepread-ocr`
- Turn a corpus into a notebook, briefing, or podcast → `notebooklm`

**Publish & narrate the docs themselves**
- Build/maintain a documentation site → `mintlify`
- Generate user-facing release notes from git history → `changelog-generator`

**Diagrams & visual documentation**
- Professional draw.io diagrams (flowcharts, BPMN, WBS/Gantt/RACI, network, UML) → `drawio-diagrams-enhanced`
- Animate a Mermaid diagram into a GIF → `mermaid-to-gif`

## Picked-up spokes

Additional documents spokes folded in from the antigravity-awesome-skills library (MIT). Route to these the same way — load on demand by reading their `SKILL.md`.

**Author project docs**
- Write an absurdly thorough `README.md` after deep codebase exploration (tech stack, getting-started, architecture, env vars, scripts, testing, deployment, troubleshooting) → `readme`

**Rendered marketing artifacts**
- Capture true-retina (2x) marketing screenshots of an app with Playwright — discover routes/features from the codebase, handle login, then shoot each view (Product Hunt / social / landing / docs) → `screenshots` *(one-way render gate: produces PNGs you cannot edit back into the app)*

## Standard Operating Flow

1. Classify the task: which **format** (DOCX/PDF/PPTX/XLSX/diagram/site) and which **intent** (create → edit → extract → convert → publish).
2. Decide **editable vs rendered** (the model in `documents-core`). If the user needs to keep editing, stay in the native format and refuse a one-way render until they confirm.
3. Delegate to the spoke(s). Multi-step asks fan out in pipeline order (e.g. "scan this contract and summarize" → `deepread-ocr` → `notebooklm`; "report from the assessment data" → `documents` ConsultingReport → Playwright PDF).
4. Return: chosen spoke(s), whether output is editable or rendered, the format, and the next action.

## Guardrails

See `documents-core`. In short: **preserve the source** — prefer the editable, round-trippable
path; treat any render-to-PDF/OCR/GIF as a one-way gate and say so before crossing it. Never
hardcode a value a formula should compute (XLSX), never silently flatten tracked changes (DOCX),
and never trust OCR text without surfacing its confidence (deepread). Keep the original file
intact; write derived artifacts alongside it, not over it.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
