---
name: sdd-ux
description: 'Create or update the shared UX design document — define user flows, create wireframe mockups, document interaction patterns, specify navigation and component inventory, and produce an HTML/CSS prototype. Use when defining UX flows, wireframes, or interaction design for the product. Do not use for architecture decisions, product requirements, or feature implementation.'
---

Create or update the shared UX design document at `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md`.
This is a **shared project document** — not tied to any specific change. It defines the UX foundations and serves as context for all future changes.

**Output**: `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` and `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prototype-[project-name].html`

**Template**: Use `assets/ux.md` and `assets/prototype-template.html` as the document structure.

**Prerequisites**: `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` should exist. If not, inform: "Create the PRD first with `/prd`."

> [!IMPORTANT]
> This skill is designed to be used with the **sdd-team:sdd-ux.agent** agent.
> Switch to it in the agent selector before invoking this skill for the full interactive experience.
> If you are already using **sdd-team:sdd-ux.agent**, proceed with the workflow below.

---

## Entry point

1. **Check if UX doc already exists**

   Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md`. If it exists:
   - Summarize current content to the user.
   - Ask: "Do you want to **revise** the existing UX design or **start fresh**?"  Skip this question if you detect from existing document or user input.
   - If revise → follow **Revise UX Workflow** below.
   - If fresh → follow **New Design Project Workflow** below.

2. **Context gathering** (always)

   - Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` — primary input (product vision, user journeys, requirements).
   - Read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` if it exists — technical constraints on the UI.
   - Ask the user for additional context if needed.

---

## New Design Project Workflow

Full guided UX design — 6 sequential sections that build the spec document, culminating in an HTML prototype.  
Use the PRD as primary input — do not re-discover what it already covers.

> **C/R/A protocol applies to every section:** present content, await user Confirmation, Revision request, or Abandon — never auto-advance without an explicit C.

### Section 1 — Project Vision

**Purpose:** Understand what we're designing, for whom, and why. Synthesize from PRD — ask only about UX-specific gaps.

**Ask about:**
1. Platform/devices? (web desktop, mobile web, cross-platform, specific breakpoints)
2. Any brand, style, or existing design system constraints?
3. What does "success" look like for a first prototype?

After the user answers: synthesize a **Project Vision** section combining PRD context + UX answers. Present and await C/R/A before advancing.

---

### Section 2 — Design Decisions Workshop

**Purpose:** Surface and resolve key design choices *before* building. This is where rework gets prevented.

> Before we touch layouts or code, let's nail the big decisions. I'll name the design choices that matter most for your project, share my recommendation for each with rationale, then you tell me where you agree, disagree, or want to explore alternatives.

**Identify 4–6 relevant decisions:**

| Decision | Options to present |
|---|---|
| Navigation pattern | Top bar / Side nav / Bottom tabs / Hamburger |
| Content density | Spacious (cards, whitespace) / Compact (tables, lists) / Mixed |
| Primary action placement | Floating action button / Top-right / Bottom bar / Contextual inline |
| Information hierarchy | Single-focus views / Dashboard overview / Progressive disclosure |
| Color approach | Neutral + accent / Brand-first / Dark mode default / System-aware |
| Form interaction | Modal / Side panel / Inline / Separate page |
| Feedback & states | Toast notifications / Inline validation / Status banners |

For each: name it, state recommendation with 1-sentence rationale, list 1-2 alternatives. Build a **Decisions Log**. Present and await C/R/A when all decisions are resolved.

---

### Section 3 — Component Inventory

**Purpose:** Define the reusable UI building blocks based on vision and decisions.

Draft a component inventory in table format:

| Component | Variants | Notes |
|---|---|---|
| Button | Primary, Secondary, Destructive, Icon-only | |
| Input | Text, Search, Textarea | |
| Card | Default, Highlighted, Compact | |
| Navigation | *(based on decision)* | |
| *(etc.)* | | |

Include 8–15 components appropriate to the project. Add 1-line notes for anything non-standard.

Present component inventory and await C/R/A.

---

### Section 4 — Key Screen Wireframes

**Purpose:** Sketch the 2–3 most important screens in text wireframe format before coding.

For each screen, produce a **text wireframe** using ASCII characters and clear labels:

```
┌─────────────────────────────────────────┐
│  HEADER: Logo + Nav + User Avatar        │
├─────────────────────────────────────────┤
│  PAGE TITLE                             │
│  Subtitle / breadcrumb                  │
├──────────┬──────────────────────────────┤
│ SIDEBAR  │  CONTENT AREA                │
│          │  ┌──────────┐ ┌──────────┐   │
│ [Nav 1]  │  │  Card 1  │ │  Card 2  │   │
│ [Nav 2]  │  └──────────┘ └──────────┘   │
│ [Nav 3]  │                              │
└──────────┴──────────────────────────────┘
```

Label every zone. Add brief annotation bullets below each wireframe (max 3 bullets per screen).

Present wireframes and await C/R/A.

---

### Section 5 — Prototype Specification

**Purpose:** Define the technical requirements for the HTML prototype before writing code.

Draft the prototype spec:

```
PROTOTYPE SPECIFICATION
━━━━━━━━━━━━━━━━━━━━━━

