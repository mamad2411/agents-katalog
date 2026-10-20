# Discriminated-Union Structured Output

## Summary

**One-sentence:** Models polymorphic structured output as a tagged union where a literal discriminator field declared first locks the JSON Schema branch, eliminating cross-branch field bleed and turning shape selection into a single constrained-decoding choice.

**One-paragraph:** When a structured-output schema must choose between two or more distinct shapes (different agent actions, different entity types, different intents, different events), model the output as a discriminated union — a tagged union where one literal field (kind, type, action) is generated FIRST and selects which branch the rest of the object must follow. The discriminator locks the JSON Schema / grammar branch and turns shape selection into a single constrained-decoding choice instead of a probabilistic mess of optional fields.

**Ефективно для:** агентських дій з різними аргументами, мульти-сутнісного екстракту, маршрутизаторів та подієвих шин — будь-де, де модель мусить обрати одну з N різних форм виводу.

## Applies If (ALL must hold)

- Agent action selection where each action has different required arguments (search vs fetch vs finish vs ask-user).
- Polymorphic entity extraction (Person vs Company vs Product vs Address) from one document.
- Router outputs that must dispatch to one of N downstream handlers.
- Event logs / message buses where each event type has its own payload schema.
- Decoder backend honours JSON Schema 2020-12 `discriminator` (OpenAI strict, Pydantic v2, Outlines, XGrammar).

## Skip If (ANY kills it)

- All branches share more than ~90% of their fields — flatten with optional fields and a single kind literal instead.
- The set of branches is open (user-defined entity types, plug-in actions) — use a registry pattern with free-string kind plus a separate validation pass.
- Targets that do not honour the discriminator keyword (older Outlines/XGrammar, custom GBNF grammars without union support) — fall back to two sequential calls (classify, then extract).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Set of N shape variants | Pydantic BaseModel classes | Application code |
| Discriminator field name | `kind` / `type` / `action` (project convention) | Style guide |
| Decoder mode | strict / grammar-backed | Provider config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `enum-constraints-closed-vocabularies` | The discriminator literal is itself an enum value; same masking principle. |
| `inverted-header-content-first` | Discriminator-first is the most important application of field-order discipline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Four testable rules: discriminator first, Literal type, Annotated[...] usage, collapse-if-overlap | ~900 |
| `content/02-output-contract.xml` | essential | Pydantic and JSON Schema 2020-12 forms of the agent-action union | ~900 |
| `content/03-failure-modes.xml` | essential | Discriminator last, optional-field bleed, branch overlap | ~700 |
| `content/06-decision-tree.xml` | essential | Pick union vs flatten vs registry | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Author the union for a new agent | sonnet | Schema design with clear constraints |
| Audit existing schema for missing discriminator | haiku | Pattern detection across files |
| Decide union vs flatten on near-overlapping shapes | opus | Tradeoff analysis needs deeper reasoning |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent_action_union.py` | Pydantic discriminated union for an agent-action selector (search / fetch / finish) |
| `templates/agent_action.schema.json` | Equivalent JSON Schema 2020-12 with `oneOf` + discriminator for non-Python providers |
| `templates/_smoke-test.json` | Minimum valid SearchAction payload for self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-discriminated-union-output.py` | Validates a sample action JSON against the discriminator + branch fields | Pre-commit on schema changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[enum-constraints-closed-vocabularies]]
- [[inverted-header-content-first]]
- [[field-descriptions-as-prompts]]

## Decision tree

See `content/06-decision-tree.xml`. The root question is whether the output space has 2+ genuinely distinct shapes. The tree then checks field overlap (>90% means flatten), branch openness (open means registry), and decoder support (no discriminator support means two-call fallback). Each leaf points at a rule in `01-core-rules.xml`.
