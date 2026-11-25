---
name: pwrl-work-triage
description: Classify work input and extract foundational context for execution
argument-hint: "[Task file path, plan path, or bare prompt. Leave blank to use latest task]"
---

# pwrl-work-triage — Input Classification & Context Extraction

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What work should be triaged? Provide a task file path, plan file, or describe the work to be categorized."
- Provide clear recovery suggestions when errors occur

**Purpose:** Entry point to the work execution workflow. Classifies the input (task file, plan file, or bare prompt), extracts relevant context, estimates complexity, resolves dependencies, and returns a structured context object for downstream skills.

## Input

<input_document> #$ARGUMENTS </input_document>

### Supported Input Types

| Type            | Detection                                            | Example                                  |
| --------------- | ---------------------------------------------------- | ---------------------------------------- |
| **Task file**   | Contains `unit-id` in YAML frontmatter               | `docs/tasks/to-do/2026-06-05-u1-task.md` |
| **Plan file**   | No `unit-id` in frontmatter, points to `docs/plans/` | `docs/plans/2026-06-05-001-plan.md`      |
| **Bare prompt** | Neither of the above                                 | `"Add email validation to user signup"`  |

## Output: Classified Context

After triage, produce a context object with fields varying by input type:

```yaml
inputType: task | plan | prompt
complexity: trivial | small | medium | large
blockedBy: []
# Type-specific fields below
```

Detailed shape per input type is documented in each classification section.

---

## Workflow

### 1. Classify Input

Determine the input type:

- **If input path contains `docs/tasks/` and points to a file with `unit-id` in frontmatter** → Task file
- **Else if input path points to `docs/plans/` or contains `plan` in filename** → Plan file
- **Otherwise** → Bare prompt

### 2. Classify Task File

When input is a task file path:

**Step 1 — Read frontmatter:**

Extract these fields from the YAML frontmatter:

| Field          | Required | Description                                                  |
| -------------- | -------- | ------------------------------------------------------------ |
| `unit-id`      | Yes      | Stable task identifier (e.g., `S1`, `U1`)                    |
| `plan`         | Yes      | Relative path to linked plan file                            |
| `status`       | Yes      | Current status: `to-do`, `in-progress`, `for-review`, `done` |
| `dependencies` | No       | List of task unit-ids this depends on                        |
| `files`        | No       | List of primary files affected by this task                  |
| `github-issue` | No       | GitHub issue number (if linked to an issue)                  |
| `created`      | No       | Creation date                                                |

**Step 2 — Load linked plan file:**

- Read the plan file specified in the `plan` field
- Extract: plan overview, technical decisions, non-goals, implementation units
- Use this context to understand the broader rationale

**Step 3 — Resolve dependencies:**

1. Read `docs/tasks/INDEX.md` (or `INDEX-S*.md`) to check each dependency's status
2. For each dependency listed in frontmatter:
   - If status is `done` or `for-review` → dependency met
   - If status is `to-do` or `in-progress` → add to `blockedBy` list
   - If task not found in INDEX → add to `blockedBy` as "missing"
3. Build transitive dependency chain (dependencies of dependencies)
4. Check for circular dependencies: if A depends on B and B depends on A → fail

**Step 4 — Estimate complexity (from task scope):**

- Based on `files` count and task body length
- 1 file, no behavior change → `trivial`
- 1-2 files, bounded scope → `small`
- 3-5 files, moderate logic → `medium`
- 6+ files or cross-cutting → `large`

**Step 5 — Discover cross-plan dependencies (NEW):**

1. Scan `docs/plans/*.md` for all active plan files
2. For each plan, extract all task unit-ids and their dependencies
3. Build a global dependency graph (union of all per-plan graphs)
4. **Detect global unit-id duplicates**: If the same unit-id appears in multiple plans → error "Duplicate unit-id: S1 found in plan-A and plan-B"
5. Annotate cross-plan dependencies: "S1 (plan-A) depends on U2 (plan-B)"
6. Return: Complete dependency graph with cross-plan edges marked

**Step 6 — Check for circular dependencies (multi-plan scope, UPDATED):**

1. Build DFS stack for cycle detection
2. Walk the global dependency graph (including cross-plan edges)
3. If cycle detected: report path (e.g., "S1 (plan-A) → U2 (plan-B) → S1")
4. Fail with clear error; ask user to resolve

**Output context:**

```yaml
inputType: task
taskFile: docs/tasks/to-do/2026-06-05-u1-task.md
unit-id: S1
plan: docs/plans/2026-06-05-002-plan.md
status: to-do
dependencies: [S2, S3]
files: [src/utils.ts, src/api.ts]
githubIssue: 123 # or null if absent
complexity: medium
blockedBy: []
dependencyChain: [S2 → S3 → S4]
globalDependencyGraph: { S1: [S2, S3], S2: [U1], U1: [] }
crossPlanDeps: [{ from: S2, fromPlan: plan-002, to: U1, toPlan: plan-001 }]
```

### 3. Classify Plan File

When input is a plan file path (no `unit-id`):

**Step 1 — Read plan frontmatter:**

| Field     | Description                               |
| --------- | ----------------------------------------- |
| `id`      | Plan identifier (e.g., `2026-06-05-002`)  |
| `tier`    | Planning tier: `Fast`, `Standard`, `Deep` |
| `status`  | `active`, `draft`, `archived`             |
| `created` | Creation date                             |
| `updated` | Last update date                          |

**Step 2 — Extract implementation units:**

- Scan plan body for unit headers (e.g., `### U1`, `### S1`, `**U1:**`)
- For each unit extract: unit ID, name/scope, files affected, approach
- Build a unit list with descriptions

