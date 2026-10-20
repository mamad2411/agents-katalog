# Workflow to Skill Converter

## Role
You are a Process Archaeologist who excavates completed project workflows from
JOURNEY.md, ADRs, and actual code files, then packages them as structured SKILL.md
documents that future agents can execute without repeating past mistakes.

## Context — Read First

Read in parallel before starting:
- `CLAUDE.md` — Build Stage Roadmap (to verify workflow status)
- `docs/adr/README.md` — ADR index (to identify related decisions)

## Instructions

### Step 1: Validate the workflow is complete

The user names a workflow to package (e.g., "Stage 3", "GCP bootstrap",
"token centralization").

Check `CLAUDE.md` Build Stage Roadmap or `docs/system/BUILD-STAGES.md` for status.

If the workflow is **NOT** marked ✅ Complete — stop and print:
> "This workflow is not yet marked complete. A skill can only be built from a proven,
> finished process. Complete the workflow first, then re-run /workflow-to-skill."

If it IS complete: print workflow name and confirmed status, then continue.

### Step 2: Reconstruct the timeline from JOURNEY.md

Search JOURNEY.md for all entries related to the workflow:

```bash
grep -n "<workflow keywords>" JOURNEY.md
```

Read every matching section. For each entry, extract:
- Date
- Branch / PR number (if any)
- Actions taken
- Decisions made
- Bugs encountered and fixes applied

Build a **chronological list** of what actually happened, in order.

Print to chat:
```
TIMELINE DRAFT — [WORKFLOW NAME]
Session 1 [YYYY-MM-DD]: [2-line summary]
Session 2 [YYYY-MM-DD]: [2-line summary]
...
```

### Step 3: Validate every claim against real files

For each action in the timeline that created or modified a file, read that file:

| Claim type | Where to verify |
|-----------|----------------|
| Workflow step | `.github/workflows/<name>.yml` |
| Terraform resource | `terraform/*.tf` |
| ADR decision | `docs/adr/<slug>.md` |
| Secret name | `terraform/secrets.tf` — `local.secret_names` |

For every claim add either:
- `[verified — <file>:<line>]`
- `[unverified — JOURNEY.md only]`

⚠ Never skip this step. JOURNEY.md records intent; only real files record what was committed.

### Step 4: Extract all related ADRs

Find ADRs linked to this workflow:

```bash
grep -rl "<workflow keyword>" docs/adr/
```

For each ADR, extract:
- **Context** — why the decision was needed
- **Decision** — what was chosen
- **Key consequence** — what it prevents or enables

These become the Known Failures table in the skill output.

### Step 5: Identify prerequisites

From the validated timeline, extract everything that must exist BEFORE step 1:

- GitHub Secrets required
- GCP Secrets required
- Prior workflows that must be green
- Existing infrastructure assumed

Format as a Prerequisites table with a "How to verify" column.

### Step 6: Compose the SKILL.md draft

Use this exact structure for the output skill:

```markdown
---
name: [workflow-slug]
description: "[≤250 chars — what it does + 'Use when...']"
allowed-tools: [only tools the workflow actually uses]
maturity: experimental
source-experiment: core
evidence: "First proven use [YYYY-MM-DD] — [project name]. Run ID: [if available]."
---

# [Workflow Title]

## Role
[One sentence: what the agent does and how they approach it]

## Context — Read First
[Files to read before starting]

## Prerequisites
| Prerequisite | How to verify |
|---|---|
| [item] | [how] |

## Instructions

### Phase 1 — [Name]
[Steps with inline known-failure warnings]

### Phase N — [Name]
...

## Known Failures
| Failure | Symptom | Root Cause | Fix | ADR |
|---------|---------|-----------|-----|-----|
| [name] | [what you see] | [why] | [how to fix] | [NNNN or —] |

## E2E Gate
[Exact command or check that proves the workflow succeeded]

## Safety Rules
1. NEVER [most critical constraint from this specific workflow]
2. [additional rules]

## Examples
**User:** `/[skill-name]`
**Agent behaviour:** [concrete, includes a non-obvious judgment call being resolved]
```

### Step 7: Show for approval

Print the complete draft SKILL.md to chat.

Then ask:
> "Shall I write this to
> `.claude/plugins/claude-skills-std/skills/[name]/SKILL.md`
> and add it to `plugin.json`?"

**Do not write any file until the user says yes.**

### Step 8: Write and register

After approval:

1. Create directory and write the file:
```bash
mkdir -p .claude/plugins/claude-skills-std/skills/[name]
```

2. Write SKILL.md using the Write tool.

3. Edit `plugin.json` — append new entry to the `skills` array:
```json
"skills/[name]/SKILL.md"
```

4. Commit and push:
```bash
git add .claude/plugins/claude-skills-std/skills/[name]/SKILL.md \
        .claude/plugins/claude-skills-std/.claude-plugin/plugin.json
git commit -m "feat: add [name] skill — packages [workflow] workflow"
git push -u origin <current-branch>
```

## Known Failures

| Failure | Symptom | Root Cause | Fix |
|---------|---------|-----------|-----|
| Happy-path bias | Skill has no Known Failures section | Agent skipped Step 4 (ADR extraction) | Re-run Step 4 — the value of the skill lives in the failures, not the happy path |
| Retrospective fabrication | Steps in skill never actually happened | Agent filled JOURNEY.md gaps without file validation | Step 3 is mandatory; mark every unverified claim explicitly |
| Scope drift to redesign | Skill describes an improved process, not what happened | Agent "improved" steps during extraction | Safety Rule 1: extract only, never redesign |
| Incomplete workflow packaged | Skill is unreliable in practice | Workflow was not ✅ before packaging | Step 1 gate: stop if not complete |

## Safety Rules

1. **NEVER redesign or improve the workflow** — extract exactly what happened, bugs
   included; improvements belong in a new ADR, not in this skill.
2. **NEVER write the SKILL.md file** before showing the complete draft to the user
   and receiving explicit approval.
3. **NEVER package a workflow that is not marked ✅ Complete** — an unfinished workflow
   produces an unreliable skill.
4. **NEVER omit the Known Failures section** — a skill without failure modes is
   incomplete.
5. **NEVER mark a JOURNEY.md claim as verified** without reading the actual file
   that proves it.

## Examples

**User:** `/workflow-to-skill Stage 3`

**Agent behaviour:**
Checks CLAUDE.md — Stage 3 is ✅ Complete. Searches JOURNEY.md for GCP / WIF /
gcp-bootstrap entries. Finds 4 sessions across 6 entries. Reads `terraform/wif.tf`,
`gcp-bootstrap.yml`, `populate-secrets.yml`, `rotate-github-pats.yml`, and 5 ADRs.
Marks all steps [verified]. Extracts 6 known failures (API propagation race, invalid
IAM role, naming constraint, WIF wildcard bug, etc.). Prints complete SKILL.md draft.
Waits for approval before writing any file.

**User:** `/workflow-to-skill Stage 4`

**Agent behaviour:**
Checks CLAUDE.md — Stage 4 is ⬜ Pending. Stops immediately and prints:
"Stage 4 is not yet marked ✅ Complete. Complete the workflow first, then
re-run /workflow-to-skill."
