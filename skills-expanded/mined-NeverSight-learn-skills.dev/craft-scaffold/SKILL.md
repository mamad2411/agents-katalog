---
name: craft-scaffold
description: Turn a rough idea into a structured prompt or skill scaffold with explicit objective, inputs, workflow, outputs, and a concrete file plan. Use this whenever the user wants to design a new prompt or skill, scaffold a skill-like workflow, mentions "scaffold," "blueprint," "structure," or "plan" for a prompt, or arrives with a vague request that needs to be shaped before implementation — even if they don't explicitly ask to scaffold.
---

# craft-scaffold

## Purpose

Turn a rough idea into a structured prompt or skill scaffold that is easy to implement, review, and reuse.

Scaffolding matters because vague requests produce vague artifacts. Separating goals, inputs, workflow, and outputs *before* writing the artifact makes the resulting prompt or skill far more reusable and far less brittle.

## Use this when

- the request is still vague
- a new skill or prompt family is being started
- a stable file plan is needed before editing the repo
- the current artifact mixes goals, constraints, and output shape

## Inputs

- brief idea or request
- intended agent or agents
- expected outcome
- constraints
- existing references if available

## Steps

1. Extract the real objective behind the request. Rough wording usually hides a cleaner goal — surface it in one sentence.
2. Separate goals, constraints, assumptions, and non-goals. Mixing these is the most common source of prompt drift.
3. Propose a clean structure for the target prompt or skill. Favor the simplest shape that can survive reuse.
4. Define the expected inputs, steps, and outputs. Be explicit enough that another agent could implement the artifact without guessing.
5. Suggest files to create or update. A concrete file list converts the scaffold into work.
6. Call out any unresolved decisions briefly. Only surface decisions that materially change the design.

## When the target is a skill (vs a prompt)

A prompt is a single file; a skill is a folder. That changes what the scaffold must decide:

1. **Shape of the plan.**
   - **Prompt scaffold** = a *section plan*: which of Role / Context / Task / Rules / Format / Examples to include, in what order, and what each carries.
   - **Skill scaffold** = a *file-tree plan* + `SKILL.md` outline. Decide which files exist before any of them are written.
2. **Files list, expanded.** For a skill, the "Files to create or update" section should enumerate concretely:
   - `skills/<name>/SKILL.md` (always required)
   - `skills/<name>/references/<file>.md` (only when detail would push SKILL.md past ~500 lines, or when a topic deserves progressive disclosure)
   - `skills/<name>/scripts/<file>.mjs` (only when the skill repeats deterministic work an agent would otherwise re-derive each invocation)
   - `skills/<name>/templates/<file>` (only when a well-crafted template adds value the agent cannot easily generate)
   Avoid pre-creating folders "just in case" — empty folders invite bloat. Add them in a later iteration when the need is real.
3. **Frontmatter is a first-class design artifact.** A skill's `name` and `description` are its triggering mechanism. The scaffold must draft a `description` that is trigger-oriented (what it does + *when* to invoke) and covers the non-obvious phrasings users might use. This has no analogue for prompts, which do not self-trigger.
4. **Size budget.** Target `SKILL.md` under ~500 lines. If the skill's job plausibly exceeds that, the scaffold should plan the split into `references/` at design time — not discover it mid-write.
5. **Progressive disclosure as a design decision.** Decide up front which content loads on every invocation (`SKILL.md` body) versus on demand (`references/`). Getting this wrong either inflates every context window or hides load-bearing detail from the agent.

Prompts skip items 2-5 entirely. Items 1 and 6 (open questions) apply to both.

## Output format

### Summary
A short paragraph describing what is being built and why.

### Scaffold
- objective
- target users or agents
- inputs
- workflow
- output format
- guardrails
- non-goals

For skill targets, also include a drafted `description` frontmatter line that (a) names what the skill does, (b) states when to invoke it, and (c) covers ≥ 2 distinct user phrasings or aliases. Prompts do not self-trigger; omit for prompt targets.

### Files to create or update
A concrete file list with one-line purpose per file. Each purpose names a task-specific responsibility — e.g. `classification taxonomy`, `urgency rubric`, `commit-parse regex` — not generic boilerplate.

### Open questions
1–3 items, or write "none — all decisions resolvable from the above" if none remain. Each item must name a decision that would change the architecture (scope cut, target split, reference-file boundary, trigger-criteria choice). Drop implementation nits (naming, format of a subfield, wording choices) — those belong in the eventual artifact, not the scaffold.

## Guardrails

- prefer the simplest structure that can survive reuse
- do not create too many top-level concepts
- keep the scaffold implementation-oriented
- avoid provider lock-in in the core structure

## Failure modes

- writing a scaffold so abstract that nobody knows how to start
- inventing a plugin system or framework before the asset itself works
- drowning the user in open questions instead of making reasonable assumptions
- copying another repo's structure instead of shaping one for the actual task

## Example

### Input
Create a reusable skill that helps improve prompts for Claude Code and Codex.

### Output

**Summary**
Create a cross-agent tuning skill that revises existing prompts with small, explicit edits.

**Scaffold**
- objective: improve prompts without rewriting them from scratch
- target agents: Claude Code, Codex
- inputs: current prompt, target improvement, constraints
- workflow: inspect, critique, edit, summarize changes
- output format: revised prompt, changelog, risks
- guardrails: keep intent stable, keep diffs minimal
- non-goals: provider-specific hacks

**Files to create or update**
- `skills/craft-tune/SKILL.md`
- `README.md` (add a row to the skill table)

**Open questions**
- Should examples live inside each skill file or in a shared examples folder?
