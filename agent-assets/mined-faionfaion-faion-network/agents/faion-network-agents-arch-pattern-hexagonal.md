# Hexagonal Architecture (Ports and Adapters)

## Summary

**One-sentence:** Application core is isolated from the outside world through ports (interfaces) and adapters (implementations); both inbound and outbound concerns are pluggable.

**One-paragraph:** Hexagonal Architecture (Cockburn, 2005) lets the application be driven by users, programs, automated tests, or batch scripts equally, and lets it work in isolation from runtime devices and databases. The application defines ports (inbound and outbound interfaces); adapters implement them. Output is a layout spec with explicit ports + adapters and a CI lint blocking direct cross-imports.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Application has at least one inbound driver (HTTP, CLI, queue) and at least one outbound dependency (DB, external API).
- You want to drive the application from tests without spinning up the whole stack.
- You expect to swap one adapter (e.g., DB or messaging) within the next 24 months.

## Skip If (ANY kills it)

- Prototype or single-test-only code path.
- Pure library with no inbound drivers.
- Team unfamiliar with DI; cost of ports exceeds benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Driver inventory (HTTP, CLI, queue) | list | tech lead |
| Driven inventory (DB, external API, file system) | list | tech lead |
| Import-direction lint tool | config | tooling team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/arch-pattern-clean` | Clean rings map directly onto hexagonal layers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layout spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: drivers → driven → ports → adapters → lint | ~700 |
| `content/05-examples.xml` | medium | Worked example: HTTP+CLI inbound, Postgres+Stripe outbound | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-ports` | sonnet | Per-port interface synthesis. |
| `draft-adapters` | sonnet | Per-port adapter scaffolding. |
| `audit-imports` | opus | Cross-module import graph audit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/hex-layout.md.j2` | Hexagonal layout spec with driving + driven ports and adapters. |
| `templates/hex-layout.md` | Hexagonal layout spec with driving + driven ports and adapters. Generated from `templates/hex-layout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-arch-pattern-hexagonal.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[arch-pattern-clean]]
- [[arch-pattern-onion]]
- [[arch-pattern-ddd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
