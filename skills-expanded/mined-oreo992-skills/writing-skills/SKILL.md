---
name: writing-skills
description: Use when creating, editing, validating, or publishing reusable Agent Skills, especially when converting agent-specific instructions into portable skills or when a skill must work across multiple agent runtimes.
---

# Writing Skills

## Overview

Writing skills is behavior design for future agents. A skill is successful only when an agent can discover it from metadata, load the right amount of context, and behave differently in the next real task.

Use test-driven documentation when possible: define the behavior, watch a baseline attempt fail, write the smallest skill that fixes the failure, then re-test under pressure.

## What Counts As A Skill

A portable Agent Skill is a directory that contains `SKILL.md` and optional supporting files:

```text
skill-name/
  SKILL.md
  references/
  scripts/
  assets/
```

Skills are reusable procedures, patterns, tools, or references. They are not session stories, one-off project notes, or generic advice that would be better handled by a checklist, validator, or ordinary documentation.

## Portability Rules

- Write for agents in general. Use "agent", "user", and "workspace" instead of product-specific identities.
- Keep platform-specific install paths out of `SKILL.md`. Put install examples in `README.md` if needed.
- Use relative file references such as `references/pressure-tests.md`.
- Do not assume one tool runtime unless the skill truly requires it. If a tool is required, state the requirement narrowly.
- Keep secrets, tenant names, internal hostnames, and private operational context out of publishable skills.
- Keep the main `SKILL.md` concise. Move long examples, API details, or test scenarios into `references/`.

## Frontmatter

Use YAML frontmatter with at least:

```yaml
---
name: writing-skills
description: Use when creating, editing, validating, or publishing reusable Agent Skills.
---
```

Rules:

- `name` should match the skill directory name.
- Use lowercase letters, numbers, and hyphens only.
- `description` should include concrete trigger conditions and searchable keywords.
- Do not put the whole workflow in the description. The description helps the agent decide whether to load the skill; the body teaches the behavior.

## Authoring Workflow

1. **Define the target behavior.**
   State what the future agent must do differently and when the skill should activate.

2. **Write pressure scenarios first.**
   Create 2-4 scenarios that would expose failure without the skill. For discipline skills, include pressure such as time, ambiguity, sunk cost, or authority.

3. **Observe the baseline.**
   Run a real agent trial when available. If that is not possible, document the expected failure and treat it as weaker evidence.

4. **Write the smallest useful skill.**
   Address the observed failure modes. Avoid adding broad theory that did not change behavior in testing.

5. **Verify with the same scenarios.**
   The agent should now choose the skill, follow it, and avoid the original failure.

6. **Refactor for discovery and context efficiency.**
   Tighten the description, move heavy material into references, remove platform assumptions, and close loopholes found during verification.

7. **Package and validate.**
   Check frontmatter, file references, secret exposure, and platform portability before publishing.

## Recommended Structure

Use this shape unless the skill needs something more specific:

```markdown
---
name: skill-name
description: Use when [trigger conditions, symptoms, and keywords].
---

# Skill Name

## Overview
One or two sentences with the core principle.

## When To Use
Concrete triggers and non-use cases.

## Workflow
Steps the agent should follow.

## Common Mistakes
Failure modes and corrections.

## References
Relative links to optional supporting files.
```

## Quality Checklist

- The skill teaches a reusable behavior, not a one-time story.
- The description is specific enough for discovery but does not replace the body.
- The main file is short enough to load comfortably.
- Supporting files are referenced only when needed.
- The skill does not assume a specific agent product, local directory, or private environment.
- Validation or pressure scenarios exist before publication.
- Public versions have been scanned for secrets and private context.

## References

Use [pressure-tests.md](references/pressure-tests.md) for test scenario patterns, genericity checks, and publication gates.
