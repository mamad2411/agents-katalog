---
name: sherpy-flow
description: Orchestrates the full Sherpy planning workflow from requirements to QA-ready delivery plan. Detects which artifacts already exist, shows a visual pipeline status, and guides through each skill in sequence — gap analysis, business interview, technical interview, implementation planning, plan review, definition of done, architecture decisions, delivery timeline, and QA test plan.
---

# Sherpy Flow

Runs the complete Sherpy planning pipeline from start to finish. Detects your current position in the workflow based on existing artifacts and resumes from there. You never need to remember which skill comes next or what its inputs are.

## Usage

```
/sherpy-flow [project-directory]
```

If no directory is given, use the current working directory.

## The Pipeline

```
Step 1   Gap Analysis Worksheet         → gap-analysis-worksheet.md
Step 2   Business Requirements          → business-requirements.yaml
Step 3   Technical Requirements         → technical-requirements.yaml
Step 4   Implementation Planner         → milestones.yaml + milestone-m*.tasks.yaml
Step 5   Implementation Plan Review     → implementation-plan-review.yaml
Step 6   Definition of Done             → definition-of-done.yaml
Step 7   Architecture Decision Records  → adrs/INDEX.md + adrs/ADR-*.md
Step 8   Delivery Timeline              → timeline.yaml
Step 9   QA Test Plan                   → qa-test-plan.yaml
```

## Process

### Step 1: Scan for Existing Artifacts

Check the project directory for these files to determine which steps are already complete:

| Artifact | Indicates step complete |
|----------|------------------------|
| `gap-analysis-worksheet.md` | Step 1 |
| `business-requirements.yaml` | Step 2 |
| `technical-requirements.yaml` | Step 3 |
| `milestones.yaml` | Step 4 |
| `implementation-plan-review.yaml` | Step 5 |
| `definition-of-done.yaml` | Step 6 |
| `adrs/INDEX.md` | Step 7 |
| `timeline.yaml` | Step 8 |
| `qa-test-plan.yaml` | Step 9 |

### Step 2: Show Pipeline Status

Display a visual status of the pipeline before doing any work:

```
## Sherpy Flow — [Project Directory]

 ✓  Step 1   Gap Analysis Worksheet
 ✓  Step 2   Business Requirements
 →  Step 3   Technical Requirements        ← resuming here
 ○  Step 4   Implementation Planner
 ○  Step 5   Implementation Plan Review
 ○  Step 6   Definition of Done
 ○  Step 7   Architecture Decision Records
 ○  Step 8   Delivery Timeline
 ○  Step 9   QA Test Plan

Resuming from Step 3. Type "start over" to restart from Step 1,
or specify a step number to jump to a specific point.
```

**Legend:** ✓ complete · → current · ○ pending

Then ask:

> "Ready to continue from Step [n]: [Step Name]? (yes / start over / jump to step N)"

Wait for confirmation before proceeding.

### Step 3: Execute Each Step

For each pending step, follow the referenced skill's full process as if it were invoked directly. The behavior at each step is identical to invoking the skill standalone — sherpy-flow is a sequencer, not a replacement.

**Step 1 — Gap Analysis Worksheet (`/gap-analysis-worksheet`)**
- Skip this step if no initial requirements document is present in the project directory.
- If an initial requirements document exists (any `.md`, `.txt`, or `.docx`-described file), run the gap analysis against it.
- After completing, ask: "Gap analysis worksheet generated. Shall I continue to the Business Requirements Interview?"

**Step 2 — Business Requirements Interview (`/business-requirements-interview`)**
- Run the full interview process (one question at a time, tracks progress in `business-interview.jsonl`).
- After `business-requirements.yaml` is generated, display the summary and ask: "Business requirements complete. Continue to Technical Requirements?"

**Step 3 — Technical Requirements Interview (`/technical-requirements-interview`)**
- Requires `business-requirements.yaml`.
- Run the full interview process.
- After `technical-requirements.yaml` is generated, display the summary and ask: "Technical requirements complete. Continue to Implementation Planner?"

**Step 4 — Implementation Planner (`/implementation-planner`)**
- Requires `business-requirements.yaml` + `technical-requirements.yaml`.
- Generate `milestones.yaml` + `milestone-m*.tasks.yaml`.
- After completion, display milestone summary and ask: "Implementation plan generated. Continue to Plan Review?"

**Step 5 — Implementation Plan Review (`/implementation-plan-review`)**
- Requires `milestones.yaml` + task files.
- Run the full review.
- After `implementation-plan-review.yaml` is generated, display the readiness score and critical issues.
- If critical issues exist, ask:
  > "The plan review found [n] critical issue(s). Would you like to:
  > 1. Address issues now (loops back to Step 4)
  > 2. Continue with acknowledged issues
  > 3. Review the issues in detail first"
- Otherwise ask: "Plan review passed. Continue to Definition of Done?"

**Step 6 — Definition of Done (`/definition-of-done`)**
- Requires `milestones.yaml` + `business-requirements.yaml`.
- Generate `definition-of-done.yaml`.
- After completion, display milestone count and ask: "Definition of Done generated. Continue to Architecture Decision Records?"

**Step 7 — Architecture Decision Records (`/architecture-decision-record`)**
- Requires `technical-requirements.yaml`.
- Generate `adrs/` directory with all ADR files.
- After completion, display ADR count and ask: "Architecture decisions recorded. Continue to Delivery Timeline?"

**Step 8 — Delivery Timeline (`/delivery-timeline`)**
- Requires `milestones.yaml`.
- Ask the three delivery parameter questions (production deploy date, QA rounds, days per round) as defined in that skill.
- Generate `timeline.yaml`.
- After completion, display the workback summary (project start → deploy date) and ask: "Delivery timeline generated. Continue to QA Test Plan?"

**Step 9 — QA Test Plan (`/qa-test-plan`)**
- Requires `business-requirements.yaml` + `technical-requirements.yaml`.
- Generate `qa-test-plan.yaml`.
- After completion, display coverage summary.

### Step 4: Final Summary

After all steps are complete, display a final summary:

```
## Sherpy Flow Complete ✓

**Project:** [name]
**Directory:** [path]

Generated Artifacts:
  gap-analysis-worksheet.md       [if generated]
  business-requirements.yaml
  technical-requirements.yaml
  milestones.yaml
  milestone-m*.tasks.yaml         ([n] files)
  implementation-plan-review.yaml
  definition-of-done.yaml
  adrs/                           ([n] ADR files)
  timeline.yaml
  qa-test-plan.yaml

Timeline: [project start date] → [production deploy date]
Total Delivery Days: [n] business days
QA Rounds: [n] × [n] days each

Your project is ready for development. Use /create-continuation-prompt
if you need to hand off context to a new session.
```

## Transition Rules

- **Always confirm** before moving to the next step — never auto-advance.
- **Loop-back**: If the user says "go back" or "redo step N", return to that step and re-run it. The new output overwrites the previous artifact.
- **Skip**: If the user says "skip step N", mark it as skipped and note it in the final summary. Downstream steps that require its output will warn if the input is missing.
- **Jump**: If the user says "jump to step N", run from that step forward. Load any required inputs from existing artifacts.
- **Interruption**: If the user needs to stop mid-flow, remind them they can resume by running `/sherpy-flow` again — the pipeline status will show exactly where they left off.
