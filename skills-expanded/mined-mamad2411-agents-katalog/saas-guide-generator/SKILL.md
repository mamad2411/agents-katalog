---
name: saas-guide-generator
description: Researches feature code, captures live UI screenshots or mockups, and writes Markdown guides in /docs with step-by-step instructions, images in assets/, and Mermaid.js flows. Use when the user asks to create a guide, document a feature, or write feature documentation.
---

# SaaS Guide Generator

Produce user-facing or internal Markdown guides for a requested feature. Follow three phases: Research, Capture Visuals, then Write.

## When to Use This Skill

Trigger this skill when the user says they want to:
- **Create a guide** (e.g., "create a guide for the export flow")
- **Document a feature** (e.g., "document the sprite sheet export feature")
- **Write feature documentation** or similar phrasing

---

## Phase 1: Research

Use the codebase to locate the feature before writing or capturing UI.

1. **Identify scope**: Clarify which feature or flow to document (e.g., "sprite export", "auto-crop", "onboarding").
2. **Search the codebase**: Use semantic search and file navigation to find:
   - Entry points (pages, routes, main components)
   - Key components and hooks that implement the behavior
   - Any shared utilities or types used by the feature
3. **Map the flow**: Note the sequence of steps, decisions, and API or state interactions so you can describe them accurately and later draw Mermaid diagrams if needed.

---

## Phase 2: Capture Visuals

Get images to embed in the guide. Prefer live UI; fall back to generated mockups.

### Option A: Browser (preferred)

1. **Confirm dev server**: Ensure the app runs locally (e.g., `npm run dev`). Check terminals or start the server if needed.
2. **Navigate**: Use the browser tool to open the relevant URL (e.g., `http://localhost:3000`) and go to the feature (route, tab, or modal).
3. **Capture screenshots**: Take screenshots of each important screen or step in the flow.
4. **Save under assets**: Store images in `docs/assets/` (or a subfolder like `docs/assets/guides/<feature-name>/`) with clear filenames (e.g., `export-step-1.png`, `crop-preview.png`).

### Option B: Image generation (fallback)

If the browser tool is unavailable or the page cannot be loaded:

1. **Describe the UI from code**: Use component structure, copy, and layout from the codebase to describe the screen.
2. **Generate a mockup**: Use the built-in image generation to create a high-fidelity UI mockup that matches the described interface.
3. **Save to assets**: Save the generated image under `docs/assets/` with a descriptive name.

---

## Phase 3: Write the Guide

Generate a single Markdown guide in the project’s `docs/` directory.

### Output location and structure

- **Path**: `docs/<feature-or-guide-name>.md` (e.g., `docs/sprite-export-guide.md`). Use kebab-case.
- **Assets**: Reference images from `docs/assets/` (or `docs/assets/guides/<feature-name>/`). Use relative paths in Markdown (e.g., `![Step 1](./assets/export-step-1.png)`).

### Guide content

1. **Title and brief intro**: One short paragraph on what the guide covers and who it’s for.
2. **Prerequisites**: Any setup, accounts, or prior steps the user needs (if relevant).
3. **Step-by-step instructions**: Numbered steps. For each step:
   - One clear action or decision.
   - Reference to the matching screenshot/mockup when it helps.
   - Code snippets or CLI commands only if the guide is technical.
4. **Complex flows**: For multi-step or branching logic, add a Mermaid diagram (flowchart or sequence diagram) so readers can see the flow at a glance. Place it after the intro or before the steps.
5. **Troubleshooting (optional)**: Short section for common issues and fixes if you have that information from the codebase or context.

### Mermaid usage

- Use **flowchart** for step/decision flows (e.g., "Upload → Validate → Crop → Export").
- Use **sequenceDiagram** when documenting interactions between user, UI, and backend.
- Keep diagrams focused; avoid huge graphs. Use subgraphs or multiple small diagrams if needed.

### Example guide outline

```markdown
# [Feature Name] Guide

Brief description and audience.

## Prerequisites
- Item 1
- Item 2

## Overview (optional)
[Insert Mermaid flowchart or sequenceDiagram here]

## Step-by-step

### Step 1: [Action]
Description.  
![Step 1](./assets/guides/feature-name/step-1.png)

### Step 2: [Action]
...
```

---

## Checklist Before Finishing

- [ ] Research phase: Relevant files and flow are identified.
- [ ] Visuals: Screenshots or mockups saved under `docs/assets/` and referenced in the guide.
- [ ] Guide path: Written to `docs/<name>.md` with relative image paths.
- [ ] Steps: Numbered, clear, and aligned with the captured images.
- [ ] Complex logic: At least one Mermaid diagram where the flow is non-trivial.
- [ ] No broken image paths: All `./assets/...` or `assets/...` paths resolve from the guide file.
