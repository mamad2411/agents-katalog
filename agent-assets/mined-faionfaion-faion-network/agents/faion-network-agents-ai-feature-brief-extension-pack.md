# AI Feature Brief Extension Pack

## Summary

**One-sentence:** Adds the four AI-specific sections that classic PRDs miss — model choice, eval set, hallucination policy, cost guardrails — to a regular feature brief, producing an extended brief PMs and engineers can ship against.

**One-paragraph:** Classic PRDs assume deterministic software: features either work or don't. AI features add four axes a PRD must commit to before engineering starts — which model (and what happens when the provider deprecates it), which eval set gates promotion, what the hallucination policy is when the model is wrong (refuse / caveat / fall through to human), and what the cost guardrails are per request / per day / per outlier. This pack is a stack of four named sections that bolt onto any PRD template; output is one extended brief reviewed by product + engineering + finance.

**Ефективно для:** Команд, де PRD виглядає як для звичайної фічі, потім інженери два тижні шукають, що робити коли LLM «бреше»; pack дає чотири розділи, на які PM відповідає до старту — і інженери знають exact contract з першого дня.

## Applies If (ALL must hold)

- A classic PRD or feature brief already exists or is being drafted.
- The feature involves at least one LLM call user-facing.
- Product, engineering, and finance can review jointly within one sprint.
- The team agrees that AI features get scoped differently from deterministic features.
- A versioned PRD store (Notion, Confluence, repo) holds the artefact.

## Skip If (ANY kills it)

- Feature uses no LLM (pure heuristics, classifier with known accuracy, deterministic logic).
- One-off experiment with no production exposure.
- Team has no governance burden (research lab, no users).
- PRD process is itself in flux — stabilise the base PRD format first.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Base PRD | Markdown | PM |
| Model catalogue | YAML / spreadsheet of available models | Tech lead |
| Eval set list | jsonl + golden answers | QA |
| Cost dashboard | URL / API | Finance / ops |
| Hallucination policy template | Markdown | Compliance / legal |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-shape-decision-frame/AGENTS.md` | Shape decision feeds into model choice. |
| `geek/ai/ai-agents/ai-governance-compliance/AGENTS.md` | Compliance constraints anchor the hallucination policy section. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: model-pinned, eval-named, policy-explicit, cost-capped, r1 (base PRD first, joint sign-off to publish), r2 (unfilled section blocks review) | ~750 |
| `content/02-output-contract.xml` | essential | JSON Schema for the extended brief | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: collect base → fill 4 sections → review → validate → publish | ~900 |
| `content/05-examples.xml` | medium | Worked example: extended brief for a doc-summarisation feature | ~900 |
| `content/06-decision-tree.xml` | essential | Tree: PRD exists? → 4 sections answerable? → publish/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_base_prd` | haiku | Structured extraction. |
| `draft_4_sections` | sonnet | Domain judgment on model/eval/policy/cost. |
| `cross_review` | opus | Product + finance + compliance synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the extended brief. |
| `templates/output.example.json` | Filled minimal valid example. |
| `templates/brief-extension.md.j2` | Markdown skeleton with the four sections. |
| `templates/brief-extension.md` | Markdown skeleton with the four sections. Generated from `templates/brief-extension.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the extended brief. | After draft, before sign-off. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[ai-governance-compliance]] — informs the hallucination-policy section.
- peer: [[ai-feature-ux-pattern-library]] — UX patterns referenced in the brief.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) does a base PRD exist? (2) can all four sections (model / eval / policy / cost) be answered now? Leaves point to "publish", "collect missing inputs", or "escalate".
