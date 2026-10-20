# Prompt Cache Prefix Order

## Summary

**One-sentence:** Produces a prompt-order spec placing STABLE parts first, VOLATILE last, with cache_control breakpoint after the longest stable prefix — Anthropic caching charges 10% for the cached prefix.

**One-paragraph:** Anthropic prompt caching charges 10% (or less) for cached prefix tokens but only for content BEFORE the cache_control breakpoint that matches an earlier call. Mixing volatile content (user input, timestamps) before stable content (system prompt, tool definitions) destroys cache hits. This methodology emits a spec ordering prompt sections by volatility and placing the breakpoint correctly.

**Ефективно для:** team paying full price on every API call because system prompt + tools live AFTER user input or RAG chunks.

## Applies If (ALL must hold)

- Using Anthropic API with prompt caching enabled.
- >1k API calls per day where caching could amortise.
- System prompt + tools > 1024 tokens (cache minimum).

## Skip If (ANY kills it)

- OpenAI / other providers (different caching semantics).
- Very small prompts (<1024 tokens).
- Every call has unique system prompt.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `prompt-sections.yaml` | list of {section_name, content, volatility} | operator |
| `min_cache_tokens` | integer (1024 default) | anthropic policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| none | Self-contained. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-stable-first; r2-breakpoint-after-stable; r3-min-1024-tokens; r4-max-4-breakpoints; r5-monitor-hit-rate. | ~900 |
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
| `templates/prompt-cache-prefix-order-spec.md.j2` | Markdown wrapper for the JSON spec. |
| `templates/prompt-cache-prefix-order-spec.md` | Markdown wrapper for the JSON spec. Generated from `templates/prompt-cache-prefix-order-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-prompt-cache-prefix-order.py` | Validates spec against the schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Sibling methodologies in `geek/ai/ai-agents/`.

## Decision tree

Lives at `content/06-decision-tree.xml`. Walks the drivers and picks a rule id per leaf. Each conclusion cites a rule in 01-core-rules.xml so the spec records the audit chain.
