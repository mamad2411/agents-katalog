---
name: sdd-ff
description: >
  Fast-forward SDD cycle: includes mandatory exploration as Step 0, then runs propose → spec+design (parallel) → tasks automatically, then asks before apply.
  Trigger: /sdd-ff <description>, quick SDD cycle, fast-forward, fast forward SDD.
format: procedural
model: haiku
---

# sdd-ff

> Fast-forward SDD cycle: infers slug, runs mandatory exploration (Step 0), then propose → spec+design (parallel) → tasks automatically, then asks before apply.

**Triggers**: `/sdd-ff <description>`, fast-forward, quick SDD cycle, fast forward SDD

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

### Step 0 — Infer slug and run exploration

`$ARGUMENTS` must be a non-empty description of the change (e.g. `add payment flow`).

If empty or missing:

```
Usage: /sdd-ff <description>

Provide a description of the change. Example:
  /sdd-ff add payment flow
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

**Infer the slug** using the algorithm below (canonical definition: `docs/sdd-slug-algorithm.md`):

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

**Context extraction sub-step** (runs before explore launch, non-blocking):

Scan the user's `/sdd-ff` description for context patterns:

```
Extract from description (and any prior conversation turns visible in context):
  - "remove X", "no longer X", "delete X"    → removals list
  - "replace X with Y", "change X to Y"      → replacements list
  - "mobile must", "not on web", "desktop only" → platform constraints list
  - "careful with Y", "provisional pending Z"  → caution notes list

If any patterns found:
  Pre-populate openspec/changes/[inferred-slug]/proposal.md with skeleton:
    ## Context Notes (from conversation — preliminary)
    ### Removals Mentioned
    - [list of removals]
    ### Replacements Mentioned
    - [list of replacements]
    ### Platform Constraints
    - [list of constraints]
    ### Provisional Notes
    - [list of notes]

If no patterns found:
  Skip pre-population silently — log INFO: "No context patterns detected — skipping pre-population"
```

This step is **non-blocking**: any failure produces at most an INFO note. Pre-populated content is preliminary — sdd-propose will refine it.

**Then immediately launch the explore sub-agent** (no user gate):

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
    - Previous artifacts: none (check for pre-seeded proposal.md at openspec/changes/[inferred-slug]/proposal.md)

    TASK: Execute the explore phase for change "[inferred-slug]".

    Return:
    - status: ok|warning|blocked|failed
    - summary: executive summary for decision-making
    - artifacts: files created/modified
    - next_recommended: next phases
    - risks: identified risks (if any)
```

Wait for result. If status is `blocked` or `failed`, stop and present a reformulated error message (see Error Reformulation below). If status is `warning`, continue but surface the warning prominently.

**Contradiction gate sub-step** (runs after explore completes, before launching propose):

```
PRECONDITION — Pre-existing exploration.md detection:
  Before reading ## Contradiction Analysis, check whether exploration.md was pre-existing:
  - If openspec/changes/[inferred-slug]/exploration.md existed BEFORE this sdd-ff run
    (i.e., the explore sub-agent did not create it — it was already present):
    → Log: "INFO: exploration.md was pre-existing — contradiction gate skipped."
    → Skip this entire gate sub-step and proceed to Step 1 (propose) immediately.
  - If exploration.md was created by the explore sub-agent in this run:
    → Continue with the gate logic below.

Read openspec/changes/[inferred-slug]/exploration.md → ## Contradiction Analysis section.

If section absent or states "No contradictions detected.":
  → Continue to Step 1 (propose) immediately — no gate.

If section contains only CERTAIN contradictions:
  → Log: "CERTAIN contradiction(s) detected — will be documented in proposal Contradiction Resolution section."
  → Continue to Step 1 (propose) immediately — no gate for CERTAIN.

If section contains one or more UNCERTAIN contradictions:
  → Present blocking gate to user:

    ⚠️ Exploration found UNCERTAIN contradiction(s) before proposing:
    [For each UNCERTAIN item:]
      - [Item name]: [explanation of what conflicts with what]
        Severity: [INFO|WARNING|CRITICAL]

    Resolving contradictions now prevents the spec and design from making conflicting assumptions that would surface later during implementation.

    Does this proposal intend to change/remove the above? Please confirm:
      Yes    — Proceed; I'll record your decision in the proposal.
      No     — Halt; please clarify the change description.
      Review — Show me the full Contradiction Analysis section before I decide.

  → WAIT for user response. Do NOT launch propose until user responds.

  → If user says "Yes":
      - Record in proposal.md ## Decisions section:
        ### Contradiction Confirmation
        Date: [ISO 8601 timestamp]
        User answer: Confirmed — proceeding with change as described.
        Items confirmed: [list each UNCERTAIN item]
      - Continue to Step 1 (propose).

  → If user says "No":
      - Halt. Report:
        "Cycle halted at contradiction gate. Please clarify your change description and re-run /sdd-ff."
      - STOP.

  → If user says "Review":
      - Display full ## Contradiction Analysis section from exploration.md.
      - Re-present the gate with the same Yes/No/Review options.
      - WAIT for a new response.
```

