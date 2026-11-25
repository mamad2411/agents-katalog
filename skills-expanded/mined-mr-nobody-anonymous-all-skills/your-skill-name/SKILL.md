---
name: your-skill-name
description: Healthcare-focused skill for <replace-this>. Use when an agent needs support with <replace-this>, especially in healthcare software, digital health product, clinical workflow, interoperability, privacy, security, or operational contexts.
source: "https://github.com/reason-healthcare/health-skills"
source_repository: "reason-healthcare/health-skills"
source_path: "templates/skill/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Your Skill Name

## Overview

State what this skill enables and the healthcare context it is designed for.

## Workflow

1. Confirm the healthcare or product context.
2. Identify the specific task, artifact, or decision to support.
3. Use references or scripts only when the task needs deeper guidance or deterministic execution.
4. Produce an output that is concrete, reviewable, and scoped to the request.

## Constraints

- Stay within the scope described in the frontmatter.
- Surface domain risks, assumptions, and safety concerns clearly.
- Do not load detailed references unless they are needed.

## Resources

- `references/`: domain-specific guidance for conditional loading
- `scripts/`: deterministic helpers
- `assets/`: templates or output artifacts
- `examples/`: representative sample output artifacts

## Output Contract

- Describe the expected shape of the response or artifact.
