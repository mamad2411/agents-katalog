---
name: sdd-new
description: >
  Starts a complete SDD cycle with mandatory exploration as first phase and user confirmation gates at each stage.
  Trigger: /sdd-new <description>, new SDD change, start full SDD cycle, new feature SDD.
format: procedural
model: haiku
---

# sdd-new

> Starts a complete SDD cycle for a change, with mandatory exploration as Step 1 and user confirmation gates before continuing.

**Triggers**: `/sdd-new <description>`, new SDD change, start full SDD cycle, new feature SDD

---

## Process

### Skill Resolution (Orchestrator)

Before launching each sub-agent, I resolve the skill path using:

```
1. .claude/skills/<skill-name>/SKILL.md     (project-local — highest priority)
2. openspec/config.yaml skill_overrides     (explicit redirect)
3. ~/.claude/skills/<skill-name>/SKILL.md   (global catalog — fallback)
```

I pass the resolved path in the sub-agent prompt. See `docs/SKILL-RESOLUTION.md` for the full algorithm.

---

### Step 0 — Infer slug from description

`$ARGUMENTS` must be a non-empty description of the change (e.g. `add payment flow`).

If empty or missing:

```
Usage: /sdd-new <description>

Provide a description of the change. Example:
  /sdd-new add payment flow
```

Stop here if argument is missing.

**Pre-processing sub-step — Flag detection and model routing setup** (runs before slug inference):

```
# 1. Detect --opus or --power flag
if $ARGUMENTS contains "--opus" or "--power":
  use_opus = true
  description = $ARGUMENTS with "--opus" and "--power" tokens stripped
else:
  use_opus = false
  description = $ARGUMENTS

# 2. Read openspec/config.yaml for per-phase model overrides (non-blocking)
try:
  phase_map = openspec/config.yaml → model_routing.phases  (map of phase_name → model_id)
catch (file missing, key absent, parse error, non-map value):
  phase_map = {}  # INFO note only — does NOT block execution

# 3. Resolution function (used at each Task call below)
resolve(phase, use_opus, phase_map):
  if use_opus == true  → return "claude-opus-4-5"
  if phase_map[phase] exists  → return phase_map[phase]
  return "claude-sonnet-4-5"  # existing default

# Warning: sdd-ff and sdd-new contain near-identical resolution sub-steps.
# Future edits to the algorithm MUST be applied to both files (see ADR 036).
```

Apply the slug inference algorithm (canonical definition: `docs/sdd-slug-algorithm.md`):

> Note: slug inference operates on `description` (flag-stripped), never on raw `$ARGUMENTS`.

```
STOP_WORDS = { "fix", "add", "update", "the", "a", "an", "for", "of", "in", "with",
               "showing", "wrong", "year", "users", "user" }

1. Lowercase and tokenize the description (split on spaces and punctuation)
2. Filter out tokens that are in STOP_WORDS
3. Take the first 5 remaining tokens as meaningful words
4. Join with hyphens
5. Prefix with today's date: YYYY-MM-DD
6. Truncate to 50 characters if needed
7. Check for collisions: if openspec/changes/[slug]/ already exists,
   append -2, then -3, etc., until the slug is unique
```

Output to user (do NOT ask for confirmation or rename):

```
Inferred change name: [slug]
```

---

### Step 1 — Run exploration (mandatory)

Launch the explore sub-agent unconditionally:

```
Task tool:
  subagent_type: "general-purpose"
  model: resolve("explore", use_opus, phase_map)
  # [resolved: claude-opus-4-5 if use_opus, else phase_map["explore"] if set, else claude-sonnet-4-5]
  prompt: |
    You are a specialized SDD sub-agent.

    STEP 1: Read the file ~/.claude/skills/sdd-explore/SKILL.md
    STEP 2: Follow its instructions exactly

    CONTEXT:
    - Project: [absolute path of current working directory]
    - Project governance: [absolute path of current working directory]/CLAUDE.md
    - Change: [inferred-slug]
    - Previous artifacts: none

    TASK: Execute the explore phase for change "[inferred-slug]". Save the output to openspec/changes/[inferred-slug]/exploration.md

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

Wait for result. Present the exploration summary to the user. If status is `blocked` or `failed`, stop and report.

---

### Step 2 — Launch propose sub-agent

```
Task tool:
  subagent_type: "general-purpose"
  model: resolve("propose", use_opus, phase_map)
  # [resolved: claude-opus-4-5 if use_opus, else phase_map["propose"] if set, else claude-sonnet-4-5]
  prompt: |
    You are a specialized SDD sub-agent.

    STEP 1: Read the file ~/.claude/skills/sdd-propose/SKILL.md
    STEP 2: Follow its instructions exactly

    CONTEXT:
    - Project: [absolute path of current working directory]
    - Project governance: [absolute path of current working directory]/CLAUDE.md
    - Change: [inferred-slug]
    - Previous artifacts: openspec/changes/[inferred-slug]/exploration.md

    TASK: Execute the propose phase for change "[inferred-slug]".

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

Wait for result. Present the proposal summary.

**Confirmation gate — after propose:**

