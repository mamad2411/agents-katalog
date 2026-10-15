---
name: how-to-write-skills
description: >-
  Helps create and refine portable, self-contained agent skills. ALWAYS USE when
  creating or editing a SKILL.md, reviewing skill frontmatter or instructions,
  or improving discoverability, triggering, portability, or skill structure.
license: MIT
metadata:
  focus: portable-skill-authoring
---

# How To Write AI Skills

## Overview

Write skills as compact, reusable guidance for a smart and capable model.

Default to a self-contained `SKILL.md`. Keep the skill portable, concise, and easy to trigger.

## Default Approach

- Prefer one self-contained `SKILL.md`.
- Keep the skill high level by default. Give recommendations, decision rules, and good defaults rather than rigid scripts.
- Use strict rigid step-by-step instructions only when the user explicitly asks for them or the task is fragile enough that ambiguity is likely to cause failure.
- Avoid teaching basics the model already knows.
- If the skill is growing too large, first cut repetition and boilerplate. If it is still too large, move heavy reference material or reusable tools into separate files only when they are clearly justified. Split into multiple skills only when the responsibilities are genuinely different.

## Frontmatter

Use portable frontmatter first.

- `name`: lowercase kebab-case, matches the directory name.
- `description`: say what the skill does and when to use it.

- Prefer folded YAML such as `description: >-` instead of one very long line.

Hard constraints:

- Keep `description` within the platform's limits. `1024` characters is a safe default.
- Avoid XML angle brackets in frontmatter.
- Do not use reserved names such as `claude` or `anthropic` in the skill name.
- Use `compatibility` only for concrete platform or environment requirements, not as a general slogan.

Write `description` for discovery, not for marketing.

- Assume the agent sees ONLY directory name, `name`, and `description` before invocation.
- Assume the body is ONLY post-invocation guidance.
- Put invocation guidance in `description`, not in the body.
- Keep `description` focused on when to load. Put detailed instructions and decision rules in the body.

- Put the main use case early.
- Include words users would actually say.
- Mention concrete tasks, artifacts, file types, symptoms, or domains when relevant.
- Keep it specific enough to trigger correctly, but not so narrow that it misses obvious paraphrases.
- Keep it trigger-oriented. State the outcome and when to use the skill, but do not stuff it with workflow steps or process summaries.
- A strong default is a two-part description: first sentence gives the trigger, second sentence packs in task, domain, artifact, and tool keywords.

Good pattern:

```yaml
description: Helps create portable, self-contained agent skills with clear frontmatter and strong discoverability. Use when creating or editing a SKILL.md, refining skill instructions, or improving skill triggering.
```

Another good pattern:

```yaml
description: >-
  ALWAYS LOAD THIS SKILL WHEN ADDING LOGGING, CONFIGURING LOG OUTPUT, OR SETTING UP COLORLOG.
  Do not configure Python logging directly — use this skill first. Python logging, stdout/stderr behavior, rotating files, CLI vs GUI/server output.
```

Bad patterns:

```yaml
description: Helps with skills.
description: Use when doing agent things.
description: Writes the perfect skill by following a strict 12-step workflow with validation gates and advanced optimization.
```

## Writing the Body

Keep the body short and load-bearing.

- Start with the core principle and default approach.
- Explain non-obvious constraints, heuristics, or patterns.
- Prefer compact sections and short examples over long theory.
- Give one-two good defaults, not five equal options.
- If you include examples, make them realistic and directly reusable.

Optional sections that often help:

- `Overview`
- `Default Approach`
- `Frontmatter` or equivalent configuration guidance
- `Core Workflow` or `Decision Rules`
- `Common Mistakes`

## Discoverability

Discovery is part of the skill design.

When writing `name` and `description`, optimize for how another agent will find the skill later.

- Treat loading and behavior as separate design problems.
- The `description` should help the skill load for the right tasks.
- The body should tell the agent how strongly to apply the skill once loaded.
- Some skills should load broadly but apply flexibly. Others should load narrowly and be followed rigidly.

Important: body text cannot help a skill that did not load. If a rule is about invocation, trigger scope, or when to reach for the skill, put it in `description`.

Example: an `advanced-repo-research` skill should load for all `inspect upstream source` requests, but explain the agent when to use simple research vs advanced.

