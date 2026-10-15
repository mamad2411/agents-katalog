---
name: skill-marketplace-creator
description: Create, curate, validate, and operate repositories or marketplaces for reusable AI agent skills. Use when designing a skill marketplace, scaffolding a public skill repo, converting domain knowledge into SKILL.md packages, defining skill quality gates, evaluating skill submissions, planning skill distribution, or building an agent-powered skill factory.
---

# Skill Marketplace Creator

Use this skill to build a skill ecosystem that is useful, trustworthy, and distribution-ready.

## Workflow

1. Identify marketplace shape: repo-only, static catalog, API-backed registry, private enterprise registry, or full community marketplace.
2. Read `references/marketplace-playbook.md` for architecture and quality gates.
3. Define the skill supply strategy: internal flagship skills, curated third-party skills, community submissions, or agent-generated drafts.
4. Require validation before publication: schema, trigger quality, safety, license, examples, and evals.
5. Produce concrete repo structure, governance, launch channels, and next 48-hour actions.

## Marketplace principles

- Start repository-first. GitHub is the first marketplace, trust surface, and contribution flow.
- Curate before scaling. A small set of excellent skills beats a huge undifferentiated directory.
- Keep content original. Distill workflows into Sylphx-owned structure, examples, and wording; do not copy or lightly paraphrase third-party writing.
- Make quality machine-checkable where possible.
- Separate skills from MCP tools: skills teach behavior; MCP servers provide capabilities.

## Output format

```text
Recommended shape: <repo-only | static catalog | API registry | full marketplace>

Repository layout:
<tree>

Quality gates:
- <gate>

Launch plan:
1. <action>
2. <action>
3. <action>

Risks:
- <risk and mitigation>
```

For repo validation scripts, inspect or run `scripts/check_skill_folder.py` if present.
