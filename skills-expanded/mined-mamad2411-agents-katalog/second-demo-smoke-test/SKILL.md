---
name: second-demo-smoke-test
description: Use when verifying that mtmskills can expose multiple skills, testing agent skill discovery lists, or demonstrating a second minimal portable agent skill.
---

# Second Demo Smoke Test

## Overview

Use this skill as a second smoke test for the mtmskills repository. It proves that an agent can discover more than one skill, load its `SKILL.md`, and follow a short instruction set.

## Demo Response

When this skill is invoked, answer with:

1. A one-sentence confirmation that `second-demo-smoke-test` was loaded.
2. The current task summary in one sentence.
3. A short checklist showing:
   - `SKILL.md` frontmatter was readable.
   - No scripts, assets, or external services are required.
   - No external systems were changed.

## Boundaries

Do not run commands, call network services, modify files, or inspect secrets for this demo unless the user explicitly asks for a separate task that requires it.
