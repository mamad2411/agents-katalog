---
name: voice-notes-processor
description: Processes raw, unstructured voice note transcripts into structured ideas, concepts, action items, and projects, routing them to appropriate Baza layers.
---

---
name: "voice-notes-processor"
description: "Processes raw, unstructured voice note transcripts into structured ideas, concepts, action items, and projects, routing them to appropriate Baza layers."
last_updated: "2026-05-23"
id: "UFTM-SKILL-002"
---

# Skill: Voice Notes Processor (Voice Transcript Distiller)

The `voice-notes-processor` skill is a custom AI-driven utility designed to ingest raw, unstructured stream-of-consciousness voice note transcripts (often recorded on-the-go with mobile devices) and distill them into highly structured, actionable Baza assets. It specializes in cleaning up transcription errors, identifying bilingual English/Russian code-switching, extracting core ideas and concepts, generating tasks, and routing them to their respective CORE_OS layers.

---

## 🚀 Quickstart

Run this skill on a voice note transcript in your vault:
```bash
Scribe, run voice-notes-processor on [[00-Inbox/My Voice Note Transcript]]
```

---

## 📖 Operational Instructions

When processing a raw voice note transcript, the agent must perform the following six steps:

### 1. 🧹 Transcription Remediation & Bilingual Cleanup
*   **Acoustic & Transcription Error Fixes:** Correct common voice-to-text errors, phonetic misspellings, and technical jargon (e.g., "composer" -> "Composio", "neon db" -> "Neon DB", "pod ruga" -> "Podruga").
*   **Bilingual Code-Switching:** Process Russian-English transitions gracefully, translating thoughts where necessary while preserving the unique context of Kamilla's bilingual professional/personal notes.

### 2. 🧠 Semantic Extraction & Taxonomy Allocation
Analyze the transcript for entities and map them to the proper Baza taxonomy:
*   💡 **Ideas & Concepts (`CNCP`):** Abstract thoughts, theories, or models.
*   📋 **Action Items & Tasks (`TODO`):** Discrete, owned, and dated tasks.
*   🚀 **Projects & Sprints (`PLAN` or `SPRNT`):** Larger initiatives with multiple deliverables.
*   📜 **SOPs & Rules (`SOP` or `PRTCL`):** Process workflows or system laws.
*   👥 **CRM Links (`CRM`):** People, organizations, or fencing clubs mentioned.

### 3. 🗺️ Layer Routing Protocol
Determine which CORE_OS Layer each extracted asset belongs to:
*   **Layer 1 (Machine/Tooling):** Custom scripts, tools, or tech specs (`SPEC`, `BPMN`).
*   **Layer 2 (Operational/Rules):** Workflows, maps, matrices (`SOP`, `MAP`, `RACI`).
*   **Layer 3 (Tracking/Reporting):** Activity logs, reflections, postmortems (`LOG`, `RFLCT`, `PSTMR`).
*   **Layer 4 (Spatial/Semantic):** Academic references, book reviews (`SRC`, `BOOK`).
*   **Layer 5 (Client/Project):** Sprints, plans, client events (`PLAN`, `SPRNT`, `EVT`).
*   **Layer 6 (Comms/Brand):** Brand assets, email drafts, instant messages (`ASST`, `EMAIL`, `MSG`).

### 4. 📝 Action Item Generation
Extract all explicit and implicit commitments, assigning clear owners, deadlines, and context. Format them as standard Obsidian checklists:
*   `- [ ] 📅 [Task Name] (Target Date): [Detailed Context] | Layer: [Layer] | Link: [[WikiLink]]`

### 5. 🔑 Strategic Synthesis (The "Aha!" Moment)
Identify the "Golden Thread" of the voice note — the single most important strategic insight or creative breakthrough that Kamilla was articulating, and highlight why it is valuable to her or her projects.

### 6. 📂 Baza File Generation or Update
Generate a new structured note under `00-Inbox/` (or update existing files if the voice note refers to an active project), ensuring full compliance with the YAML frontmatter protocol.

---

## 📊 Output Schema Template

Every processed voice note must be compiled into a note with the following structure:

```markdown
---
id: BAZA-NOTE-[Next_ID]
type: voice_note_analysis
source_audio: "[Reference to Audio File or N/A]"
date: YYYY-MM-DD
topics: [topic1, topic2]
status: processed
---

# 🎙️ Voice Note Distillation: [Clear, Descriptive Title]

## 📋 Metadata & Context
*   **Original Date:** [Date of recording]
*   **Transcription Quality:** [High / Medium (with remediation notes)]
*   **Primary Focus:** [1-sentence summary of the recording's intent]

## 🧹 Remediation & Bilingual Log
*   *Transcribed:* "[Raw error-prone phrase]" ➡️ *Remediated:* "[Corrected term/concept]"
*   *Bilingual Context:* [Notes on Russian-English code-switching and translations applied]

## 🧠 1. The Core Idea & Concept Extraction
### [Concept 1: Name]
*   **Description:** [Detailed breakdown of the idea]
*   **Baza Layer:** Layer [X] ([Layer Name])
*   **Target Note Type:** `[CNCP/SPEC/MAP/etc.]`
*   **Strategic Alignment:** [How this aligns with Kamilla's brand or consulting models]

## 🛠️ 2. Action Items & Task Breakdown
*   [ ] 📅 [Task 1] (YYYY-MM-DD): [Context] | Owner: [Agent/Kamilla] | Layer: [X]
*   [ ] 📅 [Task 2] (YYYY-MM-DD): [Context] | Owner: [Agent/Kamilla] | Layer: [Y]

## 👥 3. CRM & Stakeholder Links
*   **People Mentioned:** [[Person_Name]] (CRM Profile) — [Role/Context]
*   **Organizations:** [[Organization_Name]] — [Context]

## 🔑 4. The Strategic "Aha!" Discovery
> [Write a bolded, insightful summary of the core breakthrough. What is the "unfair advantage" or strategic pivot hidden in this stream of consciousness?]

## 🗺️ 5. Next-Step Asset Routing
| Asset Name | Target Path | Target Note Type | Status |
| :--- | :--- | :--- | :--- |
| `[Asset Name]` | `[Path in Baza]` | `[Type]` | [Draft / Pending Sync] |
```