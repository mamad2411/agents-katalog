---
name: skill-forge
description: Crystallize a captured workflow journal into a validated Claude skill. Use this whenever the user says "turn this into a skill", "make this repeatable", "build a skill from this", or when a workflow-capture worklog is ready to become a skill. Also use to improve or extend an existing produced skill from a new worklog.
---

# Skill Forge

Turn a WORKLOG.md into a skill. The journal's tags map directly onto skill sections, so synthesis is mostly routing.

## Step 1: Read the worklog

Read the full `_worklogs/<date-slug>/WORKLOG.md`. If the user references a workflow without a path, find the matching worklog.

## Step 2: Route by tag

- DECISION + SEQUENCE -> the procedure: ordered, imperative steps.
- CORRECTION + DEADEND -> guardrails: "do not", "always", warnings, each with the one-line reason.
- CONVENTION + DISCOVERY -> reference files and compatibility notes.

A DEADEND that blocked progress usually becomes an early SEQUENCE step in the procedure so it cannot recur.

## Step 3: Draft SKILL.md

Read `references/skill-anatomy.md` first. Then produce:

- name: kebab-case identifier.
- description: the trigger. Make it pushy and list concrete contexts; Claude tends to undertrigger skills. Put all "when to use" info here, not in the body.
- body: imperative voice, under ~500 lines. Explain why a rule matters rather than stacking bare MUSTs.
- references/: push variant-specific or long details out of the body. Files over ~300 lines get a table of contents.
- scripts/ and assets/ only if the workflow has deterministic steps or output templates.

## Step 4: Validate

Adapt to the environment.

- Subagents available (e.g. Claude Code): run 2 to 3 realistic test prompts, baseline vs with-skill, grade, review the results.
- No subagents (e.g. a chat client): run test prompts inline, one at a time, using the skill yourself. Skip quantitative benchmarking; rely on qualitative review.

Iterate: run -> review -> revise SKILL.md -> rerun. Optimize the description for triggering once stable.

## Step 5: Archive and link

Move the source worklog to `skills/<name>/.source/WORKLOG.md` for provenance. Archive, never delete. Symlink or copy the produced skill into the runtime skill path so it loads.

## Step 6: Package (if available)

If a packaging script is available, package the skill and hand back the artifact path.
