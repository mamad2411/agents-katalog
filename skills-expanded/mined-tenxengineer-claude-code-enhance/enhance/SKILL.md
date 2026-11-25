---
name: enhance
preamble-tier: 1
version: 1.0.0
description: |
  Augment-style prompt enhancer for Claude Code. Takes a rough developer
  intent and produces a production-quality, codebase-aware, lesson-cross-
  referenced, prompt-engineering-optimized prompt that the user reviews and
  approves before execution.

  USE THIS SKILL when the user types "/enhance <rough idea>", "enhance:
  <idea>", "improve this prompt: <idea>", "structure this: <idea>",
  "expand this: <idea>", "make this prompt better:", "rephrase as a proper
  prompt:", or asks for a better-written/structured version of their
  request before any actual work begins. ALSO use when the user gives a
  vague high-level request with multiple possible interpretations and you
  want to align with them BEFORE coding — the enhancement output surfaces
  ambiguities as explicit questions.

  The skill loads project context (codemap, lessons, CLAUDE.md, recent git
  activity) and applies real prompt engineering principles (clear goal,
  scope, constraints, success criteria, suggested approach, anti-patterns,
  verification). The user can submit, edit, or scrap the enhanced version.

  This is a USER-FACING enhancement tool. The user must approve the
  enhanced version before it becomes the actual instruction. Never auto-
  apply the enhanced prompt without explicit user confirmation.
---

# Enhance — Production-Quality Prompt Enhancer

When the user invokes this skill (via `/enhance <rough intent>` or any
trigger phrase listed in the description), follow this protocol exactly.
The output is a structured, codebase-aware prompt the user reviews,
edits, or submits verbatim.

The end goal: lift a vague developer thought into a prompt that a
distinguished engineer would actually act on.

## Step 1 — Capture the rough intent

The user has typed something like:

> /enhance refactor auth middleware

Capture their full text after the trigger word. This is the **rough
intent**. Preserve it verbatim — never lose the original wording.

## Step 2 — Load project context aggressively

Run these in parallel where possible. Skip silently any source that
doesn't exist:

### 2a. Codemap

- Walk up from CWD to find `.codemap/` directory
- If found, read `overview.md`, `hotfiles.md`, `recent.md`
- These give architecture, hot files, and current sprint state

### 2b. Lessons (scar tissue library)

- List `~/.claude/lessons/*.md` (one per domain)
- For each domain file, grep its `**Tags:**` lines for keywords from the rough intent
- Read any matching domain files in full — those lessons apply

### 2c. Project conventions

- Read `<project-root>/CLAUDE.md` if present (project-specific rules)
- Read `<project-root>/AGENTS.md`, `GEMINI.md`, `.claude/CLAUDE.md`
  variants if present
- Check `~/.claude/memory/_global/MEMORY.md` for universal rules

### 2d. Codebase structure (if Serena MCP is connected)

- Use `find_symbol` or `get_symbol_overview` to identify relevant code
- If a specific module/file is implied, get its symbol overview
- Use `find_references` to identify all callers of relevant symbols

### 2e. Codebase structure (Serena fallback — grep + find)

- If Serena isn't available, use `grep -r`, `find`, and `git ls-files`
  to identify relevant files
- Cap the search to stay under ~30 seconds

### 2f. Recent activity

- `git log --since="14 days ago" --oneline -- <relevant-paths>`
- Anything in flight or recently changed near this work

## Step 3 — Apply prompt engineering principles

Process the rough intent through these stages:

### 3a. Intent classification

Classify the rough intent as one of:

- **build** — new feature, new module, new endpoint
- **refactor** — change existing structure, no behavior change
- **migrate** — replace one approach with another
- **debug** — fix a known bug or symptom
- **investigate** — understand something before deciding
- **review** — assess existing code, no changes
- **plan** — produce a spec/RFC, no implementation
- **optimize** — improve performance/cost/UX of existing code

### 3b. Goal extraction

Distill the rough intent into ONE crisp goal sentence. Concrete, not
abstract. Names the outcome, not the process.

### 3c. Scope detection

- **In scope:** specific files/symbols/modules from context loading
- **Out of scope:** related areas the user explicitly or implicitly excluded
- Be explicit about both. Vague scope is the #1 cause of scope creep.

### 3d. Constraints

Pull from:

- Project CLAUDE.md (specific rules: stack defaults, conventions)
- Lessons that match this intent (cite by ID: L-AUTH-001, etc.)
- Global MEMORY.md (universal preferences)
- Anti-patterns the user has burned us with before

### 3e. Success criteria

Specific, verifiable conditions. Not "tests pass" — "ran X, Y passed,
manually verified Z". Each criterion answers: "how would I verify this
in production?"

### 3f. Implicit assumptions

Surface things the user is taking for granted that might be wrong:

- Assumed scope boundaries
- Assumed default values
- Assumed migration paths
- Assumed concurrency/scale characteristics

Format as explicit yes/no or short-answer questions.

### 3g. Suggested approach

A 3-5 step high-level plan. Not detailed implementation — just the
shape of the work. Reference which skills should be invoked at each
step (`spec-architect` for planning, `consult-scars` already auto-
fires, `codex` for adversarial review post-implementation, etc.).

### 3h. Risk classification

**high** — security-critical, payment, migrations, production data,
distributed consensus, cryptography
**medium** — auth, persistent state, public APIs, infra changes
**low** — UI tweaks, internal refactors, dev tooling, docs

