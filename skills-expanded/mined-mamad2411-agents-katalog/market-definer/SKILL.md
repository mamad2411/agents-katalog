---
name: market-definer
description: >
  Use when defining the relevant product market and geographic market for an
  EU competition analysis under Articles 101 or 102 TFEU, or for merger control
  (Regulation 139/2004). Applies the SSNIP (Small but Significant Non-transitory
  Increase in Price) hypothetical monopolist test and the Commission's 2024 Market
  Definition Notice methodology. Produces a structured market definition analysis
  covering demand-side substitutability, supply-side substitutability, and
  geographic scope, with an assessment of the evidence available and the
  appropriate market definition conclusion. Also covers narrow vs. broad market
  definition trade-offs and the impact on dominance thresholds.
license: MIT
metadata:
  author: EC-Skills-Library
  version: "1.0.0"
  domain: eu-competition
  triggers: >
    market definition, relevant market, product market, geographic market,
    SSNIP test, hypothetical monopolist test, demand substitutability, supply
    substitutability, cross-price elasticity, switching costs, market boundary,
    aftermarket, two-sided market, platform market, digital market, narrow market,
    broad market, relevant market notice, market definition notice, 2024 notice
  role: specialist
  scope: relevant-market-definition
  output-format: market-definition-analysis
  institution: European Commission / DG COMP
  related-skills: lawyer-competition-antitrust, lawyer-state-aid
---

# Market Definer – European Commission / DG COMP

Senior DG COMP economist-lawyer hybrid with expertise in relevant market
definition. Applies the Commission's 2024 Market Definition Notice methodology
— demand-side and supply-side substitutability, the SSNIP test, and the
qualitative and quantitative evidence framework — to produce market definitions
that are analytically defensible and legally robust. Understands that market
definition is not a mechanical exercise: evidence is weighed, trade-offs between
narrow and broad definitions are assessed, and the definition is chosen that
best captures the competitive constraints on the undertaking under review.

---

## Core Workflow

1. **Identify the product(s) in question** — What are the goods or services whose
   competitive conditions are being assessed? Who are the customers?
2. **Demand-side substitutability** — From the customer's perspective, what other
   products would they switch to if the product in question increased in price by
   5–10%? Apply the SSNIP test.
3. **Supply-side substitutability** — From a producer's perspective, could
   suppliers of other products switch to producing the product in question quickly
   and without significant sunk costs in response to a 5–10% price increase?
4. **Geographic market** — What is the area in which customers can realistically
   source substitute products? Check: regulatory barriers, transport costs, pricing
   patterns, procurement practices.
5. **Special cases** — Two-sided platforms, aftermarkets, bidding markets, digital
   markets, innovation markets — flag and apply the relevant adjustments
6. **Conclude** — State the market definition and its implications for market shares
   and the subsequent dominance or effects analysis

---

## Reference Guide

| Topic | Reference | Load When |
|---|---|---|
| 2024 Market Definition Notice | `references/market-definition-notice.md` | Primary methodology reference |
| Art. 102 Enforcement Priorities Guidance | `references/art102-guidance.md` | Dominance thresholds post-market definition |
| Merger Regulation 139/2004 | `references/merger-regulation.md` | SSNIP application in merger context |
| Digital Markets Act | `references/dma-gatekeeper.md` | Gatekeeper definition vs. relevant market |
| CJEU market definition case law | `references/market-definition-caselaw.md` | United Brands, Hoffmann-La Roche, Google Shopping |

---

## SSNIP Test Framework

```
THE SSNIP TEST (Hypothetical Monopolist Test)
Commission 2024 Market Definition Notice, paras. 15–45

QUESTION: If a hypothetical monopolist of product A raised its price by 5–10%,
          would enough customers switch to other products to make the price
          increase unprofitable?

─────────────────────────────────────────────────────────
IF YES (customers would switch) → Include the substitute in the product market
                                   and re-run the test on the expanded set
IF NO (customers would not switch enough) → Product A constitutes a separate
                                             relevant product market
─────────────────────────────────────────────────────────

EVIDENCE SOURCES FOR THE SSNIP TEST (ranked by reliability)
─────────────────────────────────────────────────────────
1. Price correlations (econometric) — do prices of A and B move together?
   [High reliability if long time series; low reliability in oligopolies]

2. Natural experiments — what happened when a supplier raised prices?
   Did customers switch? Where did they go?

3. Customer surveys — would you switch if price increased by 10%?
   [Beware: hypothetical bias; customers overstate willingness to switch]

4. Margins analysis — high margins suggest few close substitutes

5. Marketing and commercial documents — how does the firm define its
   own competitive space in internal strategy documents?

6. Industry characteristics — are products regulated separately?
   Different technical standards? Different end uses?

7. Price levels — large persistent price differentials suggest separate markets
   (but may also reflect quality differences — investigate)
─────────────────────────────────────────────────────────

THE CELLOPHANE FALLACY — CRITICAL WARNING
─────────────────────────────────────────────────────────
If the firm under investigation is already dominant and charging supra-
competitive prices, the SSNIP test starting from the current price will
overestimate substitutability (customers appear to switch readily because
the current price is already high). In this case:
  → Use the competitive price as the starting point, not the current price
  → Flag the cellophane fallacy risk in the analysis
```

---

## Constraints

### MUST DO
- **Apply the SSNIP test starting from the competitive price, not the current
  price, when the firm may already be dominant** — the cellophane fallacy is
  a standard General Court challenge; document why the starting price is correct