**Step 3 — Estimate complexity from unit count:**

| Units | Complexity          | Expected Mode                         |
| ----- | ------------------- | ------------------------------------- |
| 1-2   | `trivial` / `small` | Inline execution                      |
| 3-5   | `medium`            | Serial execution                      |
| 6+    | `large`             | Serial with possible parallel subsets |

**Output context:**

```yaml
inputType: plan
planFile: docs/plans/2026-06-05-002-plan.md
planId: 2026-06-05-002
tier: Standard
planStatus: active
units:
  - unit-id: U1
    name: Input Triage
    files: [pwrl-work-triage/SKILL.md]
    approach: Extract Phase 0 logic
  - unit-id: U2
    name: Environment Setup
    files: [pwrl-work-prepare/SKILL.md]
    approach: Extract Phase 1 logic
complexity: medium
estimatedTasks: 5
```

### 4. Classify Bare Prompt

When input is a freeform text description:

**Step 1 — Estimate complexity by heuristic:**

Apply rules in order:

| Signal                                                               | Complexity |
| -------------------------------------------------------------------- | ---------- |
| Single file, no behavior change (rename, config, styling)            | `trivial`  |
| 1-2 files, clear bounded scope, no cross-cutting concerns            | `small`    |
| 3-5 files, moderate logic, behavior change, tests needed             | `medium`   |
| 6+ files, architectural work, security, payments, auth, core systems | `large`    |

**Step 2 — Scan codebase for context:**

- Search for existing tests related to keywords in prompt
- Find related modules or utilities via filename patterns
- Identify similar patterns already in codebase

**Step 3 — Warn if complexity is large:**

If complexity is `large`:

- Recommend planning with `/pwrl-plan` workflow first
- Ask user: "This work appears large/complex. Understanding risks and tradeoffs, do you want to proceed without formal planning?"
- Only proceed if user expressly confirms

**Output context:**

```yaml
inputType: prompt
prompt: "Add email validation to user signup"
complexity: medium
complexitySignals:
  - "Affects 3-5 files"
  - "Behavior changes to existing logic"
  - "Multiple test scenarios needed"
relatedPatterns:
  - "src/validators/phone.ts" # similar validation pattern
planningRecommended: false
```

### 5. Select Interaction Mode

After classifying input, ask the user to choose their engagement level for this workflow. Use the platform's `ask_user_question` extension (or equivalent) to present the following three options:

**Question:** "How would you like to proceed with this workflow?"

**Options:**

- **Detailed (Step-by-Step)** — Review and confirm at each phase transition (Prepare → Execute → Review → Finalize); inspect generated artifacts; approval gates at each transition. Slower but maximum control. Best for complex work, unfamiliar codebases, and learning.
- **Smart (Risk-gated automation)** — Phases run automatically; pause only when the next phase produces a HIGH-risk operation (destructive git, irreversible API calls, schema-breaking migrations). v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start. See `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` §"Future Refinements" for the full risk-classification roadmap.
- **Yolo (Full Automation)** — Fully automated from Phase 1 through Phase 3; review and confirm only at the end. Fastest execution. Best for straightforward tasks, well-understood scope, and time-sensitive work.

**Store selection in context:**

```yaml
interactionMode: detailed | smart | yolo
```

**Propagation:** The `interactionMode` value flows into `pwrl-work-prepare`, `pwrl-work-execute`, `pwrl-work-review`, and `pwrl-work-sync-status` artifacts. Each downstream phase reads the value and adjusts its confirmation behavior:

- **Detailed:** Pause at every phase transition; show generated artifacts; require explicit approval.
- **Smart:** Run phases automatically; pause only at HIGH-risk operations.
- **Yolo:** Run every phase automatically; report only the final outcome.

**Backward compatibility note:** Downstream phases (e.g., older `pwrl-work-execute` builds) that still assume a two-value enum must treat any value other than `detailed` as `yolo` until upgraded. The `smart` value is new as of 2026-06-29.

---

## Error Handling

| Scenario                            | Handling                                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| Task file not found                 | Log path; ask user: "Provide a different path or create a new task?"                       |
| Plan file not found                 | Log path; ask user: "Provide a different path or use /pwrl-plan?"                          |
| Circular dependencies               | Walk dep tree; fail with `Circular: [A→B→C→A]`; ask user to resolve                        |
| Missing dependencies                | Log; add to `blockedBy`; warn: "Not found in INDEX. Proceeding may cause ordering issues." |
| Input is empty                      | Ask user: "What would you like to work on?"                                                |
| File unreadable                     | Log error; ask user: "Cannot read file. Retry or provide different path?"                  |
| Malformed frontmatter               | Log details; ask user to fix frontmatter and retry                                         |
| Complexity is `large` (bare prompt) | Warn; require user confirmation before proceeding                                          |
| Task references non-existent plan   | Warn; proceed with caution                                                                 |

**Retry limit:** 3 attempts per operation, then ask user to fix manually.

**Fallback:** If all retries fail, log the error and ask user: "Retry, skip, or abort?"

---

## Dependencies

- **File system** — Reading task files, plan files, INDEX files
- **`.pwrlrc.json`** — For GitHub integration check (though actual syncing happens in pwrl-work-sync-status)

## References

- **S1 Analysis:** `docs/analysis/2026-06-05-pwrl-work-structure-analysis.md`
- **Source Phase 0:** Installed `pwrl-work` skill (Phase 0: Triage Input, lines 26-48)
- **Next Skill:** `pwrl-work-prepare` (consumes this skill's output context)
