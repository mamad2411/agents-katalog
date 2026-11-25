---
name: project-docs-prep
description: Use this skill whenever the user wants to prepare or scaffold documentation for a new (or existing) software project before handing it to an AI coding agent — for example when they ask to "set up project docs", "write a project spec", "prepare AGENTS.md", "prepare DESIGN.md", "เตรียมเอกสารโปรเจกต์", "เริ่มโปรเจกต์ใหม่ให้ AI เขียนโค้ด", or describe a project idea and want it turned into proper docs. Also trigger when the user wants a full docs/ folder (numbered specs — project overview, system requirements, tech stack & architecture, system modeling, UX/UI design) plus root-level agent-facing files (AGENTS.md, DESIGN.md, CLAUDE.md, README.md). Trigger even if the user only gives an informal one-line project idea and doesn't name any file explicitly — this skill's job is to turn that idea into the full documentation set. Also use when the user wants to review or upgrade an existing project's docs to be "AI-agent ready".
---

# Project Docs Prep

Turns a short project idea (or an existing incomplete docs folder) into a complete, AI-agent-ready documentation set. Produces two operational layers:

1. **Spec Layer** (`docs/`) — describes *what* to build. Five numbered files:
   - `01-project-overview.md`
   - `02-system-requirements.md`
   - `03-tech-stack-architecture.md`
   - `04-system-modeling.md`
   - `05-ux-ui-design.md`
2. **Operational Layer** (repo root) — describes *how the agent should work* and *what design tokens/commands look like*:
   - `AGENTS.md`
   - `DESIGN.md`
   - `CLAUDE.md`
   - `README.md`

These two layers are complementary, not redundant. The spec layer is read once during planning. The operational layer is loaded by the agent every session — keep it concise and omit facts inferable from code.

## Templates

This skill ships with skeleton templates in `templates/`. When generating docs for a new project:

1. Read the relevant template from `templates/` as your starting structure.
2. Replace all `{{PLACEHOLDER}}` markers with project-specific content.
3. Delete any sections that don't apply — do NOT leave empty headings.
4. Add project-specific sections where the template doesn't cover them.

See `references/template-usage-guide.md` for detailed instructions on each template.

---

## Workflow

### Step 1 — Gather Project Info
If given a short idea (e.g. "Meeting room booking system for 50 users"), do not interrogate field-by-field. Draft reasonable content and mark uncertain items with `> ⚠️ TODO:`. Only ask clarifying questions when the answer would alter architecture or design direction.

### Step 2 — Generate `docs/01`–`05`
Create numbered specs in `docs/`. Use the templates in `templates/docs/` as starting structure. Maintain consistent section headings. Fill placeholders with project specifics. Keep descriptions clear and accessible for both human developers and AI agents.

### Step 3 — Generate `AGENTS.md`
Use `templates/AGENTS.md` as base. Include build, test, and lint commands for the chosen stack, directory layout, and hard constraints. Delete non-applicable template sections to conserve token budget.

### Step 4 — Generate `DESIGN.md`
Use `templates/DESIGN.md` as base. Create a design specification with:
- YAML front matter containing design tokens (colors, typography, spacing, breakpoints, z-index).
- Markdown body detailing design rationale, accessibility, and component standards.

**Hard Rule — NO Emoji in UI-facing files.**
`docs/05-ux-ui-design.md` and `DESIGN.md` must **never** contain emoji as UI elements (status markers, buttons, icons, flags). Always specify an icon library (e.g. Lucide Icons) or named inline SVGs, referencing icons by name (e.g. `CheckCircle` icon or `<i data-lucide="check-circle"></i>`).

### Step 5 — Generate `CLAUDE.md` and `README.md`
- `CLAUDE.md`: thin pointer file linking to `AGENTS.md` and `DESIGN.md` plus Claude Code notes. Use `templates/CLAUDE.md`.
- `README.md`: concise human-facing summary condensed from `01-project-overview.md`. Use `templates/README.md`.

### Step 6 — Assemble and Deliver
Deliver the full file tree:

```text
/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── DESIGN.md
└── docs/
    ├── 01-project-overview.md
    ├── 02-system-requirements.md
    ├── 03-tech-stack-architecture.md
    ├── 04-system-modeling.md
    └── 05-ux-ui-design.md
```

---

## Guardrails

1. **No Emoji in `docs/05-ux-ui-design.md` or `DESIGN.md`, ever.** Use Lucide Icons or named SVGs instead.
2. **Token Efficiency:** Keep `AGENTS.md`, `DESIGN.md`, and `docs/` high-density and free of generic fluff.
3. **No Fabricated Performance Figures:** Use `> ⚠️ TODO: confirm target NFR` for unconfirmed metrics.
4. **Language Strategy:** Keep operational files (`AGENTS.md`, `DESIGN.md`, `CLAUDE.md`) in English for optimal LLM token efficiency.
