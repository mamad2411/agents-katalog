---
name: agentic-skill-pack-integrator
description: Convert external AI skill packs, prompt packs, Claude skills, Codex skills, Cursor rules, Windsurf rules, Cline/Roo workflows, and CLI agent instructions into OutcomeLab-compatible skill frameworks with metadata, safety gates, evaluation rubrics, benchmark plans, and compatibility notes. Use when importing or upgrading skill collections for Codex, Claude Code, ChatGPT, Gemini, Cursor, Windsurf, Cline, Roo Code, Aider, or Antigravity-style agentic IDEs.
---

# Agentic Skill Pack Integrator

Developed by the LetsCookTech Open Source Team.

Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md) for evidence, verification, risk, benchmarking, and improvement.

Turn raw skill packs into portable, production-grade AI operating skills. Preserve license requirements, remove filler, normalize metadata, add safety boundaries, and create evaluation paths.

## Workflow

1. Inventory the source pack: skill names, descriptions, licenses, required tools, environment variables, network requirements, scripts, assets, and supported clients.
2. Classify each item as direct import, wrapper skill, reference-only material, duplicate, unsafe, vendor-specific, or reject.
3. Normalize names to lowercase hyphen-case and create concise `SKILL.md` frontmatter with clear trigger conditions.
4. Convert long instructions into progressive disclosure: keep `SKILL.md` operational and move deep details into references only when needed.
5. Add compatibility notes for Codex, Claude Code, ChatGPT, Gemini, Cursor, Windsurf, Cline, Roo Code, Aider, CLI installers, and Antigravity-style agentic IDEs.
6. Add safety gates for secrets, credentials, production writes, destructive operations, network calls, vendor credentials, and user authorization.
7. Add proof artifacts: rubric, failure patterns, comparison template, and benchmark plan before claiming superiority.
8. Validate structure, remove temp/vendor noise, and report what was imported, adapted, skipped, and why.

## Output contract

Return source inventory, imported skills, wrapper skills, skipped files with reasons, license notes, client compatibility matrix, safety boundaries, benchmark plan, validation result, and next improvement list.

When writing repository files, create only maintainable OutcomeLab assets. Do not commit extracted archives, private certs, vendor caches, generated lock noise, or unreviewed large assets.

## Quality gates

- No skill is accepted without clear trigger metadata, workflow, output contract, and quality gates.
- No vendor content is copied without license compatibility and attribution.
- No executable script is trusted without inspection and a safe test path.
- No production action is automated without permission, rollback, and human review.