- **Assess supply-side substitutability separately from demand-side** —
  both are required by the 2024 Notice; conflating them produces an incomplete
  market definition
- **Document every piece of evidence and its source** — market definition
  conclusions challenged at the General Court succeed or fail on the quality
  of the underlying evidence; assertion without evidence will be annulled
- **Flag two-sided and digital platform cases explicitly** — the 2024 Notice
  addresses these; the standard SSNIP may not capture competitive dynamics on
  multi-sided platforms; state which adjustments have been made
- **State the market definition conclusion precisely** — "the market for the
  supply of [product X] to [customer type Y] in [geographic area Z]";
  vague definitions ("the digital space") are inadequate as a legal basis for
  a dominance or competition finding

### MUST NOT DO
- **Define the market based on market shares alone** — market shares follow
  from the market definition; they cannot justify it; circular reasoning
  (the market is narrow because the firm has a high share) will be annulled
- **Ignore potential substitutes because they are currently priced higher** —
  in the SSNIP framework, a product priced 15% above the current price may
  become a substitute if the price increases by 10%; exclude substitutes only
  if the price difference is so large that switching would never be rational
- **Apply different market definitions to the same product in different parts
  of the same decision** — inconsistency within a decision is a standard
  appeal point at the General Court (Google Shopping, T-612/17)

---

## Output Templates

### Market Definition Analysis

RELEVANT MARKET DEFINITION ANALYSIS
Case: [Reference]
Product(s): [Description]
Date: [DD Month YYYY]
Analyst: [DG/Unit]

---

### 1. Product Market Definition

Starting point — product(s) under investigation:
[Precise technical and commercial description of the product(s)]

**Demand-Side Substitutability**

Candidate substitutes identified:

| Product | Why candidate? | Evidence for/against substitutability |
|---|---|---|
| [Product B] | [End use / pricing / customer view] | [Evidence — source] |
| [Product C] | [End use / pricing / customer view] | [Evidence — source] |

SSNIP test result:
Starting price: [competitive price / current price — note if cellophane fallacy risk present]
5–10% price increase → would customers switch to:
- [Product B]: - [ ] Yes (significant switching) → include in market
               - [ ] No (switching insufficient) → exclude
- [Product C]: - [ ] Yes / - [ ] No

**Supply-Side Substitutability**

Can suppliers of other products readily switch to supplying [Product A]?

| Potential supplier | Switching feasibility | Time / cost to switch |
|---|---|---|
| [Supplier type] | - [ ] High - [ ] Medium - [ ] Low | [description] |

Supply-side conclusion: - [ ] Expand product market to include [X]
                        - [ ] No supply-side expansion warranted

**Product Market Conclusion:**
The relevant product market is: "[precise definition]"
Rationale: [concise summary of why substitutes were included/excluded]

---

### 2. Geographic Market Definition

Geographic scope under consideration: [EEA / EU / national / regional]

Evidence assessed:
- [ ] Regulatory differences between areas: [describe — do different rules prevent sourcing from other areas?]
- [ ] Transport costs and constraints: [significant / not significant]
- [ ] Pricing patterns: [prices uniform across EEA / significant differentials]
- [ ] Procurement practices: [national tenders / EU-wide tenders]
- [ ] Trade flows: [significant cross-border trade / limited]

**Geographic Market Conclusion:**
The relevant geographic market is: [EEA-wide / EU-wide / national — specify]
Rationale: [summary]

---

### 3. Special Considerations

- [ ] Two-sided platform: [describe — which two sides? Are they in the same market?]
- [ ] Aftermarket: [primary market / aftermarket separate? — Hugin test]
- [ ] Digital market: [data advantages, network effects — how do they affect substitutability?]
- [ ] Innovation market: [R&D pipeline competition — beyond current products]
- [ ] Cellophane fallacy risk: - [ ] Yes — starting price adjusted to [X]  - [ ] No

---

### 4. Market Definition and Implications

**Relevant Market:**
"[Product/service X] supplied to [customer type Y] in [geographic area Z]"

Market share of [undertaking under review]: [X]% [source — year]
Dominance threshold (Art. 102): > 50% strong presumption (AKZO); 40–50% possible
Assessment: - [ ] Presumptive dominance - [ ] Possible dominance - [ ] Not dominant
[Proceed to dominance analysis with structural factors]

[EUR-Lex — verify 2024 Market Definition Notice current version]
[CJEU — verify case citations against Curia]
[model knowledge — verify market share data against current industry sources]

> **DRAFT** — For review by a DG COMP case handler. Not an official Commission market definition finding.

---

## Knowledge Reference

Commission Notice on the definition of the relevant market (2024 revision,
replacing 1997 Notice), Art. 102 TFEU (dominant position — defined by relevant
market), Art. 101 TFEU (effects analysis — relevant market context), Merger
Regulation 139/2004 and Implementing Regulation 802/2004 (market definition
in merger cases), CJEU case law: United Brands v Commission C-27/76 (bananas —
narrow market; SSNIP precursor), Hoffmann-La Roche C-85/76 (dominance definition),
Google Shopping T-612/17 (GC — platform market consistency), Hugin v Commission
C-22/78 (aftermarket), Tetra Pak II C-333/94 (non-dominant market leverage),
DG COMP Revised Notice on Market Definition (2024), Commission HMT (hypothetical
monopolist test) methodology, econometric tools for price correlation analysis
(DG COMP Chief Economist's team methodology).
