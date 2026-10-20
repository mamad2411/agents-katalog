# Verb-Object Tool Naming with Namespace Prefix

## Summary

**One-sentence:** Force every tool to lowercase snake_case verb_object form, namespace-prefixed when catalog spans multiple servers; validates by a name-audit rubric.

**One-paragraph:** Tool names matter more than descriptions for selection accuracy — the model parses the name first and uses the description only to disambiguate close matches. Single-token opaque names (`search`, `manage`, `do_thing`) are the most common reason an agent picks the wrong tool. Anthropic's tool-writing guidance reports prefix and naming schemes meaningfully change selection accuracy on internal evals; small renames produce outsized swings. This methodology enforces `verb_object` (snake_case) plus a service namespace (`github_create_issue`) when the catalog spans multiple MCP servers, validates the catalog against a name-audit rubric, and tracks tool-selection error rate as the primary regression signal.

**Ефективно для:**

- MCP-агрегатори, де 10+ серверів зливаються в один каталог: namespace prefix усуває collisions.
- Каталоги з `search` / `query` / `find` дублетами: rename + namespacing підвищує selection accuracy.
- Wrappers навколо third-party SDKs (GitHub/Stripe/Asana): зберігаємо verb, додаємо namespace.
- Tool-eval ітерації: rename → rerun eval → keep better name (data-driven naming).

## Applies If (ALL must hold)

- Tool catalog has ≥5 tools.
- Tools come from multiple sources / MCP servers / gateways.
- Eval set or trace store exists to measure tool-selection error rate pre/post rename.

## Skip If (ANY kills it)

- Single-tool hobby scripts where naming is not the bottleneck.
- Host SDK enforces non-snake_case convention (GraphQL camelCase, Go-style ExportedName) — match host.
- Auto-generated tool catalogs from OpenAPI where names are owned by the upstream spec.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool catalog | JSON / Python dict / MCP server list | repo or MCP gateway |
| Naming convention doc | Markdown | team conventions |
| Selection-error baseline | JSON | first eval run committed to repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Background (names are prompt; one-line form of the naming rule) + 6 testable rules: verb-object-snake-case, namespace-on-multi-server, forbid-padding, rename-after-eval, name-schema-alignment, atomic-verb-per-tool; source links | 1250 |
| `content/02-output-contract.xml` | essential | JSON Schema for rubric + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix (incl. polymorphic-action-enum) | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | recommended | Namespaced verb_object catalog vs opaque single-token catalog (json) | 400 |
| `content/06-decision-tree.xml` | essential | Routing tree on tool count → multi-server → action enum → padding → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest_catalog` | haiku | File parsing + tokenization. |
| `score_each_name` | haiku | Deterministic 0/1 checks. |
| `propose_renames` | sonnet | Light judgment to pick the right verb/object. |
| `run_ab_rename` | haiku | Mechanical eval execution. |

## Templates

| File | Purpose |
|------|---------|
| `templates/name-rewrite-prompt.md.j2` | Prompt template for the naming-rewrite subagent |
| `templates/name-rewrite-prompt.md` | Prompt template for the naming-rewrite subagent Generated from `templates/name-rewrite-prompt.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-verb-object-tool-naming.py` | Validate the rubric artefact against the schema | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-description-as-prompt]]
- [[terse-default-tool-output]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
