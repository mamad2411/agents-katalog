---
name: seeri
description: Verifiable deep-research skill for any onchain or market question. Decomposes a messy question into sub-claims, maps sources by category, triangulates the highest-stakes claims, builds an evidence grid with confidence ratings, and synthesizes a defensible thesis. Uses SERV Reasoning for the reasoning steps when SERV_API_KEY is available. Use when researching a token, protocol, chain, RWA vault, tokenized asset, market move, or any claim that needs sourcing before someone acts on it.
---

# Seeri

Seeri turns an ambiguous question into research someone can defend: every claim is tied to a source category, every conclusion carries a confidence level, and every thesis states what would change it.

It is chain-agnostic and asset-agnostic. Research a Stock Token on Robinhood Chain, a lending protocol on Base, an RWA yield vault, a memecoin launch, or a regulatory headline with the same process. Domain packs add the specific data sources and failure modes for each area.

## Intake

Capture these before research:

- Original question, exactly as received
- Decision this informs
- Deadline
- Cost of being wrong
- Expected output (memo, article, thread, grid only, go/no-go)

If any field is blank and the answer cannot be safely inferred, ask for it or state the assumption.

## Route By Task

- Full research run: read [research-workflow.md](research-workflow.md)
- Source planning or claim checking: read [source-map.md](source-map.md)
- Findings grid, confidence, or contradictions: read [evidence-grid.md](evidence-grid.md)
- Article, thread, or memo: read [article-synthesis.md](article-synthesis.md)
- Using SERV Reasoning for decomposition, grading, and synthesis: read [reasoning-serv.md](reasoning-serv.md)
- Hackathon packaging: read [hackathon-submission.md](hackathon-submission.md)
- Mantle example and source links: read [resources.md](resources.md)

## Domain Packs

Load the pack that matches the subject. Each pack lists primary data sources, what to verify first, and the traps specific to that domain.

- Robinhood Chain, Stock Tokens, chain-native launches: read [domains/robinhood-chain.md](domains/robinhood-chain.md)
- Coinbase AgentKit, Base, agent wallets: read [domains/agentkit-base.md](domains/agentkit-base.md)
- IXS and licensed RWA yield vaults: read [domains/ixs-rwa-vaults.md](domains/ixs-rwa-vaults.md)
- Memecoins, attention markets, launch safety: read [domains/memecoin-markets/SKILL.md](domains/memecoin-markets/SKILL.md)

## Core Workflow

1. Preserve the messy question.
2. Decompose into 5-8 answerable sub-questions.
3. Assign at least three source categories.
4. Triangulate the highest-stakes claim through two source categories.
5. Build a findings grid with confidence and gaps.
6. Synthesize a thesis, caveats, and "what would change my mind."
7. Package the output for the requested format.

## Confidence Rules

- High: recent primary source plus independent corroboration, no unresolved contradiction.
- Medium: one strong source or multiple interested sources.
- Low: stale, indirect, contradicted, or incentive-heavy evidence.

## Boundaries

- Do not provide legal, tax, compliance, investment, or trading advice.
- Do not imply tokenized equities are direct ownership unless the source proves it.
- Do not invent traction, volume, holders, revenue, integrations, allocations, or regulatory approval.
- Label project-reported claims and interested-party claims clearly.
- Never present a model's reasoning output as a source. Reasoning organizes evidence; it does not create it.
