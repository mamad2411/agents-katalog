---
name: product-prd
description: "Generate or update a project-level Product Requirements Document (PRD.md) after the user and AI have already discussed requirements, target users, product goals, implementation approach, workflow, and key technical decisions. Focuses on product overview, vision, core objectives, user personas, high-level feature groups, tech stack, system architecture key components, and phased roadmap / future work. Use when the user asks to create a PRD, write a product PRD, document project requirements, summarize the whole project direction, or produce a global project context file for future AI implementation work. Do not use for single-feature specs, acceptance criteria, detailed technical design, or implementation tasks."
---

# Product PRD Generator

Generate a project-level Product Requirements Document that captures the whole product direction and shared context for future implementation work. This PRD is a PM-facing project context file, not a feature spec and not a technical design document.

**Output location:** Project root as `PRD.md`

---

## Resources

- **Template:** [templates/PRD.md](templates/PRD.md) — the PRD structure to fill in
- **Example:** [examples/PRD.md](examples/PRD.md) — a complete filled-in reference

Read `templates/PRD.md` before generating output to use the exact format.

---

## The Job

1. **Synthesize** what the user and AI have already discussed across requirements, audience, scope, workflow, implementation approach, and key decisions
2. **Clarify** only critical gaps that would materially change the project-level PRD
3. **Generate** the PRD using `templates/PRD.md` as the exact format
4. **Save** to `PRD.md` at the project root

---

## Step 1: Gap Analysis

The user will typically invoke this skill after discussing the project in detail. Treat the existing conversation and repository context as the primary source of truth. Do not restart discovery unless critical information is missing.

1. Read what the user has already shared
2. Map the discussion against the PRD sections
3. Identify which dimensions are unclear or missing:
   - **Overview & vision** — what the project is, who it serves, and what outcome it enables
   - **Objectives** — what the project is trying to accomplish at a measurable product level
   - **Audience** — primary user groups and their goals / pain points
   - **Feature groups** — major product capabilities, not detailed specs
   - **Tech stack** — platform, frameworks, important packages, database, infrastructure, auth, and integrations already decided or clearly implied
   - **Architecture components** — high-level system building blocks and cross-cutting services already decided or clearly implied
   - **Roadmap** — completed phases, the current phase, one consolidated Future Work phase, and explicit exclusions
4. Ask only the 1–3 most critical questions that are genuinely unresolved

If the conversation already contains enough context, proceed directly to writing the PRD. Do not ask a fixed questionnaire.

**Key principle:** This skill documents the project after planning discussion has already happened. It should consolidate decisions and assumptions, not reopen broad product discovery.

---

## Step 2: Generate the PRD

Once you have enough context, generate the PRD following the structure in `templates/PRD.md`.

Guidelines:
- **Project Overview (Section 1):** Include the product vision as one bullet inside the overview. Do not create a separate Product Vision section.
- **Core Objectives (Section 2):** Use plain bullet points, not TODO checkboxes. Objectives should be concrete and product-level.
- **User Personas (Section 3):** Keep personas focused on goals and pain points. Avoid implementation needs.
- **Feature Groups (Section 4):** Use high-level capability groups only. No acceptance criteria and no implementation detail.
- **Tech Stack (Section 5):** List the agreed platform, frameworks, important packages, data stores, infrastructure, auth, and external integrations. Include important libraries such as UI kits, ORM/data access, auth packages, validation/form libraries, job queues, and analytics when they are part of the project direction. If something is undecided, write `TBD`.
- **System Architecture Overview (Section 6):** Describe key system components and their responsibilities at a high level, such as frontend app, API layer, database, message queue, cache, logging, monitoring, background workers, search, storage, authentication, or external integration layer. Do not list feature-specific modules unless they are genuine architecture components.
- **Phased Roadmap (Section 7):** Mark exactly one current phase in the table. Include prior phases when useful to show how requirements evolved. Version-style phase names such as `v0.1`, `v0.2`, or `v1.0` are acceptable when they reflect the project plan. Use a single `Future Work` phase that consolidates all later goals; do not split future work into multiple named future phases.
- **Out of Scope:** Do not create a separate section. Put exclusions or deferred work into the roadmap table as Future Work / Out of Scope notes.
- **Omit:** Do not include Success Metrics or Open Questions sections.
- **Technical detail:** Capture only agreed stack and high-level architecture context needed for future AI work. Do not discuss low-level implementation details, compare technologies, or introduce new technical recommendations.
- **Language:** Write the PRD in English to match the template.

---

## Step 3: Save

Save to `PRD.md` at the **project root** (not in `docs/` or any subdirectory).

---

## Quality Checklist

Before saving:

- Read `templates/PRD.md` and followed the exact format
- Used existing conversation and repo context before asking questions
- Asked only critical gap questions, if any
- Project vision appears inside Project Overview
- Core objectives use bullet points, not TODO checkboxes
- Feature groups are high-level — no acceptance criteria
- Tech Stack section lists agreed technology choices and important packages separately from architecture
- Architecture section lists key system components, not feature-specific services
- Roadmap marks exactly one current phase
- Roadmap uses one consolidated Future Work phase for all later goals
- Version-style roadmap labels are used only for concrete completed/current phases, not to split Future Work
- No separate Out of Scope, Success Metrics, or Open Questions sections
- Saved to `PRD.md` at project root