Cite the specific reason for the risk level.

## Step 4 — Produce the enhanced prompt

Output using this structure (markdown, with the original prompt
preserved at the bottom for reference):

```markdown
# Enhanced Prompt

> **Original rough intent:** <verbatim user input>

## Intent class

<one of: build | refactor | migrate | debug | investigate | review | plan | optimize>

## Goal

<one crisp sentence>

## Scope

**In:**

- <file/module/symbol path 1>
- <file/module/symbol path 2>
- ...

**Out:**

- <explicit exclusion 1>
- <explicit exclusion 2>

## Constraints

**Lessons that apply:**

- **L-XXX-NNN** — <one-line summary>
- **L-YYY-NNN** — <one-line summary>

**Project rules (from CLAUDE.md):**

- <rule 1>
- <rule 2>

**Universal preferences (from global MEMORY):**

- <pref 1>

## Success criteria

1. <verifiable condition with command + expected outcome>
2. <verifiable condition>
3. <verifiable condition>

## Implicit assumptions to confirm

- [ ] <question 1 with multiple-choice answers if helpful>
- [ ] <question 2>
- [ ] <question 3>

## Suggested approach

1. **<step 1>** — invoke `<skill>` if applicable
2. **<step 2>** — ...
3. **<step 3>** — ...
4. **Verification step** — `/browse` for UI, full test suite for backend, etc.

## Skills to invoke

- `<skill 1>` — <why>
- `<skill 2>` — <why>

## Risk: <high | medium | low>

<one-line reason — cite specific lesson IDs or domain factors>

---

**Original prompt preserved:**
<verbatim user input>
```

## Step 5 — Present and ask

After producing the enhanced prompt, ask the user EXACTLY:

> **Submit this enhanced version (s), edit first (e), or scrap (x)?**

Wait for their response. Do NOT proceed without explicit confirmation.

## Step 6 — Act on the choice

### If user answers "s" (submit)

Treat the **enhanced prompt** as the actual instruction. Begin executing
the goal using the suggested approach. Invoke listed skills in order.
Apply listed constraints. Verify against success criteria before
claiming done.

### If user answers "e" (edit)

Wait for the user's revisions. They might:

- Add/remove items from scope
- Tighten or relax success criteria
- Answer the implicit assumption questions
- Reword the goal

After they reply, treat their revised version as the actual instruction
and proceed as in "s".

### If user answers "x" (scrap)

Discard the enhancement. Fall back to the **original rough intent**
verbatim. Proceed without the enhancement, treating the user's original
text as the instruction.

### If user answers something else

They've provided revisions or follow-up. Interpret intelligently and
proceed.

## Anti-patterns (do NOT do these)

- ❌ Auto-submit the enhanced prompt without user approval
- ❌ Lose the original rough intent verbatim — preserve it always
- ❌ Pad the enhanced prompt with generic best-practices that don't
  apply to the specific intent (e.g., don't add "implement
  comprehensive error handling" to a CSS tweak)
- ❌ Hallucinate file paths — if you can't find the relevant files via
  codemap/Serena/grep, say so explicitly rather than inventing
- ❌ Cite lesson IDs that don't exist — only reference real entries in
  `~/.claude/lessons/`
- ❌ Add 50 success criteria for a 5-line change — match density to
  the actual scope of the work
- ❌ Treat enhancement as a way to expand scope — it surfaces hidden
  scope, doesn't add unrequested scope

## Graceful degradation

This skill works in three tiers depending on what's available:

- **Tier A (full):** codemap + lessons + CLAUDE.md + Serena → produces
  fully codebase-aware enhanced prompt with real file references and
  cross-referenced lessons
- **Tier B (partial):** lessons + CLAUDE.md only → produces structured
  prompt with applicable lessons but generic file references
- **Tier C (minimal):** no codemap, no lessons, no Serena → produces
  structurally-improved prompt using only prompt-engineering principles
  (intent class, goal, scope, success criteria, assumptions)

In Tier C, mark the output as "no project context loaded — enhancement
based on prompt engineering principles only" so the user knows what
they're getting.

## Why this exists

Prompt quality is a force multiplier. A vague prompt produces guessing;
a structured prompt produces aligned execution. This skill applies
real prompt engineering principles (Anthropic's prompt design
guidelines, scope boundaries, success criteria, explicit assumption
surfacing) to lift rough developer intent into something a
distinguished engineer would actually act on.

Specifically, this skill closes the gap between:

- "fix the bug" (rough intent — multiple interpretations)
- "fix the area-computation bug in apps/api/src/fields/area.service.ts
  for self-intersecting polygons; preserve historical values; add
  regression test for the bowtie case from issue #142" (enhanced —
  one interpretation)

## For users distributing this as a plugin

This skill is portable. It uses standard locations:

- `~/.claude/lessons/` (optional — lessons cross-reference)
- `~/.claude/memory/_global/MEMORY.md` (optional — universal preferences)
- `<project>/.codemap/` (optional — project context)
- `<project>/CLAUDE.md` (optional — project conventions)
- Serena MCP (optional — semantic codebase queries)

If none of these exist, the skill operates in Tier C (prompt
engineering principles only) and still produces value.

To distribute as a plugin:

1. Copy this `SKILL.md` to your plugin's skills directory
2. Document the optional dependencies (codemap, lessons, Serena)
3. Provide a setup script that bootstraps the optional pieces if
   desired

The skill itself is self-contained — no hardcoded paths to specific
projects, no project-specific assumptions.
