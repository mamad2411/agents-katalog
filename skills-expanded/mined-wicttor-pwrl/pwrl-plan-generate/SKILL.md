---
name: pwrl-plan-generate
description: "Choose tier, render plan from templates, embed learnings, and save to docs/plans/."
argument-hint: "[scoped context + research findings + implementation units]"
---

# pwrl-plan-generate — Plan Generation

**Purpose:** Final output step in the planning workflow. Accepts scoped context, research findings, and implementation units from upstream skills (S2→S3→S4). Selects the appropriate tier (Fast/Standard/Deep), renders the plan from the templates reference file, embeds related learnings, and saves it to `docs/plans/`.

## Interaction Method

- Use the platform's `ask_user_question` extension for confirmations and overrides.
- Present tier selection and plan preview before saving.
- Ask one question at a time. Use multiple-choice for tier override.

## Input

This skill expects three inputs:

1. **Scoped context** from `pwrl-plan-scope` (S2) — problem, criteria, domain, learnings
2. **Research findings** from `pwrl-plan-research` (S3) — patterns, risk, constraints
3. **Implementation units** from `pwrl-plan-design` (S4) — U-IDs, files, approach, criteria

If inputs are missing, search for recent scope/research/design files or prompt the user to run prerequisite skills first.

## Output: Plan File

After completing the workflow, a plan file is saved to `docs/plans/YYYY-MM-DD-NNN-<kebab-case-name>.md`. The function returns: `{ file_path: "docs/plans/...md", tier: "Fast", summary: "..." }`. For detailed schema documentation, file structure, frontmatter specification, content requirements per tier, storage conventions, and versioning rules, see **[state-schema.md](references/state-schema.md)**.

## Workflow

### Step 1: Tier Selection

1. Read the complexity hint from S4's output and the research findings.
2. Apply the heuristic to determine initial tier:

   | Unit Count | Risk Level         | Initial Tier |
   | ---------- | ------------------ | ------------ |
   | 1-3        | LOW                | Fast         |
   | 1-3        | MEDIUM or HIGH     | Standard     |
   | 4-8        | any                | Standard     |
   | 9+         | any                | Deep         |
   | any        | 2+ high-risk areas | Deep         |

3. Present to user: "Based on [N] units and [risk] risk level, the recommended tier is **[Tier]**. Would you like to use this tier or choose a different one?"
   - Options: Accept [Tier], Select Fast, Select Standard, Select Deep
4. Apply user's choice.
5. Document the tier selection rationale in the plan.

### Step 2: Load Template

1. Read the appropriate template from `pwrl-plan/references/plan-templates.md`.
2. Select the template section matching the chosen tier (Fast, Standard, or Deep).
3. If the template cannot be loaded, fall back to the inline template definitions in this skill.

### Step 3: Render Plan Sections

Use the loaded template to populate each section based on the chosen tier. For detailed rendering logic, section requirements per tier (Fast/Standard/Deep), template structure, and examples, see **[render-workflow.md](references/render-workflow.md)**.

### Step 4: Embed Learnings

1. From S2's `Related Learnings` list, add to the plan:

   ```
   ## Related Learnings

   - **[Learning Title]** — `docs/learnings/XXX.md` — [1-line applicability note]
   ```

2. From S2's `Learning Gaps` list, add to the plan:

   ```
   ## Learning Gaps

   - **[Gap Name]** — *Action:* Document via `/pwrl-learnings` after implementation
   ```

3. If no learnings or gaps exist, still include the sections:
   - "No relevant learnings found"
   - "No learning gaps identified at this time"

### Step 5: Generate Filename

1. Format: `docs/plans/YYYY-MM-DD-NNN-<kebab-case-name>.md`
2. Components:
   - **Date:** Today's date in YYYY-MM-DD format
   - **NNN:** Sequential 3-digit number (001, 002, 003...)
   - **Name:** Kebab-case slug from the plan title
3. Avoid collisions:
   - Read `docs/plans/` directory
   - Find the highest existing NNN for today's date
   - Increment: new NNN = max NNN + 1
   - Example: if `2026-06-05-001-...` exists, next is `2026-06-05-002-...`

### Step 6: Validate Plan

Before saving, validate:

- [ ] Frontmatter: id, status, tier, created, updated are present and valid
- [ ] All required sections present for the chosen tier (see Required Sections Per Tier in plan-templates.md)
- [ ] All file paths are repository-relative (no /home/user/... paths)
- [ ] Related Learnings section exists (even if empty)
- [ ] Learning Gaps section exists (even if empty)
- [ ] No empty placeholders remain (e.g., `{{GOAL}}` or `[placeholder]`)
- [ ] Plan is valid markdown (can be read without parse errors)

### Step 7: Confirm and Save

1. Present the plan preview to the user via `ask_user_question`:
   - Show: tier selected, filename, first 500 characters of the plan
2. Ask: "Shall I save this plan to `[filename]`?"
   - Options: Yes, Edit (iterate on sections), Cancel
3. If Yes: Write the file and confirm.
4. If Edit: Iterate on specific sections the user wants changed.
5. If Cancel: Discard and exit.
6. Return the file path and a brief summary.

## Edge Cases

Seven edge cases commonly encountered during generation: template loading failure, filename collisions, tier override after preview, minimal research findings, unit count/complexity mismatch, empty complex sections, and multiple plans with same date/title. For handling strategies, decision trees, and examples, see **[edge-cases.md](references/edge-cases.md)**.

## References

- **Templates:** `pwrl-plan/references/plan-templates.md` (created by S1)
- **Tier Heuristic:** `pwrl-plan-generate/references/tier-heuristic.md`
- **Input:** Scoped context (S2) + Research findings (S3) + Units (S4)
- **Output:** `docs/plans/YYYY-MM-DD-NNN-<name>.md`
- **Learnings:** `docs/learnings/INDEX.md` for embedding

```

```
