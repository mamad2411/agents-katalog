---
name: skill-cross-reference-audit
description: Automated audit of the skill library for cross-reference issues — detects skill names duplicated in Composition and Related Skills sections, missing AGENTS.md, missing YAML frontmatter, empty Related Skills, and missing Related Skills in skills that have Composition sections.
category: General-Development
---

# Skill Cross-Reference Audit (v1)

> **Skill ID:** `skill-cross-reference-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This skill is a **base skill** — it owns the mechanical primitive of scanning
every SKILL.md in the skill library and reporting structural cross-reference
issues. It does NOT fix the issues (that requires human judgement). It provides
a deterministic, reusable report that:

- The [`skill-factory`](../skill-factory/SKILL.md) consumes in its Post-Drafting
  Checklist (§3 — Composition Audit step) to verify a new skill didn't introduce
  duplication or missing sections.
- Library maintainers run periodically to detect drift across the skill graph.
- Skill authors run before declaring a new skill complete.

## Environment & Dependencies

| Requirement | Minimum | Notes |
|---|---|---|
| Python 3 | 3.10+ | `python3` on PATH |
| `re` module | stdlib | Regex-based section parsing |
| `json` module | stdlib | Output formatting |
| Read permission | — | To read all SKILL.md files under `.agents/skills/` |

Verification:
```bash
python3 -c "import re, json, sys, argparse; print('OK')"
```

## When to Use

- After creating or modifying a skill, to verify no cross-reference issues were introduced.
- Before committing changes to the skill library, as a pre-commit sanity check.
- After renaming a skill, to confirm all references are updated.
- Periodically (weekly/monthly) as a library health scan.
- When running the [`skill-factory`](../skill-factory/SKILL.md) Post-Drafting
  Checklist, specifically the Composition Audit step.

## Operational Logic

### Step 1 — Run the audit

```bash
python3 scripts/audit-cross-refs.py [--skills-dir .agents/skills]
```

The script scans every directory containing a `SKILL.md` and checks:

1. **Duplicate in Composition + Related Skills**: A skill name appears in both
   a Composition table (`## Composition by Higher-Level Skills`,
   `## Called Base Skills`, or `## Composition Rationale`) AND the
   `## Related Skills` list. The name belongs in only one place — Composition
   (stronger relationship) or Related (looser association).

2. **Missing AGENTS.md**: A skill directory has a `SKILL.md` but no
   companion `AGENTS.md` bridge file. Per skill-factory §2.3, every skill
   MUST have a bridge.

3. **Missing YAML frontmatter**: A `SKILL.md` does not start with
   `---\n` + YAML block. Per skill-factory §2.2, every skill MUST have
   frontmatter (`name:`, `description:`, `category:`).

4. **Empty Related Skills section**: A `## Related Skills` heading exists
   but contains no content (only blank lines) before the next heading.
   Remove the empty heading.

5. **Missing Related Skills section**: A skill has a Composition section
   but no `## Related Skills` section at all. Per skill-factory's
   Composition Audit, bidirectional discoverability requires both.

### Step 2 — Review the report

Human-readable output:

```
Audited: 223 skills in .agents/skills
Issues found: 12

  [3] Duplicate In Composition And Related:
    - git-absorbed-branch-decommission: git-branch-promotion, git-divergence-audit
    ...

  [0] Missing Agents Md: NONE

  [5] Missing Yaml Frontmatter:
    - github-repo-templates
    ...
```

### Step 3 — Fix issues

Each category requires a different fix:

| Issue | Fix |
|---|---|
| Duplicate in Composition + Related | Remove the name from Related Skills (keep it in Composition — stronger relationship) |
| Missing AGENTS.md | Create per skill-factory §2.3.2 template |
| Missing YAML frontmatter | Add `---\nname: ...\ndescription: ...\ncategory: ...\n---` at line 1 |
| Empty Related Skills | Remove the `## Related Skills` heading entirely |
| Missing Related Skills | Add a `## Related Skills` section with relevant cross-references |

### CLI flags

| Flag | Purpose |
|---|---|
| `--skills-dir PATH` | Scan a different skills root (default: `.agents/skills`) |
| `--skill-names NAME [NAME ...]` | Only report issues for skills matching the given names |
| `--json` | Output as JSON for programmatic consumption |

## Output format (JSON)

```json
{
  "duplicate_in_composition_and_related": [
    {"skill": "git-absorbed-branch-decommission", "path": "...", "duplicates": ["git-branch-promotion", "git-divergence-audit"]}
  ],
  "missing_agents_md": [],
  "missing_yaml_frontmatter": [{"skill": "github-repo-templates", "path": "..."}],
  "empty_related_sections": [],
  "missing_related_sections_with_composition": [{"skill": "github-ci-lint", "path": "..."}]
}
```

Exit code: `0` if no issues, `1` if issues found.

## SSOT Compliance

- The **skill structure requirements** (YAML frontmatter, AGENTS.md bridge,
  Composition/Related sections) are defined in
  [`skill-factory` §2.2–§2.3](../skill-factory/SKILL.md#22-skillmd-composition) —
  this skill does NOT redefine them, it audits compliance.
- The **Post-Drafting Checklist steps** are owned by
  [`skill-factory` §3](../skill-factory/SKILL.md#3-post-drafting-checklist).
- The **8±2 organization principle** is owned by
  [`human-scanable-organization`](../human-scanable-organization/SKILL.md).

## Related Skills

- [`script-template-extraction`](../script-template-extraction/SKILL.md) —
  companion base skill for template extraction; run this audit after extraction
  to verify the skill graph is clean.
- [`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md) —
  the decomposition pattern this skill's audits support.
- [`human-scanable-organization`](../human-scanable-organization/SKILL.md) —
  the 8±2 principle that governs skill folder organization.
- [`directory-tree-audit`](../directory-tree-audit/SKILL.md) — sibling audit
  skill for folder depth / item counts.

## Related Conversations

- Audit and cross-reference fix session — `docs/conversations/cross-reference-audit.md`
  (pending redaction pass before commit).