Screens included:     [list the screens to include]
Interactions:         [list clickable elements and what happens]
NOT included:         [list what's out of scope — back-end, auth, etc.]
Breakpoints:          [e.g., desktop 1200px, tablet 768px, mobile 375px]
Design tokens:        [color palette hex codes, font sizes, spacing scale]
Browser target:       Modern browsers (Chrome, Firefox, Safari, Edge)
Accessibility:        ARIA labels, semantic HTML, keyboard navigation for nav
```

Ask: "Anything to add or remove from this scope?" Present and await C/R/A.

---

### Section 6 — HTML/CSS Prototype

**Purpose:** Generate the working, standalone HTML prototype.

Start from the official template at `assets/prototype-template.html`. Read that file first — it contains base design tokens, reset, layout utilities, and component styles. Extend and customise it; never start from a blank file.

**HTML rules:**
- `<!DOCTYPE html>` with proper `<head>` (charset, viewport, title)
- Semantic HTML5 elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- ARIA labels on interactive elements
- All styles embedded in `<style>` — no external CSS files
- All interactivity embedded in `<script>` — no external JS
- Dummy content that resembles real data (not "Lorem ipsum" for UI labels)

**CSS rules:**
- CSS custom properties at `:root` for colors, spacing, fonts
- Mobile-first responsive using `@media` breakpoints
- Flexbox or CSS Grid — no floats
- Hover, focus, and active states on interactive elements

**JavaScript rules:**
- Only for interactions specified in the prototype spec
- Vanilla JS only — no frameworks
- Comment every function

Deliver the complete HTML as a single fenced code block. After the code block, list key interactions implemented.

Save as `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prototype-[project-name].html`.

Present and await C/R/A.

---

### Section 7 — Completion

Display a summary:

```
✅ Project Vision        — Goals, users, platform targets
✅ Design Decisions      — [n] key decisions resolved
✅ Component Inventory   — [n] components defined
✅ Screen Wireframes     — [n] screens sketched
✅ Prototype Spec        — Scope and tokens defined
✅ HTML Prototype        — Working prototype built
```

- Confirm: "UX design saved to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md`"
- Suggest: "You can now create the architecture (`/sdd-arch`) or start a change (`/sdd-propose`)."

---

## Revise UX Workflow

Structured improvement of an existing UX document.

### Step 1 — Discovery

1. Load `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` completely.
2. Ask: *"What would you like to change?"* Examples:
   - Revisit a design decision (navigation, color, density)
   - Add or remove components from the inventory
   - Update wireframes for new screens
   - Regenerate or update the HTML prototype
   - Incorporate new requirements from an updated PRD
3. If user provides updated spec files (PRD, architecture), load them to understand the delta.

### Step 2 — Impact analysis

1. Identify which sections are affected by the requested change.
2. Present a brief change plan: sections to update, order, ripple effects.
3. Get user approval before proceeding.

### Step 3 — Apply edits

1. Work through sections in the approved order.
2. For each section: present revised content → C/R/A.
3. Ensure consistency across sections (e.g., component inventory reflects wireframe changes).

### Step 4 — Completion

1. Apply all edits to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` (and `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prototype-[project-name].html` if the prototype changed).
2. Present a **completion recap**: sections modified, decisions changed.

---

## Tracker Update

After saving UX artifacts, follow the **`sdd-tracker` skill** — update `shared.ux.ux` and/or `shared.ux.prototype` (only those actually written this session) and add a changelog entry "UX design updated on YYYY-MM-DD" with a summary of what was changed.

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Adopt the UX Designer agent's persona** — from: `agents/ux-designer.agent.md`
- **Questions first, output second** — understand before generating.
- **C/R/A protocol** at every section — NEVER auto-advance without explicit C.
- Use the PRD as primary input — Do not re-ask what it already covers.
- Semantic and accessible HTML in all prototype output.
