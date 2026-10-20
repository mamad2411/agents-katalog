---
description:
globs:
alwaysApply: false
---
- **Documentation Must Track All Major Changes**
  - **Tech Stack:**
    - Update `docs/ARCHITECTURE_OVERVIEW.md` whenever a new library, framework, or tool is added, removed, or upgraded (e.g., React, Next.js, Tailwind, ShadCN, Chart.js, etc.).
    - Clearly document the reason for the change and its impact on the system.
  - **Component Inventory:**
    - Update `docs/ShadCN-context.md` whenever a new UI component (ShadCN or fallback) is added, removed, or significantly changed.
    - Include source, wrapper path, rationale, key props, and integration notes.
  - **Design System:**
    - Document any changes to the design system, color palette, or UI/UX patterns in `docs/ARCHITECTURE_OVERVIEW.md` and reference relevant files (e.g., Tailwind config, custom classes).
    - If a new design pattern or layout is introduced, add a section or update the relevant diagram.
  - **Project Structure:**
    - Regenerate `docs/PROJECT_STRUCTURE_TREE.md` after any structural change (new folders, major file moves, etc.).
  - **Agentic Workflow:**
    - If the agentic workflow or rules change (e.g., new agent, new automation), update the relevant sections and diagrams in `docs/ARCHITECTURE_OVERVIEW.md`.
  - **CI Enforcement:**
    - CI should fail if these docs are not updated when relevant code or config changes are detected.

- **Best Practices**
  - Use clear commit messages referencing the documentation update (e.g., `docs: update architecture overview for new charting library`).
  - Reference the updated documentation in PR descriptions for visibility.
  - Use Mermaid diagrams to visualize new architecture or workflow changes.

- **Onboarding & Contribution**
  - Reference this rule in onboarding and contribution docs.
  - Remind all contributors (human or AI) to update these docs as part of the development workflow.