- Use descriptive names with real task words.
- Cover likely synonyms.
- Include concrete trigger phrases when they help.
- Mention failure symptoms when the skill addresses a problem.
- Mention specific tools, libraries, file types, or domains only when they are truly part of the trigger.
- Prefer literal task-shaped names and descriptions over abstract goals.
- Hard directives like `ALWAYS LOAD THIS SKILL WHEN X` are useful when you need to ensure a skill is consistently loaded for a clearly scoped class of work.
- Do not make entire body `UPPER CASE`, only initial phrase.
- You can adjust this to language of the skill, eg russian.
- Scope `X` tightly enough to avoid bad matches.
- Pair it with a second sentence such as `Do not do Y directly — read this skill first` when you need to steer the agent away from bypassing the skill.

Example: `ALWAYS LOAD THIS SKILL WHEN WORKING WITH PYSIDE6, QT, OR DESKTOP GUI CODE. Do not review or write PySide6 or Qt code directly — use this skill first.`

Think in terms of search terms an agent might match:

- user requests: `create skill`, `start backend`, `proceed to plan`
- artifacts: `SKILL.md`, `frontmatter`
- problems: `does not trigger`, `too vague`, `loads too often`
- goals: `portable`, `discoverable`, `self-contained`

Undertriggering signs:

- The skill does not load for obvious requests.
- Agents keep asking for guidance the skill should already provide.
- You need to invoke it manually for common matching tasks.

Overtriggering signs:

- The skill loads for adjacent but different tasks.
- The description is broad enough to match generic writing or documentation work.

If triggering is wrong, refine the description instead of editing body text.

Also verify that the skill is discoverable from the expected directory layout for the target agents. For supported agent paths, check:

- `https://github.com/vercel-labs/skills#supported-agents`

## Verification

Do not turn verification into ritual.

For simple skills, a small careful read by separate subagent is usually enough.

Match the verification effort to the risk. Use stronger checks when the main failure mode is triggering, discoverability, or behavior in realistic agent workflows.

Example: a tiny wording cleanup may only need a careful read, while a trigger-sensitive skill should usually get at least one realistic invocation test.

Use stronger verification only when the skill contains:

- non-trivial scripts or other code
- complex instructions
- brittle workflows
- decision logic that could be misread

In those cases:

1. Start with a cheap check: try a few prompts that should trigger the skill and a few that should not.
2. If the environment supports it, have a subagent or fresh reviewer try to use or review the skill.
3. Look at where the skill was misunderstood, skipped, or interpreted too narrowly or too broadly.
4. Fix the skill.
5. Repeat if the first verification exposed meaningful problems.

For skills where triggering matters, a realistic invocation test is often the most useful check:

- give a fresh agent a plausible task
- do not over-specify the workflow unless that is part of the requirement
- see whether the skill loads or is disclosed naturally
- check whether it changed the behavior you cared about, such as tool choice, escalation, or reporting

Example: ask a fresh agent to research an upstream package behavior from real sources, instruct it to report used skills and see whether it will use `advanced-repo-research` practices or not.

The goal is not formal TDD. The goal is to confirm that another agent can understand and apply the skill. And that it's instructions are correct.

## When Extra Files Make Sense

Default answer: they usually do not.

Keep the skill self-contained unless an extra file is meaningfully better outside the main markdown.

Good reasons:

- executable scripts
- templates the agent should fill in
- structured data or large tables better kept as data files
- external mutable artifacts that are part of the workflow, eg credentials.txt

Weak reasons:

- optional reading
- extra theory
- long examples that can be shortened
- reference docs that duplicate the main skill or are not explicitly linked from `SKILL.md`

If the skill depends on another file, say so explicitly and make the dependency obvious.

## Platform-Specific Notes

Platform means "AI agent program", eg claude code, opencode or codex.

Default to standard frontmatter for portability.

Only add platform-specific fields when the task clearly needs platform-specific behavior such as invocation control, subagent execution, tool permissions, or argument substitution.

Check current docs for the target host before adding those fields.

Useful references:

- Claude Code: `https://docs.anthropic.com/en/docs/claude-code/skills`
- OpenCode: `https://opencode.ai/docs/skills`

If portability matters, keep the core skill useful even after those fields are removed.

## Common Mistakes

- Explaining basics instead of the non-obvious parts.
- Writing a vague description that never triggers.
- Writing a broad description that triggers on unrelated tasks.
- Turning guidance into a rigid workflow without need.
- Splitting a small skill into too many files.
- Keeping a bloated skill instead of cutting or splitting it.
- Adding platform-specific frontmatter by habit instead of need.
- Assuming the agent will read optional extra files just because they exist.

## Final Check

Before finishing, quickly confirm:

- The skill is still concise.
- `name` and directory name match.
- `description` states what the skill does and when to use it.
- The core instructions are self-contained.
- Extra files are absent unless they serve a clear purpose.
- Verification level matches the skill's complexity.
