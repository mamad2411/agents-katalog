# Progressive Disclosure Skills

## Summary

**One-sentence:** Produces a skill-design spec authoring Claude Skills as a 3-level pyramid: frontmatter always-loaded, body on activation, references on explicit Read.

**One-paragraph:** Claude Skills auto-load frontmatter into context; body loads on keyword match; references load only on explicit Read. Designing skills as a 3-level pyramid defers context cost. This methodology emits a spec: frontmatter keyword set, body length target, reference layout.

**Ефективно для:** Claude Code user whose plugin scope is exploding because every skill body is 2K+ tokens.

## Applies If (ALL must hold)

- Authoring Claude Code skills (SKILL.md format).
- Plugin scope exceeds 20K tokens always-loaded.
- Skills have content that not every invocation needs.

## Skip If (ANY kills it)

- Single-tool skill with <500 tokens.
- Custom CLI commands (not skills).
- Throwaway prototype.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `skill-inventory.yaml` | list of {name, frontmatter_tokens, body_tokens, ref_count} | operator |
| `max_session_tokens` | integer | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-frontmatter-bounded; r2-body-keyword-triggered; r3-references-on-read; r4-triggers-precise; r5-three-levels-only. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact. | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with detector + repair. | ~700 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure. | ~600 |
| `content/05-examples.xml` | recommended | Worked example. | ~600 |
| `content/06-decision-tree.xml` | essential | Decision branches mapped to rule ids. | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `parse_input` | haiku | Mechanical. |
| `classify_drivers` | sonnet | Subjective tradeoffs. |
| `audit_output` | opus | Cross-cutting subtleties. |
| `emit_spec` | sonnet | Mechanical emission. |

## Templates

| File | Purpose |
|---|---|
| `templates/progressive-disclosure-skills-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/progressive-disclosure-skills-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/progressive-disclosure-skills-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/skill-body.md.j2` | skill body scaffold; loads on trigger match, defers details to references/ |
| `templates/skill-body.md` | skill body scaffold; loads on trigger match, defers details to references/ Generated from `templates/skill-body.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-progressive-disclosure-skills.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
