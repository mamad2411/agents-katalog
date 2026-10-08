---
name: self-evolution-engine
description: Pipeline for synthesizing, quarantine-testing, versioning, and registering new skills into the ecosystem. Use when a capability gap is found mid-task, when the user asks to "evolve a new skill", "create a skill for X", "the agent needs a new tool/skill", when a recurring workflow should be captured, or when deduplicating/upgrading existing skills. Also use for auditing the skill library for overlap or stale versions.
license: MIT
compatibility: No special requirements
metadata:
  author: villain
  version: "1.0"
---

# Self-Evolution Engine

Ports the `evolve-new-skill` workflow. The agent modifies its own skill set through a gated pipeline — never by ad-hoc file writes. Canonical registry: `agent/skills/` (via `list_skills` / `evolve_skill`).

## Pipeline

### 1. Dedupe scan (always first)

Before creating anything, scan for semantic duplicates:

- Call `list_skills` (or `Glob agent/skills/*/SKILL.md`) and read every `name` + `description`.
- Also check the built-in skill list in the system prompt — never shadow a built-in skill name.
- Decision: **extend** an existing skill (add a reference file or section) beats **create** a new one whenever the domain overlaps >50%. Duplicated skills split trigger probability and both undertrigger.

### 2. Research & scaffold

- Pull real patterns from the current conversation/codebase first; web research second. Skills grounded in observed corrections beat skills written from imagination.
- Follow the `skill-creation` skill for frontmatter rules and body guidelines. Description carries all trigger weight — write it generous with trigger phrases.
- Scaffold to a **quarantine path** first via `evolve_skill` (`agent/skills/_quarantine-{name}/SKILL.md`). Quarantined skills use the `_quarantine-` prefix so they are visually distinct and never confused with registered ones.

### 3. Quarantine test

A skill passes quarantine when:

- Frontmatter validates (MUST include name, description, license, compatibility, metadata version & author).
- Must have all 5 directories (`scripts/`, `references/`, `assets/`, `examples/`) even if empty with `.gitkeep`.
- **Trigger test**: write 3 realistic prompts that SHOULD fire it and 2 that should NOT; verify the description discriminates them.
- **Dry run**: apply the skill's instructions to a real sample task in the current project; the output must be correct without needing information the skill omits.
- Body < 500 lines; overflow moved to `references/`.

Failures loop back to step 2. Two consecutive failures → stop, report the gap to the user instead of force-registering a bad skill.

### 4. Version & register

- Add version metadata to frontmatter:
  ```yaml
  metadata:
    version: "1.0.0"
    created: "YYYY-MM-DD"
    source: "evolved from <task/conversation context>"
  ```
- Rename directory from `_quarantine-{name}` to `{name}` (Move each file). The registry directory is the single source of truth — no copies elsewhere.
- Bump semver on later edits: patch = wording, minor = new sections/references, major = changed trigger scope.

### 5. Record outcome

Call `record_outcome` (or append one line to `agent/memory/skill-outcomes.md`):
`| date | skill | created|extended|rejected | reason |`
This log feeds `skill-orchestrator` reinforcement and future dedupe scans.

## Upgrade & Prune Path

When invoked for library maintenance: read all registered skills, flag pairs with overlapping descriptions for merge, flag skills never referenced in `skill-outcomes.md` after 10+ entries as prune candidates, and propose (don't auto-delete) removals to the user.
