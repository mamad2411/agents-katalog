---
name: funding-rounds-analysis
version: "1.0"
description: Guides Slice MCP analysis of funding rounds, share classes, price per share, primary issuances, secondary transactions, convertibles, SAFEs, option-pool top-ups, total raised, and dilution. Use when answering questions about rounds, Series A/B/C, seed rounds, bridge rounds, investor positions, round history, valuation, PPS, or post-money ownership.
---

# Funding Rounds Analysis

## Scope

Use for round mechanics, proceeds, and dilution. For company-wide cap-table structure without round focus, use cap-table-analysis. For exit proceeds allocation, use waterfall-analysis.

## Tool Workflow

1. Use `rounds_list` to discover rounds and the share classes associated with each round.
2. Use `rounds_get_display_data` only when names/IDs are enough.
3. Use `rounds_get_total_raised` after collecting the target round's share class IDs from `rounds_list`.
4. Use `share_classes_list` and `share_classes_get_one` for share-class terms and names.
5. Use `cap_table_get_summary`, `cap_table_search_entries`, `securities_find`, and `securities_search` to inspect investors, issued shares, convertibles, warrants, and stakeholder positions around the round.
6. Use `valuations_list` when valuation/FMV context is relevant.

Keep the same as-of date across tools when comparing pre/post or current round effects.

## Round Mechanics

A priced round usually has: pre-money valuation, pre-money fully diluted share count, optional pool top-up, price per share, new primary shares issued, post-money valuation, and post-money fully diluted ownership.

Do not conflate primary and secondary transactions. Primary issuances create new shares and cash goes to the company. Secondary transfers move existing shares between stakeholders and cash goes to the seller, so they do not increase company proceeds or outstanding shares.

Founder shares issued at nil or nominal consideration are normal formation shares. SAFE and convertible instruments may affect fully diluted calculations before they convert and become shares at a priced round.

## Option Pool Top-Ups

Investors often require the unissued option pool to be refreshed before closing. That top-up is typically pre-money, diluting existing holders before the new investment price is set. Use equity pool and cap-table tools to understand pool size and availability; do not infer a top-up unless round, pool, or share-class data supports it.

## Convertibles And SAFEs

For SAFE or convertible-note questions, identify the instrument, principal, valuation cap, discount, interest, maturity, and conversion round if available. The favorable conversion price is usually the lower of cap-implied price and discount-implied price, but exact terms govern. Use securities tools for convertible records and avoid inventing missing deal terms.

## Response Style

Report round name, closing/effective date, share classes, total raised, price per share if available, primary investors, new shares issued, option pool changes, convertibles converted, and dilution. State when the available MCP data supports only a current snapshot rather than a full pre/post round reconstruction.
