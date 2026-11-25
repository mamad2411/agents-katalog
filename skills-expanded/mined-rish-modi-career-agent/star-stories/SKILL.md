---
name: star-stories
description: Extract projects from career docs (or user-pasted text) and convert each into a STAR-format Markdown file. One file per project, multiple STAR angles per file (technical, leadership, ambiguity, conflict, etc.). Output goes to $PERSONAL/career/star/. Use when the user says "STARify", "build STAR stories", "convert my projects to STAR", or asks to extract a single project to STAR.
---

# STAR Stories

## When to use
- User says "STARify", "STARify my resume", "STARify [project name]", "build STAR stories"
- User wants to convert career-doc project entries into structured behavioral-interview ammo
- User pastes a project description and wants it formatted in STAR
- Before a hiring-manager or behavioral round, when the user needs ready-to-deliver project narratives

For mock interviews or curating which stories to lead with for a specific role, use `interview-prep`. STARify produces the raw material; `interview-prep` selects and rehearses it.

After STARifying a project (or batch of projects), suggest the user run `/interview-prep` in audit mode to refresh the competency index, or in cheat-sheet mode if there's an upcoming round the new stories should feed.

## Inputs

`$PERSONAL` is the personal-docs sibling directory defined in `CLAUDE.md`. Resolve it once at the start of the session.

**Source documents** (read all that exist):
- `$PERSONAL/career/impact-doc.md` — primary source. Has roles, projects, scope, metrics.
- `$PERSONAL/career/brag-doc.md` — wins and recognition. Cross-check metrics; brag doc often has sharper numbers.
- `$PERSONAL/career/rish-career.md` — narrative framing. Use to recover the *why* and the *struggle* behind a project, which often gets compressed out of impact-doc bullets.

**Or:** user-pasted project text. If the user pastes a single project description, skip the file reads and STARify the paste directly.

## Modes

### Mode 1: STARify the full portfolio
Triggered by: "STARify my resume", "build STAR stories for everything", "go through all my projects".

1. Read the three source docs.
2. Extract a deduped list of distinct projects. A "project" is a named piece of work with a beginning, a personal contribution, and an outcome (e.g., "Agentic Dev Team", "Bill's Design System MCP", "OPEX Notebook"). Not roles. Not skills. Not multi-year team initiatives that aren't yours.
3. **Present the list to the user before writing.** Confirm the slug for each, ask which to skip, ask whether to merge any.
4. For each confirmed project, write `$PERSONAL/career/star/<slug>.md` using the template below.

### Mode 2: STARify a single project
Triggered by: "STARify [project name]", or user pastes one project's worth of detail.

1. Skip the list-and-confirm step.
2. Pull whatever context exists about that project across the source docs (or just use the pasted text).
3. Write `$PERSONAL/career/star/<slug>.md`.

### Mode 3: Update / refine an existing STAR file
Triggered by: "tighten the Agentic Dev Team story", "add a conflict angle to OPEX", "the metric is wrong in trinity-mcp.md".

1. Read the existing file.
2. Apply the requested edit.
3. Preserve other angles in the file unless the user says to drop them.

## File format

One file per project. Each file contains:
1. **Frontmatter** with project metadata.
2. **Context block** (2-3 sentences, role-agnostic background a reader needs).
3. **Multiple STAR angles**, each tagged with the competencies it lands.

```markdown
---
slug: agentic-dev-team
project: Agentic Dev Team
company: Bill
years: 2025-2026
scope: 10-agent SDLC pipeline, adopted across multiple teams
primary_competencies: [leadership, ambiguity, technical-depth, leverage]
---

# Agentic Dev Team

## Context
(2-3 sentences. What was the system, what team, what was the state of the world when you started. Reader should be able to evaluate the rest without back-and-forth.)

---

## Angle 1: Leadership / influence without authority
**Best for:** "Tell me about a time you drove a change without formal authority."

- **Situation:** ...
- **Task:** ...
- **Action:** ...
- **Result:** ...

## Angle 2: Ambiguity
**Best for:** "Describe a time you had to define the problem before solving it."

- **Situation:** ...
- **Task:** ...
- **Action:** ...
- **Result:** ...

## Angle 3: Technical depth / architecture
**Best for:** "Walk me through a technically complex system you designed."

- **Situation:** ...
- **Task:** ...
- **Action:** ...
- **Result:** ...

(Add more angles as the project supports them. A strong project supports 3-5 angles. Don't pad.)

---

## Quick-fire facts (for follow-ups)
- One-line scope:
- Key metrics:
- Who else was involved:
- What I'd do differently:
- Why this matters now:
```

## Workflow rules

- **Write in first person, past tense.** "I built", not "we built" unless the action genuinely was a we. Surface the user's specific contribution.
- **Action should be decision-driven, not task-driven.** "I chose multi-agent over a single God-Agent because X" beats "I implemented an orchestrator class." Interviews reward judgment, not labor.
- **Result must be quantified.** Pull numbers from impact-doc / brag-doc. If a project's result is unquantified in the source files, flag it: `**RESULT-NEEDS-METRIC:** ...` and ask the user inline.
- **Don't invent.** If a detail isn't in the source material, write `[VERIFY]` and ask. Never fabricate scope, names, or numbers.
- **Cross-reference, don't duplicate.** If the OPEX story shares a competency with Agentic Dev Team, both files keep the angle but each frames it through its own project.
- **Push back on weak angles.** If a project doesn't actually support a "conflict" angle, don't force one. Note it: `## Angle X: Conflict — N/A for this project, see [other-project].md instead`.
- **Slug rules:** lowercase, kebab-case, short. Match how the project is referenced in impact-doc when possible.

## Output discipline

- Files: `$PERSONAL/career/star/<slug>.md`. Create the directory if missing.
- If a file already exists, prompt: **Overwrite** (replace entirely), **Merge** (add new angles, preserve existing), or **Cancel** (print to terminal only).
- After writing, summarize: which files were created/updated, which angles are weakest and would benefit from a verification pass, and any `[VERIFY]` or `RESULT-NEEDS-METRIC` flags the user needs to resolve.

## Anti-patterns

- Don't write a STAR file for a role (e.g., "Senior Engineer at Bill"). STARify projects, not job titles.
- Don't pad an angle if the project doesn't earn it. Three sharp angles beats five wishy-washy ones.
- Don't lead the Action with the technology choice. Lead with the decision/judgment, then explain what enabled it.
- Don't write a Result without a number unless the source material genuinely lacks one (then flag, don't fabricate).
- **Never use em or en dashes (— –) in the output.** Use commas, periods, colons, or parentheses.
- Don't bury the metric at the end of a long paragraph. Result section should land the number in the first sentence.
