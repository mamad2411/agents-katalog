---
name: playbook-writer
description: Meta-skill that generates compliant PLAYBOOK.md files following the BRAINIAC template. Use when creating or editing modules in the command center. For general readme creation, see create-readme.
---

# Playbook Writer Skill

## When to Use
- When a directory has no PLAYBOOK.md or has generic boilerplate
- When rewriting existing playbooks to match `PLAYBOOK_TEMPLATE.md`
- When adding new modules to the command center

## Tools Required

| Tool | Purpose |
|------|---------|
| `view_file` | Read PLAYBOOK_TEMPLATE.md for format compliance |
| `write_to_file` | Create or overwrite the PLAYBOOK.md |
| `view_file` | Read adjacent playbooks for cross-references |

## Instructions

### 1. Read the Template
Always start by reading `BRAINIAC/PLAYBOOK_TEMPLATE.md` to ensure format compliance.

### 2. Gather Context
Before writing, determine:
- **Phase**: Which lifecycle phase (Idea, Validation, Planning, etc.)
- **Module**: The specific subdirectory (Problem Discovery, Market Research, etc.)
- **Phase Index**: The numbered prefix (0. Idea, 1. Validation, etc.)
- **Module Position**: Where this module sits in the phase sequence
- **APP_NAME**: The user's SaaS product name (from GEMINI.md or user input)

### 3. Determine Prerequisites
Scan the phase directory:
- List all sibling modules
- Check which modules logically precede this one
- Check cross-phase dependencies (e.g., Development depends on Planning)
- Read adjacent PLAYBOOK.md files for cross-reference links

### 4. Write Module-Specific Content

**CRITICAL RULES:**
- **NO BOILERPLATE.** Every section must contain content specific to THIS module.
- Action steps must name the specific tool, MCP, or agent to use.
- Vibe Coding Prompts must include `{PLACEHOLDERS}` for user-specific context.
- Success Criteria must be binary pass/fail — never subjective vibes.
- Deliverables must be concrete files, documents, or decisions.

**Anti-patterns to AVOID:**
```
BAD:  "Define the MVP for Frontend."
GOOD: "Create a component inventory listing every UI screen, with wireframe references from Design/Wireframes/."

BAD:  "Track the metrics."
GOOD: "Set up Posthog/Mixpanel tracking for: signup rate, activation rate, D7 retention. Export dashboard link to this directory as METRICS.md."

BAD:  "Generate a robust, production-ready implementation plan."
GOOD: "Using Next.js 15 App Router, scaffold the authenticated dashboard layout with sidebar navigation. Include: /dashboard, /settings, /billing routes. Use Supabase Auth for session management."
```

### 5. Validate Before Saving
Checklist before writing the file:
- [ ] Every section from PLAYBOOK_TEMPLATE.md is present
- [ ] Objective is exactly one sentence
- [ ] Deliverables are checkboxes with concrete outputs
- [ ] Prerequisites table references real modules with correct paths
- [ ] Action Steps each specify Tool/Agent, Input, Output
- [ ] Agent Context table lists actual MCPs, skills, and workflows
- [ ] Vibe Coding Prompts use {PLACEHOLDERS}
- [ ] Success Criteria are binary pass/fail
- [ ] Cross-References link to real adjacent playbook paths

### 6. Save
Write the file to `BRAINIAC/{Phase}/{Module}/PLAYBOOK.md`, overwriting any existing boilerplate.

## Quality Gates
- Zero generic sentences (grep for "ship fast", "no fluff", "pour gasoline" — these are boilerplate markers)
- Every action step maps to a tool or agent
- Cross-references resolve to existing files
