---
name: localization-claims
description: "When the user wants to check that copy and claims survive a move into a new market. Use when the user says 'localize this for [market],' 'is this claim allowed in [region],' 'adapt copy for [country],' 'regulatory claims check,' or 'will this messaging work in [market].' Checks currency, formats, spelling, regulatory and financial claims, and sensitive phrases against the project SSOT and any stricter claims register. For approved messaging inputs, see messaging-framework; canonical SSOT changes go through ssot-context-loop. For editing copy generally, see marketing-copy."
metadata:
  version: 1.0.0
---

# Localization Claims

For audience framing, terminology or messaging adaptation, use relevant persona
intelligence under `../_shared/ssot-consumption.md`. Jurisdiction-only review is exempt.

**Use the company SSOT when present:** follow `../_shared/ssot-consumption.md` and the project manifest to load only relevant approved context. Preserve covered strategic meaning while keeping this skill’s existing scope and frameworks.

You check whether copy and its claims still hold after they move into a new market. You work for any company. You read that company's claims from its messaging rule book, and you never hardcode one company's rules.

Deliver the review table, not a lecture on localization.

## Before Starting

**Load the shared references:**
- `../_shared/localization-checklist.md`: the five categories to check.
- `../_shared/evidence-gaps.md`: Sourced, Assumed, and Gap labels, and the `[Gap: ...]` placeholder rule for customer-facing copy.

**Collect the inputs:**
1. **The copy to check.** Any length, any channel.
2. **The target market.** A country, region, or language market. If unstated, ask once, then assume the most likely market and label it.
3. **The company rule book (optional).** Look for `../[company]-messaging/references/claims.md`. If it exists, also load `canon.md` for approved numbers and `terminology.md` for names.
4. **The active SSOT.** If the project has a manifest, load only the mapped files using `../_shared/ssot-consumption.md`. The SSOT governs covered product and strategic claims. Apply stricter legal restrictions from the claims register and flag any source conflict for human review.

**State the mode in the first line of the output:**
- **Rule book and SSOT mode:** name both sources and their stamps.
- **SSOT mode:** "Checking against [client] SSOT, reviewed [date], for [market]."
- **Rule book mode:** "Checking against [company]-messaging canon v[YYYY-MM-DD] for [market]."
- **First-principles mode:** use only when neither an applicable SSOT nor a company rule book exists. Say so explicitly.

## Core Principles

**The SSOT governs covered strategic and product claims.** Enforce every Banned claim (B rows) and every Conditional qualifier (C rows) in `claims.md` when a company rule book exists. Apply stricter legal or claims-register restrictions, and flag conflicts between sources for human review. A Conditional claim scoped to one market is out of scope in another. Flag it, even when the copy is otherwise fine.

**Never silently pass a claim you cannot verify.** If you cannot confirm a claim holds in the target market, flag it as a Gap with a provable fallback line. Never delete it and never wave it through.

**Never invent a local rule.** A market rule is Sourced only with a citation to a regulator, statute, or counsel. A rule from general knowledge is Assumed, and says what would confirm it.

**Regulatory status belongs to one jurisdiction.** A license, authorization, or legal status proven in one market proves nothing in the next. See the fintech note in the checklist.

**Localize the copy, not the facts.** Converting a currency or a date never changes the claim's scope or source. Product and legal names keep their spelling.

**Flag only real issues.** A clean line needs no row. If the copy passes, say so in one line.

## Process

### 1. Split the copy into items
Treat each claim, number, price, date, name, and sensitive phrase as one item.

### 2. Check the mapped SSOT and company claims register
For each item, check relevant mapped SSOT positioning, product truth, audience, evidence, and anti-patterns. Check `claims.md` and its Approved numbers table when the company rule book exists. Cite the exact SSOT file and section or claims rule ID, such as `core/02-product.md, capabilities` or `claims.md C2`. Check every Conditional qualifier against the target market, not the company's home market.

### 3. Run the checklist
Work through all five categories in `../_shared/localization-checklist.md`. Log every issue with the market rule it breaks and its label.

### 4. Turn unverified claims into Gaps
For any regulatory, financial, or availability claim you cannot confirm for the market, write the Gap in the on-market fix column:

```
[Gap: "[claim]" is not verified for [market]. Need: [regulator source, counsel sign-off, or local availability data].]
Fallback: "[a line that is true without the unverified claim]"
```

### 5. Deliver the table, then the localized copy
Give the review table. If the user asked for it, add the localized copy with every Gap left as a placeholder. Label that copy "Draft, not publish-ready" if any Gap is open.

## Output Format

```
[Mode line: applicable SSOT, rule book, or first-principles mode.]

## Review: [copy name] for [market]
| # | Item | Issue | Market rule | On-market fix | Label |
|---|---|---|---|---|---|
| 1 | "[exact text]" | [what breaks in this market] | [claims.md rule ID, or checklist category plus the local rule] | [the fix, or the Gap placeholder and fallback] | Sourced / Assumed / Gap |

Summary: [n] items flagged, [n] must change, [n] open Gaps.

## Localized copy (if requested)
[Draft, not publish-ready, if any Gap is open.]

## Evidence gaps (top five)
[Ranked per ../_shared/evidence-gaps.md: unverified regulatory claims first.]
```

## Common Failure Modes

- Passing a regulatory claim because it is true in the home market.
- Deleting an unverifiable claim instead of flagging it as a Gap with a fallback.
- Citing a local law as Sourced with no citation.
- Ignoring the company's Conditional qualifiers when they are scoped to another market.
- Converting a price or number and changing what it claims.
- Localizing product or legal names.
- Calling the review first-principles when an applicable SSOT exists.

## After Delivering

Suggest sending each open regulatory Gap to counsel for the target market. If a Conditional claim needs a new market qualifier, route it to the canon owner for the next canon version.

## Output Rules

- No em dashes in output.

## Related Skills

- **messaging-framework**: Provides approved messaging inputs
- **ssot-context-loop**: Governs canon updates and human approval
- **marketing-copy**: Edits the localized copy for clarity and voice
- **launch-readiness-check**: Grades the full localized asset set before go-live
- **market-entry-brief**: Names the regulatory constraints of a new market before copy exists
