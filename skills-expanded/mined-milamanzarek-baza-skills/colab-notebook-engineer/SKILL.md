---
name: colab-notebook-engineer
description: "Architects, refactors, audits, and validates Google Colab notebooks for agency and Baza workflows. Enforces the 7-stage topology contract (BAZA-PRTCL-009 v1.2), two-tier hierarchical folding (# and ##) for mobile and iPad ergonomics, the dual-interface Markdown card standard, dedicated subfolder vaults with co-equal README documentation, embedded Google Drive/Colab links, zero-stub execution discipline, variable ingestion externalization (Colab Forms, Sheets, Secrets), and runs automated headless QA audits via GLBL-SOP-045."
category: workflow-automation
risk: safe
source: own
date_created: 2026-09-05
created_by: "Kamilla + Antigravity (Gemini 3.8 Flash)"
version: 1.1.0
tags: ["colab", "jupyter", "notebook-automation", "dual-interface", "python", "qa-audit"]
tools: ["antigravity", "claude", "gemini", "cursor"]
---

# Colab Notebook Engineer & QA Validator

## Purpose
This skill provides end-to-end engineering, refactoring, and quality assurance for Google Colab and Jupyter notebooks. It enforces Baza's dual-interface principle, two-tier mobile ergonomics, deterministic execution standards, dedicated subfolder vaults with companion markdown documentation, and automated pre-flight verification.

Use this skill to transform sprawling scripts or fragile web applications into robust, production-grade Colab pipelines that run reliably for clients and internal teams.

---

## When to Use This Skill
Activate this skill whenever:
- Designing or authoring a new Google Colab notebook from scratch.
- Refactoring an existing notebook to meet Baza standards (`BAZA-PRTCL-009` v1.2).
- Debugging a notebook that fails to produce expected outputs or throws runtime errors.
- Auditing a notebook before deploying it to Google Drive or handing it off to clients.
- Converting a heavy web application (Node.js, React, Firebase) into a lightweight sequential notebook.
- Structuring a notebook for optimal mobile or iPad viewing with collapsible sections.
- Packaging a notebook in its dedicated subfolder with co-equal `README.md` documentation.

---

## Core Architectural Standards

### 1. The 7-Stage Topology Contract (`BAZA-PRTCL-009`)
Every notebook must adhere to the 7 canonical operational stages:
- **Stage 0: AI Assistant Directive & Safe Editing Contract** (Protects code from LLM truncation; embeds Drive and Colab launch links).
- **Stage 1: Environment Setup & Deterministic Dependency Installation** (Zero-crash package management. Never upgrade pre-installed libraries like Pillow or Matplotlib with `-U`, as mid-session binary upgrades cause C-extension PyCapsule pointer mismatches).
- **Stage 2: Authentication, Secret Injection & Service Handshakes** (Google Drive, Cloud services, API keys).
- **Stage 3: Dynamic Variable Ingestion & Configuration** (Externalized parameter intake).
- **Stage 4: Deterministic Data Engine & Core Transformations** (Pure Python calculation and logic).
- **Stage 5: Artifact Production & Media Generation** (Image generation, markdown briefs, PDF exports).
- **Stage 6: Client Delivery, Cloud Sync & Audit Logging** (Drive sync, Google Sheets logging, showcase cards).

### 2. Two-Tier Hierarchical Folding (`#` and `##`)
To ensure smooth navigation on mobile phones, tablets, and desktop sidebars:
- Use top-level Markdown headers (`# 1. ...`, `# 2. ...`) exclusively for the 7 primary operational stages.
- Use second-level Markdown headers (`## 1.1 ...`, `## 6.2 ...`) to decompose distinct functional tasks within a stage.
- Colab automatically converts `#` into master collapsible accordions and `##` into nested sub-accordions. Never bundle multiple unrelated tasks into a single unsectioned block.

### 3. Dual-Interface Markdown Card Pairing
Every functional code cell must be immediately preceded by a dedicated Markdown documentation card. The card must explain:
- **Human Purpose**: What business or operational outcome this cell achieves.
- **Inputs**: Variables, data frames, or files consumed.
- **Outputs**: Files written, memory states modified, or UI cards rendered.
- **Safe Editing Instructions**: Guidance on what parameters can be safely edited without breaking logic.