```
Proposal created: openspec/changes/[inferred-slug]/proposal.md
[one-paragraph summary from sub-agent]

Continue to spec + design?
  Y → Launch spec and design in parallel
  N → Stop here (you can review the proposal and resume later with /sdd-ff [inferred-slug])
```

If user says N, stop gracefully.

---

### Step 3 — Launch spec + design sub-agents in parallel

Use two Task tool calls simultaneously:

**Spec sub-agent:**

```
Task tool:
  subagent_type: "general-purpose"
  model: resolve("spec", use_opus, phase_map)
  # [resolved: claude-opus-4-5 if use_opus, else phase_map["spec"] if set, else claude-sonnet-4-5]
  prompt: |
    You are a specialized SDD sub-agent.

    STEP 1: Read the file ~/.claude/skills/sdd-spec/SKILL.md
    STEP 2: Follow its instructions exactly

    CONTEXT:
    - Project: [absolute path of current working directory]
    - Project governance: [absolute path of current working directory]/CLAUDE.md
    - Change: [inferred-slug]
    - Previous artifacts: openspec/changes/[inferred-slug]/proposal.md

    TASK: Execute the spec phase for change "[inferred-slug]".

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

**Design sub-agent:**

```
Task tool:
  subagent_type: "general-purpose"
  model: resolve("design", use_opus, phase_map)
  # [resolved: claude-opus-4-5 if use_opus, else phase_map["design"] if set, else claude-sonnet-4-5]
  thinking: enabled
  prompt: |
    You are a specialized SDD sub-agent.

    STEP 1: Read the file ~/.claude/skills/sdd-design/SKILL.md
    STEP 2: Follow its instructions exactly

    CONTEXT:
    - Project: [absolute path of current working directory]
    - Project governance: [absolute path of current working directory]/CLAUDE.md
    - Change: [inferred-slug]
    - Previous artifacts: openspec/changes/[inferred-slug]/proposal.md

    TASK: Execute the design phase for change "[inferred-slug]".

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

Wait for **both** to complete. Present both summaries.

**Confirmation gate — after spec + design:**

```
Spec and design complete:
  spec   : [status] — [one-line summary]
  design : [status] — [one-line summary]

[If any warnings] Warnings: [list]

Continue to tasks breakdown?
  Y → Launch tasks sub-agent
  N → Stop here (resume later with /sdd-tasks [inferred-slug])
```

If user says N, stop gracefully.

---

### Step 4 — Launch tasks sub-agent

```
Task tool:
  subagent_type: "general-purpose"
  model: resolve("tasks", use_opus, phase_map)
  # [resolved: claude-opus-4-5 if use_opus, else phase_map["tasks"] if set, else claude-sonnet-4-5]
  prompt: |
    You are a specialized SDD sub-agent.

    STEP 1: Read the file ~/.claude/skills/sdd-tasks/SKILL.md
    STEP 2: Follow its instructions exactly

    CONTEXT:
    - Project: [absolute path of current working directory]
    - Project governance: [absolute path of current working directory]/CLAUDE.md
    - Change: [inferred-slug]
    - Previous artifacts: openspec/changes/[inferred-slug]/proposal.md, openspec/changes/[inferred-slug]/specs/, openspec/changes/[inferred-slug]/design.md

    TASK: Execute the tasks phase for change "[inferred-slug]".

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

Wait for result.

---

### Step 5 — Present complete summary and remaining phases

```
SDD cycle ready — [inferred-slug]

Phase results:
  explore  : [status] — [summary]
  propose  : [status] — [summary]
  spec     : [status] — [summary]
  design   : [status] — [summary]
  tasks    : [status] — [summary]

Artifacts:
  openspec/changes/[inferred-slug]/exploration.md
  openspec/changes/[inferred-slug]/proposal.md
  openspec/changes/[inferred-slug]/specs/*/spec.md
  openspec/changes/[inferred-slug]/design.md
  openspec/changes/[inferred-slug]/tasks.md

[If any warnings] Warnings:
  - [warning text]

Remaining phases:
  → /sdd-apply [inferred-slug]   — implement the tasks
  → /sdd-verify [inferred-slug]  — verify against specs
  → /sdd-archive [inferred-slug] — archive when done (auto-updates ai-context/ memory)

Ready to implement? Run:
  /sdd-apply [inferred-slug]
```

Do NOT invoke `/sdd-apply` automatically. The user must trigger it explicitly.

---

## Rules

- `$ARGUMENTS` must be provided — fail early with usage if missing
- The slug is always inferred from the description — do NOT ask the user to provide or confirm a name
- The explore phase is mandatory and runs unconditionally as Step 1 (no user gate)
- There are two mandatory confirmation gates: after propose, and after spec+design
- `spec` and `design` sub-agents are always launched in parallel (single message with two Task calls)
- If any phase returns `blocked` or `failed`, stop immediately — do NOT continue
- Warnings are surfaced but do not block the cycle
- I do NOT invoke `/sdd-apply` automatically — user must trigger it explicitly
- I maintain minimal state: only file paths between phases, not file contents
- The inferred slug is passed to all sub-agents (never the raw description)
- After stopping gracefully at any gate, inform the user which command resumes from that point
