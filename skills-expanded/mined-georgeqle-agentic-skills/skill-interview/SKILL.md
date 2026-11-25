---
name: skill-interview
description: Interview the user to define the characteristics of a skill they want created
type: planning
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[skill-name-or-topic]"
context_intake: deep
---

# Skill Interview

Invoke as `$skill-interview`.

Use this skill when the user wants to create or substantially redesign a skill but the desired behavior, scope, triggers, outputs, validation, or agent compatibility is not yet clear. This skill interrogates the user and turns the answers into a creation-ready skill brief. It does not create the skill itself; route to `$create-agentic-skill`, `$create-local-skill`, or `$targeted-skill-builder` after the brief is complete.

## Process

1. **Identify the target skill idea.**
   - Treat the user's initial request as a draft, not a complete requirement.
   - Resolve the likely skill name in kebab-case when possible.
   - If the request is a correction to an existing workflow gap, consider whether `$targeted-skill-builder` is a better next route after the interview.
   - If the user wants an experimental personal skill under `~/.codex/skills`, plan for `$create-local-skill`; otherwise default to repo-managed `$create-agentic-skill`.

2. **Gather local evidence before probing.**
   - Search for overlapping skills in the active skill list and repository paths such as `base/codex/`, `base/claude/`, and `packs/*/{codex,claude}/`.
   - Read the closest existing skill contracts and any relevant `tasks/lessons.md` entries before asking detailed questions.
   - If an existing skill already covers the request, explain the overlap and ask whether the user wants an update, alias, narrower variant, or new skill.

3. **Surface a lightweight assumptions checkpoint.**
   - Before deep probing, present 3 to 7 assumptions most likely to affect the skill contract.
   - Tag each assumption:
     - `[from request]` — explicitly stated by the user
     - `[from existing skill]` — derived from a current skill contract
     - `[from lessons]` — derived from `tasks/lessons.md`
     - `[from codebase]` — derived from repository conventions or test harnesses
     - `[inferred]` — a default judgment that needs confirmation
   - Bias toward assumptions that affect trigger rules, allowed side effects, deliverables, verification, benchmarkability, and next-step routing.
   - Deliver the checkpoint inline as the final message text of its own turn — never only as mid-turn text in a turn that ends with a tool or command call. In the next turn, ask the user to confirm or correct it together with one focused interview question so momentum is kept.
   - If an `[inferred]` assumption is corrected, preserve the correction in the interview log and final brief.

4. **Interview one material decision at a time.**
   - Codex cadence: ask one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same decision.
   - If already in Plan mode, `request_user_input` may present 2 to 3 real options for the current material decision. Otherwise ask one concise direct question in plain text.
   - Research and recommend by default: use local codebase evidence and, when the user requests current external facts, web evidence before asking the user to choose.
   - For each material choice, explain the options, recommend one, and ask the user to approve, adjust, or override.

5. **Cover the skill characteristics completely.**
   - Continue until the brief captures:
     - Skill name and one-line description
     - Target location: repo-managed, local-only, pack-local, Codex-only, Claude-only, or mirrored
     - Trigger rules and explicit non-triggers
     - Inputs and argument syntax
     - Required evidence gathering before questions or edits
     - Interview cadence or execution workflow
     - Deliverables and file paths
     - Side-effect permissions and safety constraints
     - Verification and benchmark coverage strategy
     - Next-step routing after successful completion
     - Relationship to overlapping skills
   - For mutation-capable skills, explicitly define whether the skill should commit and push by default.
   - For repo-managed skills, include benchmark coverage expectations in the brief.

6. **Coverage checkpoint.**
   - Before concluding, summarize each covered area with the decision made and source evidence, delivered inline as the final message text of its own turn.
   - In the next turn, ask: "Does this cover the skill you want, or is there any behavior, boundary, or output we should revisit?"
   - Do not write final deliverables until the user confirms the checkpoint or provides final corrections.

7. **Write deliverables.**
   - Create `specs/[skill-name]-skill-brief.md` with:
     - `## Overview`
     - `## Goals`
     - `## Non-Goals`
     - `## Skill Contract`
     - `## Workflow`
     - `## Inputs and Outputs`
     - `## Safety and Side Effects`
     - `## Verification and Benchmark Coverage`
     - `## Related Skills`
     - `## Open Questions`
     - `## Assumptions & Risks`
     - `## Recommended Creation Route`
   - Create `specs/[skill-name]-skill-interview.md` with:
     - Assumptions checkpoint and corrections
     - Questions asked
     - Options and recommendations presented
     - User responses and decisions
     - Deviations from the initial request
   - If the repository uses another canonical specification directory, use that directory and note the path.

## Next-Step Routing

After writing the brief and interview log, recommend exactly one next command:

- `$create-agentic-skill <skill-name>` for repo-managed base skills.
- `$create-local-skill <skill-name>` for personal local-only skills.
- `$targeted-skill-builder <existing-skill> <gap>` when the interview found that an existing skill should be updated instead of creating a new skill.
- `$init-agentic-skills` (guided pack setup) or a pack-local creation route when the skill belongs inside a project-local pack rather than base skills.

Output exactly two lines beyond the normal report:

- **Next work:** <specific skill creation or update task>
- **Recommended next command:** <one command>

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/skill-interview-{topic}.html`.

## Constraints

- Do not create or edit the final `SKILL.md` during the interview unless the user explicitly asks to skip the brief and create the skill now.
- Do not assume a new skill is needed when an existing skill update would satisfy the workflow gap.
- Do not batch unrelated interview questions.
- Do not invent benchmark coverage; if deterministic local coverage is unsafe or impractical, mark the coverage plan as blocked with a reason and next command.
- Keep the final brief implementation-ready enough that `$create-agentic-skill` or `$create-local-skill` can execute without re-interviewing the same decisions.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