### 4. Side-Panel LLM Anti-Stubbing Defense (Cell 0 Contract)
Large Language Models operating inside browser side panels (such as Gemini in Colab) tend to summarize large code cells into placeholder stubs (e.g. replacing 400 lines of drawing logic with `print("Done")`).
Cell 0 must always contain an explicit, visible prompt contract instructing any assisting AI:
> "DO NOT summarize, truncate, or replace code cells with placeholder stubs. All edits must preserve existing imports, helper functions, and logic blocks verbatim."

### 5. The Variable Ingestion Triad
Hardcoding parameters inside execution code is strictly forbidden. All variable values must be ingested through three distinct layers:
1. **Interactive Presets**: Colab Form fields using `#@param {type:"string"}` for manual testing.
2. **Batch / Agency Intake**: Dynamic row fetching from a client Google Sheet.
3. **Secure Secrets**: API credentials accessed exclusively via `google.colab.userdata.get()`.

### 6. Auxiliary Failure Isolation Architecture
Secondary or external services (such as logging an audit row to Google Sheets or sending a notification webhook) must reside in isolated `##` subsections and be enclosed within individual `try...except` blocks. A failure to connect to Google Sheets must never prevent asset generation or Google Drive file writing.

### 7. Deterministic Logic Separation
Keep math, layout coordinates, file operations, and validation strictly within deterministic Python functions. Reserve generative AI models exclusively for qualitative text generation or creative analysis.

### 8. Dedicated Subfolder Vault & Co-Equal Documentation Standard
In strict adherence to Baza's Dual-Interface and Co-Equal Access Principles:
- Every notebook MUST reside in a dedicated subfolder matching its name (`notebooks/<Notebook_Name>/`).
- It MUST contain a companion `README.md` explaining What It Is, When to Implement (Triggers), How It Operates (Topology & Flow), Parameter Configuration, Generated Deliverables, and direct clickable links to Google Drive and Google Colab.
- Cell 0 of the `.ipynb` file MUST contain direct links to the Google Drive asset and Colab direct launcher (`> **Google Drive Asset**: [Open in Google Drive](...) | [Open in Google Colab](...)`).

---

## Standard Workflow: How to Build or Refactor a Notebook

### Step 1: Initialize Specification Document
1. Copy `templates/NOTEBOOK_SPEC_AND_QA_CHECKLIST.md` into the workflow directory.
2. Fill out the business objectives, client deliverables, and cell-by-cell topology map.

### Step 2: Assemble Code and Markdown Cells
1. Write Cell 0 with the mandatory AI Safe Editing Contract and embedded Google Drive / Colab links.
2. Pair each code block with its corresponding dual-interface Markdown card.
3. Group related cells under `#` and `##` headers to create collapsible accordions.
4. Wrap all external API and cloud sync operations in failure-isolated exception handlers.

### Step 3: Organize into Dedicated Vault with Companion README
1. Create `notebooks/<Notebook_Name>/` directory.
2. Place `<Notebook_Name>.ipynb` inside.
3. Author comprehensive `README.md` in the same directory covering purpose, triggers, architecture, configuration, deliverables, and cloud links.

### Step 4: Run Automated QA Verification
Execute the automated validator script against the generated notebook or entire fleet:
```bash
python scripts/qa_notebook.py
```

Review the terminal output:
- Verify that all QA gates report `[PASS]` (including QA-09 Subfolder & Markdown Docs).
- If any gate reports `[FAIL]`, correct the cell structure, headers, stubs, or documentation, and re-run.

### Step 5: Deploy and Register
1. Upload/update the validated notebook in Google Drive via `gws.exe`.
2. Record the notebook in the agency Google Sheets Master Matrix.
3. Log the creation in the active Baza Weekly Activity Log.

---

## References and Resources
- `scripts/qa_notebook.py`: Headless automated inspector verifying the quality gates across all notebooks.
- `templates/NOTEBOOK_SPEC_AND_QA_CHECKLIST.md`: Standard specification and QA sign-off template.
- `references/BAZA_PRTCL_009_SUMMARY.md`: Summary of Colab Notebook Architecture Protocol.
- `references/GLBL_SOP_045_SUMMARY.md`: Summary of Pre-Flight Quality Assurance SOP.
