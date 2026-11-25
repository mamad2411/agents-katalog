---
name: story-validator
description: Validate Master and Sprint Stories — template sections, ADO-ready PRD lift, UI/Figma, non-redundancy, AC quality
model: haiku-4-5
token_budget: {input: 8000, output: 2000}
---

> **Scope:** Validates **story markdown** structure and authoring rules. For PRD quality, use `skills/shared/prd-gap-analyzer/`. Do not re-validate the PRD here.
>
> **Authoring standards:** [templates/AUTHORING_STANDARDS.md](../../templates/AUTHORING_STANDARDS.md)

# Story Validator Skill

Templates live in `templates/story-templates/`:

- **Master:** `master-story-template.md`
- **Sprint:** `sprint-story-template.md`

CLI validators (optional): `templates/story-templates/validators/master-story-validator.sh`, `sprint-story-validator.sh`

---

## Master Story — required themes (not legacy § numbering)

Confirm the file includes these **headings** (emoji titles as in template):

1. **🎯 Outcome** — User + business outcome; **do not** paste Problem or full AC here.
2. **🔍 Problem Definition** — Pain and evidence only.
3. **👤 Target User & Context**
4. **⚡ Job To Be Done (JTBD)**
5. **💡 Solution Hypothesis**
6. **🧩 Capability Definition**
7. **📎 PRD-sourced specifics** — Verbatim PRD copy: notifications, errors, limits. **Never** id-only (e.g. `N7` without text). If PRD silent → `USER_INPUT_REQUIRED`.
8. **🎯 Experience Intent** — Qualitative feel; **not** Figma links.
9. **🎨 UI & design** — **Figma (primary)**, prototype, design status, or **N/A** / `USER_INPUT_REQUIRED`.
10. **🧾 Acceptance Criteria** — Given/When/Then; may **reference** rows in 📎 section instead of duplicating strings.
11. **📊 Measurement & Signals** — KPIs, events, baselines.
12. **🧪 Validation Plan** — Pilot/A/B/rollout; **do not** duplicate full KPI tables from Measurement.
13. **⚠️ Risks & Unknowns**
14. **🔗 Dependencies**
15. **🚫 Explicit Non-Goals**
16. **📅 Priority & Rollout Strategy**
17. **🏆 Related Stories** *(optional)*
18. **📝 Notes**
19. **📋 Story Metadata**
20. **🔗 PRD Traceability** — Required table: PRD doc, section IDs, ADO id.

---

## Sprint Story — required themes

1. **🎯 What We're Building** — Deliverable only; **not** a second copy of full Context narrative.
2. **🔍 Context** — Why this sprint.
3. **⚡ Scope** — IN / OUT / assumptions.
4. **📎 PRD / Master lift (this sprint)** — Full strings for this sprint’s scope; or pointer to Master ADO + row if copy already there.
5. **🏗️ Technical Approach**
6. **🧾 Acceptance Criteria** — Checklists; align with Master AC ids where applicable.
7. **🎨 UI & design** — Figma for **this sprint** or N/A.
8. **🔗 Dependencies**
9. **📊 How We'll Measure It** — Sprint target/delta; **do not** duplicate entire Master measurement section.
10. **⚠️ Known Risks**
11. **👥 Team & Effort**
12. **🚀 Definition of Done**
13. **📝 Notes & Updates**
14. **📋 Story Metadata**
15. **🔗 Traceability** — Parent Master + PRD sections.

---

## ADO-ready rules (both types)

- **Self-contained:** Reader should not need the PRD for copy, notifications, or error text.
- **No duplication:** Same paragraph must not appear in Outcome, Problem, and Context. Measurement vs Validation Plan: metrics vs methodology.
- **Readable:** Short sentences, **bold** labels, bullets, blank lines, tables for PRD extracts.

---

## USER_INPUT_REQUIRED

Blocks are **incomplete but valid** for early review. Flag as **not implementation-ready** until resolved.

---

## Validation report

Use the format in the original skill (Passed / Issues / Blocking / Approval status). Call out:

- Missing **📎** or **🎨 UI & design** sections
- PRD ids without lifted text
- Repeated copy across sections
- Placeholders: `[URL]`, `[name]`, `[date]` in UI section

---

## Triggers

Story grooming, pre–`sdlc story push`, QA handoff, sprint planning.
