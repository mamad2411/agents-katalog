---
name: rewrite
description: Rewrite prompts using proven prompt engineering frameworks — select from 20 curated frameworks or provide a custom template, then get a structured rewrite via a fast sub-agent.
metadata:
  author: Biswajit Sahoo (https://github.com/IamBiswajitSahoo)
  license: Apache-2.0
argument-hint: '"your prompt here"'
---

# Rewrite

Rewrite the user's raw prompt (`$ARGUMENTS`) into a structured version using a prompt engineering framework. All reasoning is delegated to haiku sub-agents to keep main-session context lean.

## Phase 1 — Capture prompt and context

- If `$ARGUMENTS` is non-empty, use it as the original prompt.
- If empty, ask via `AskUserQuestion`: *"What prompt would you like to rewrite?"* — AskUserQuestion requires ≥2 options, so use placeholders **"Type my prompt"** and **"Paste from clipboard"**. The user types into the "Other" field; use that text.
- **Capture conversation context.** Before delegating, write a short `CONTEXT SUMMARY` (≤150 words) drawn from the current session: what the user is working on, relevant files/tech, prior decisions, and any constraints the user has stated. If the skill was invoked at the start of a session with no prior turns, set `CONTEXT SUMMARY: (none — fresh session)`. Never fabricate context — only include what was actually discussed.
- This summary is passed to both the recommender (Phase 2 Step 0) and the rewriter (Phase 3) so framework choice and rewriting reflect the real task, not just the prompt text in isolation.

## Phase 2 — Select framework

Flow: **recommend first, browse if needed.** Happy path = 1 question.

**Standalone install** (no `bix-utils:rewrite:*` agents available): for both sub-agent calls below, launch `general-purpose` with the same `model` and prompt, prefixed with "Read `${CLAUDE_SKILL_DIR}/references/agents/<name>.md` and follow it as your instructions", where `<name>` is `recommender` or `rewriter`.

### Step 0 — Recommendation (sub-agent)

Invoke **Agent** with `subagent_type: "bix-utils:rewrite:recommender"`, `model: "haiku"`, `description: "Recommend prompt framework"`, and `prompt`:

```
CONTEXT SUMMARY:
{context_summary}

---
ORIGINAL PROMPT:
{original_prompt}
```

The sub-agent has its own catalog — do not add extra instructions.

It returns exactly:

```
PRIMARY: <name>
PRIMARY_REASON: <sentence>
RUNNER_UP: <name>
RUNNER_UP_REASON: <sentence>
```

If parsing fails or names don't match the catalog, skip to Step 1 (browse).

Otherwise ask via `AskUserQuestion`: *"Based on your prompt, I recommend **{PRIMARY}**. How would you like to proceed?"*

| # | Label | Description |
|---|---|---|
| 1 | **Use {PRIMARY} (recommended)** | {PRIMARY_REASON} |
| 2 | **Use {RUNNER_UP} instead** | {RUNNER_UP_REASON} |
| 3 | **Browse all frameworks** | See all 20 organized by category |
| 4 | **Custom / Skip** | Own template, or use prompt as-is |

Options 1/2 → Step 3. Option 3 → Step 1. Option 4 → Custom / Skip branch below.

### Step 1 — Pick a category (browse)

Ask: *"Which type of framework fits your prompt?"*

| # | Category | Frameworks |
|---|---|---|
| 1 | **Core Structured** | RISEN, TIDD-EC, CRAFT, APE — general-purpose scaffolds, 80% of tasks |
| 2 | **Content & Communication** | CO-STAR, K.E.R.N.E.L., BAB — audience writing, validation, transformation |
| 3 | **Reasoning** | Chain of Thought, Tree-of-Thought, Plan-and-Solve, Self-Refine, Skeleton-of-Thought |
| 4 | **Expert & Creative** | RACE, CRISPE, SCRIBE, C.R.E.A.T.E. — personas, variants, dialogue, creative |
| 5 | **Quick & Clarify** | RTF, Step-Back, Chain-of-Density, Reverse-Role |
| 6 | **Custom / Skip** | Own template, or use prompt as-is |

### Step 2 — Pick a framework

Ask *"Select a framework:"* with the rows for the chosen category:

**Core Structured** — RISEN (multi-step structured; safe default) · TIDD-EC (precision/code with do/don't rules) · CRAFT (general; tone + format) · APE (minimal 3-part scaffold)

**Content & Communication** — CO-STAR (audience-sensitive writing: emails, pitches, posts) · K.E.R.N.E.L. (meta-validation checklist for existing prompts) · BAB (before/after transformations, migrations)

**Reasoning** — Chain of Thought (analysis, debugging, root-cause) · Tree-of-Thought (multiple solution branches, pick winner) · Plan-and-Solve (numbered plan then execute; order matters) · Self-Refine (draft → critique → revise; quality-sensitive) · Skeleton-of-Thought (outline then expand; long structured outputs)

**Expert & Creative** — RACE (fast expert persona) · CRISPE (multiple output variants) · SCRIBE (iterative dialogue/interview) · C.R.E.A.T.E. (creative with tight style control)

**Quick & Clarify** — RTF (Role·Task·Format; minimum scaffold) · Step-Back (abstract first, apply second) · Chain-of-Density (dense summaries of long docs) · Reverse-Role (model interviews you; vague requests)

**Custom / Skip** — ask:

| # | Label | Description |
|---|---|---|
| 1 | **Custom template (file)** | Provide a path to a .md/.txt template — read with `cat` |
| 2 | **Custom template (text)** | Paste template text directly |
| 3 | **Skip rewriting** | Echo the original prompt in a code block, state *"Original prompt passed through without rewriting."*, and **stop** — do not proceed to Phase 3 |

### Step 3 — Load template

For named frameworks, read `${CLAUDE_SKILL_DIR}/templates/{key}.md` where `{key}` is the framework name lowercased with spaces/dots replaced by dashes (e.g., `RISEN` → `risen`, `C.R.E.A.T.E.` → `create`, `K.E.R.N.E.L.` → `kernel`, `Chain of Thought` → `chain-of-thought`, `TIDD-EC` → `tidd-ec`).

## Phase 3 — Rewrite (sub-agent)

**You MUST delegate — never rewrite inline.** Invoke **Agent** with `subagent_type: "bix-utils:rewrite:rewriter"`, `model: "haiku"`, `description: "Rewrite prompt: {framework}"`, and `prompt`:

```
Rewrite the following user prompt using the framework template below. Output ONLY the rewritten prompt.

---
CONTEXT SUMMARY:

{context_summary}

---
ORIGINAL PROMPT:

{original_prompt}

---
FRAMEWORK TEMPLATE:

{template_text}
```

Display the result to the user:

> **Rewritten using {framework}:**
>
> ```
> {rewritten_prompt}
> ```

## Phase 4 — Confirm

Ask *"How would you like to proceed with the rewritten prompt?"*

| # | Label | Description |
|---|---|---|
| 1 | **Use this prompt** | Main session acts on it → Phase 5 |
| 2 | **Try another framework** | Loop back to Phase 2 Step 0, preserving the original prompt |
| 3 | **Edit first** | Ask *"What changes would you like?"*, apply, re-display, repeat this question |

## Phase 5 — Handoff

Output plain text (no code fence) so the main session interprets it as instructions:

> Now executing the rewritten prompt:

Then the rewritten prompt verbatim.

## Rules

- **Delegate, never inline.** Both the recommender (Phase 2 Step 0) and the rewriter (Phase 3) must run in sub-agents. The 20-framework catalog and rewrite reasoning must never enter main-session context.
- **Preserve intent.** Rewriting restructures and clarifies; it does not add requirements or change goals.
- **Always present for approval** (Phase 4) before handoff.
- **Question budget:** happy path = 1 question (accept recommendation). Browse mode = 2 questions (category → framework). Do not add extra tiers.
- **On sub-agent error or empty result:** tell the user and offer to try a different framework.
- **Skip rewriting** ends the skill after echoing the original prompt.
