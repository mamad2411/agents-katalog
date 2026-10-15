---
name: codebase-knowledge-builder
description: Deep-dive into any codebase and produce structured knowledge artifacts that turn a coding agent into a codebase specialist. This skill should be used when the user asks to "study this repo", "understand this codebase", "document this project", "onboard me onto this code", "create codebase knowledge", "map this architecture", or when asked to produce knowledge artifacts for any agent working on an unfamiliar repository.
version: 1.0.0
---

# Codebase Knowledge Builder

Transform from a generalist into a codebase specialist by systematically studying a repository and producing high-quality knowledge artifacts. The process follows a strict "read first, write later" principle across four sequential phases.

## Prerequisites

- File read access to the target repository (cloned locally or accessible via tools)
- Bash access for file counting and structure discovery
- Write access to produce scratch files and final artifacts

## Workflow

1. **Reconnaissance** -- Build a broad mental model of the entire repo
2. **Deep-Dive Study** -- Investigate each requested topic in isolation
3. **Artifact Authoring** -- Synthesize findings into polished knowledge artifacts
4. **Delivery** -- Package and deliver artifacts to the user

---

### Phase 1: Reconnaissance

Clone the repo and build a high-level map before touching any specific topic.

1. Run `find . -type f -name '*.js' -o -name '*.ts' -o -name '*.py' | head -50` and `wc -l` to gauge scale.
2. Read the main entry point file end-to-end.
3. Follow the checklist in `references/recon-checklist.md` to systematically discover architecture, entry points, config systems, and key abstractions.
4. Save a structured summary to a scratch file (`recon_findings.md`) with: tech stack, directory map, module responsibilities, design patterns, and open questions.

**Do not proceed to Phase 2 until the repo's architecture can be described in one paragraph.**

### Phase 2: Deep-Dive Study

For each topic the user requests, perform a focused investigation. Study each topic **separately** -- do not mix concerns.

1. Read `references/deep-dive-methodology.md` for file reading strategies, tracing patterns, and note-taking protocol.
2. Start from the subsystem's entry point and follow imports outward (dependency order, not alphabetical).
3. Trace three paths per subsystem: **happy path**, **error path**, **edge cases**.
4. After every 2-3 files, save key findings to a scratch file. Do not rely on context memory alone.
5. For each file, capture: purpose (one sentence), key functions, what it calls, what calls it, and gotchas.

### Phase 3: Artifact Authoring

Synthesize each topic's findings into a standalone knowledge artifact.

1. Copy the template from `templates/knowledge_artifact.md` for each topic.
2. Fill **every section** -- Overview, Architecture, Key Components table, Data & Control Flow, Key Functions table, Configuration table, Gotchas, Extension Points, and Visual Flow diagram.
3. Include Mermaid diagrams: use `sequenceDiagram` for flows, `graph TD` for architecture.
4. Each artifact must be self-contained -- a developer reading only that artifact should understand the subsystem completely.

### Phase 4: Delivery

Attach all completed Markdown artifacts to a message to the user. Include a brief summary of what each artifact covers.

---

## Limitations

- Large monorepos (>10,000 files) may require scoping to specific directories or packages before starting reconnaissance.
- Binary files, compiled assets, and vendored dependencies should be excluded from study.
- Knowledge artifacts reflect the codebase at a point in time. Major refactors may invalidate sections.

## Quality Checklist

Before delivering any artifact, verify:

| Check | Criteria |
| :--- | :--- |
| **Completeness** | Every template section is filled with codebase-specific detail, not placeholders. |
| **Accuracy** | File paths, function names, and parameter descriptions match the actual code. |
| **Gotchas** | At least 2-3 non-obvious behaviors, historical fixes, or race conditions documented. |
| **Visuals** | At least one Mermaid diagram per artifact. |
| **Self-contained** | A reader with no prior context can understand the subsystem from the artifact alone. |

## Bundled Resources

| Resource | Path | When to Read |
| :--- | :--- | :--- |
| Recon Checklist | `references/recon-checklist.md` | At the start of Phase 1 |
| Deep-Dive Methodology | `references/deep-dive-methodology.md` | At the start of each Phase 2 topic |
| Artifact Template | `templates/knowledge_artifact.md` | At the start of Phase 3 for each topic |
