---
name: card-shared
description: Shared research policy and output contracts for the card command suite (card-full, card-transfer, card-rate, card-news, card-credits, card-compare, card-value, card-wallet). Use as background reference, not as a user-facing command.
user-invocable: false
allowed-tools: Read, Bash(curl -sS *)
---

# Card Shared

## Purpose

This hidden skill holds the shared rules for the card command suite. User-facing commands should reuse these files instead of redefining sourcing, confidence, or output contracts independently.

## Shared References

- [source-policy.yaml](source-policy.yaml) for issuer-first research, approved secondary sources, issuer blog/newsroom policy, and the fast-search policy
- [command-contracts.yaml](command-contracts.yaml) for required sections and YAML keys
- [section-definitions.md](section-definitions.md) for `/card-full` composition rules
- [../card-identity/SKILL.md](../card-identity/SKILL.md) for centralized card-name resolution, abbreviation handling, and disambiguation
- [card-identity-rules.md](card-identity-rules.md) for card matching and ambiguity handling rules
- [confidence-rules.md](confidence-rules.md) for `confirmed`, `unconfirmed`, and `conflicting`
- [recency-rules.md](recency-rules.md) for freshness expectations, especially `/card-news`
- [normalization-rules.md](normalization-rules.md) for shared formatting and field conventions

## Shared Behavior

1. Identify the exact card variant first. If ambiguous, return a numbered choice list and stop.
2. Follow the fast-search policy: issuer pages first, stop early when the contract is satisfied, consult only 2-4 secondary sources when needed.
3. Mark uncertain or conflicting claims explicitly in `confidence_notes`.
4. Return compact markdown with emoji section headings and numbered lists.
5. YAML is internal only — never include it in user-facing output.
6. End every report with a `## 🔗 Sources` section listing each URL fetched during research as a markdown hyperlink with a short "Site - Topic" label, e.g. `[Chase - Sapphire Preferred](https://...)`.
7. Omit the Card Identity section when the match is confident.

## Composition Note

`/card-full` composes from `/card-rate`, `/card-transfer`, and `/card-credits`. `/card-news` is intentionally independent — news is time-windowed and conceptually separate from the static card framework. `/card-compare`, `/card-value`, and `/card-wallet` are multi-card or analytical commands that reuse the same shared rules but have their own contracts.