---

### Step 1 — Launch propose sub-agent

Use the Task tool:

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

Wait for the result. If status is `blocked` or `failed`, stop and present a reformulated error message (see Error Reformulation below). If status is `warning`, continue but surface the warning prominently.

---

### Step 2 — Launch spec + design sub-agents in parallel

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

Wait for **both** to complete before proceeding. If either is `blocked` or `failed`, stop and present a reformulated error message (see Error Reformulation below). Surface any warnings from either.

---

### Step 3 — Launch tasks sub-agent

Use the Task tool:

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

Wait for the result. If status is `blocked` or `failed`, stop and present a reformulated error message (see Error Reformulation below). If status is `warning`, continue but surface the warning prominently.

---

### Error Reformulation

When any sub-agent returns `status: blocked` or `status: failed`, do NOT relay the raw status verbatim as the only content. Instead, present a reformulated message:

```
⚠️ [Phase name] returned [status]: [original summary from sub-agent]
This happened because [cause derived from the sub-agent's summary].
To resolve it, [concrete next step the user can take].
```

This pattern applies to explore (Step 0), propose (Step 1), spec and design (Step 2), and tasks (Step 3). Statuses `ok` and `warning` are NOT affected — they follow the normal summary presentation.

---

### Step 4 — Present complete summary and ask before apply

Present to the user:

```
Fast-forward complete — [inferred-slug]

Phase results:
  explore  : [status] — [one-line summary]
  propose  : [status] — [one-line summary]
  spec     : [status] — [one-line summary]
  design   : [status] — [one-line summary]
  tasks    : [status] — [one-line summary]

Artifacts created:
  openspec/changes/[inferred-slug]/exploration.md
  openspec/changes/[inferred-slug]/proposal.md
  openspec/changes/[inferred-slug]/specs/*/spec.md
  openspec/changes/[inferred-slug]/design.md
  openspec/changes/[inferred-slug]/tasks.md

[If any warnings] Warnings:
  - [warning text]

[1-paragraph narrative reflection — only when all phases completed successfully, not when halted:]
This cycle [summarize what was decided and specified, what architectural decisions were captured in the design, and what risks the structured SDD approach mitigated that ad-hoc implementation would have missed — reference the specific change domain, not generic SDD praise].

Continue with implementation? Reply **yes** to proceed.
_(Manual: `/sdd-apply [inferred-slug]`)_

Note: When the cycle completes, /sdd-archive will auto-update ai-context/ memory.
```

Do NOT invoke `/sdd-apply` automatically. The user must trigger it explicitly.

---

## Rules

- `$ARGUMENTS` must be provided — fail early with usage if missing
- The slug is always inferred from the description — do NOT ask the user to provide or confirm a name
- Exploration runs unconditionally as Step 0 (no user gate)
- Context extraction (pre-population) runs BEFORE explore launch — it is non-blocking
- Contradiction gate runs AFTER explore completes and BEFORE propose launches — it is blocking only for UNCERTAIN contradictions
- CERTAIN contradictions are NOT gated — they are passed to sdd-propose for documentation
- Prior attempt findings from exploration.md are informational only — they do NOT trigger a gate
- The contradiction gate requires explicit user response (Yes/No/Review) — there is no bypass or timeout
- Sub-agents are launched with the Task tool; I (sdd-ff) am the orchestrator, not a sub-agent
- `spec` and `design` sub-agents are always launched in parallel (single message with two Task calls)
- If any phase returns `blocked` or `failed`, stop immediately and report — do NOT continue to the next phase
- Warnings are surfaced but do not block the cycle
- I do NOT invoke `/sdd-apply` automatically — user must trigger it explicitly
- I maintain minimal state: only file paths, not file contents, between phases
- The inferred slug is passed to all sub-agents (never the raw description)
