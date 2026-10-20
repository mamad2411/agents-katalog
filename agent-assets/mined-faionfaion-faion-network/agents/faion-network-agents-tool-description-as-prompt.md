# Tool Description as Prompt

## Summary

**One-sentence:** Treat each tool description as a zero-shot teaching prompt with five named parts under 200 tokens, validated against a catalog-audit rubric.

**One-paragraph:** A tool definition becomes part of the system context every time the model decides whether to call a tool. Anthropic's engineering team reported state-of-the-art on SWE-bench achieved by rewriting descriptions, not changing the model. This methodology enforces a five-part structure (use-when, do-NOT-use-when, input contract, output contract, side effects), caps each description at 200 tokens, requires mutual anti-triggers between overlap pairs, mandates `MUTATING:` markers on destructive tools, and verifies the result with an audit-rubric schema that scores each tool 0-5 across the axes. Catalogs are re-evaluated quarterly; both tool-selection and argument-fill error rates are tracked as primary regression signals.

**Ефективно для:**

- MCP-агрегатори і tool-каталоги &gt; 10 інструментів — структуроване опис різко знижує mis-selection.
- Команди, в яких опис інструмента =  marketing-blurb або docstring — швидке покращення SWE-bench-style accuracy.
- Side-effect інструменти (DELETE, DROP, ROLLOUT) — MUTATING-prefix зупиняє accidental calls.
- Description-schema drift аудити — лінт-rule cross-check блокує phantom-arguments ще до production.

## Applies If (ALL must hold)

- Catalog has ≥3 tools whose names share a verb-class (search/get/list etc.) or use cases overlap.
- The catalog is reachable by an agent loop (Claude, GPT, Llama agents — anything that picks tools by description).
- A 50-task eval set or trace store exists to measure pre/post selection-error rate.

## Skip If (ANY kills it)

- Single-tool catalogs where there is no selection problem to begin with.
- One-off scripts where the agent calls a fixed sequence and tool-pick is hard-coded.
- Catalogs whose tools are auto-generated from OpenAPI specs and overwritten on every regen (apply at the spec layer instead).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tool catalog | JSON / Python dict / MCP server list | repo / MCP gateway |
| Eval set | 50 representative task prompts | recorded user requests or synthetic set |
| Trace store | per-call (tool_name, args, outcome) | LangSmith / Phoenix / internal logs |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[verb-object-tool-naming]] | Naming has to be sound before descriptions are tuned. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: structured-description-required, under-200-tokens, anti-trigger-on-overlap, mutating-marker, latency/pagination caps, schema-match | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema for catalog-audit rubric + examples | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: marketing-prose, overlap-without-anti-trigger, silent-mutation, schema-description-drift, unbounded-pagination | 800 |
| `content/04-procedure.xml` | essential | 5-step audit → score → detect-overlap → rewrite → measure procedure | 800 |
| `content/06-decision-tree.xml` | essential | Branches on audit-score + mutating + overlap | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score_catalog` | haiku | Five 0/1 checks against templates; deterministic. |
| `detect_overlap` | haiku | Lexical similarity + verb-class clustering. |
| `rewrite_description` | sonnet | Needs balance of brevity + completeness; light judgment. |
| `measure_eval_delta` | haiku | Counting tool-selection errors over fixed eval set. |

## Templates

| File | Purpose |
|------|---------|
| `templates/anthropic-tool-definition.py` | Anthropic SDK tool definition using the 5-part structure |
| `templates/openai-tool-definition.py` | OpenAI SDK function definition using the 5-part structure |
| `templates/mcp-tool-description.py` | MCP `@mcp.tool()` decorator with structured docstring |
| `templates/tool-family-with-anti-triggers.py` | Pattern: read_file + grep_repo with mutual anti-triggers |
| `templates/side-effect-tools.py` | Pattern: apply_patch + dry_run_patch with `MUTATING:` marker |
| `templates/pagination-pattern.py` | Pattern: list_issues with explicit per-page + max-page cap |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-description-as-prompt.py` | Validate the audit JSON against the rubric schema | After each catalog audit; pre-commit on the audit artefact |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[verb-object-tool-naming]] — naming sets the lexical anchor; description fills the gap.
- [[terse-default-tool-output]] — description must declare summary/full mode and token bands.

## Decision tree

See `content/06-decision-tree.xml`. The tree first asks for the tool's 5-axis audit score (5/5 = keep), then asks whether the tool mutates state (yes → `MUTATING:` rewrite), then whether any peer description has cosine &gt; 0.8 (yes → mutual-anti-trigger rewrite). Each leaf references a rule from `01-core-rules.xml`.
