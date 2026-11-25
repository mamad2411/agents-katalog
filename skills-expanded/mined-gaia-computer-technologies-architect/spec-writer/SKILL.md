---
name: spec-writer
description: Draft outline specification clauses in the practice's own system (NBS / Uniclass in the UK, MasterFormat / SectionFormat in North America, NATSPEC, STABU, CCTP, StLB and others) and build product comparison tables with manufacturer source links. Separates design intent from product choice, writes performance-based or proprietary clauses as asked, and marks every performance value, standard number, and product claim "to confirm against datasheet" unless a source is supplied. Use when the architect wants to "write a spec", "outline specification", "spec clause for", "compare products", "find three alternatives to", "performance spec", or "NBS clause". Hands to material-palette for design-intent material choices, carbon-estimate for embodied carbon of options, and cost-check for cost comparison.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Spec writer

A specification is a contract document. Write clauses that say exactly what is required, in the structure the practice already uses, and never let a plausible-sounding product name or test standard slip in unsourced.

## When to use

- Outline or full specification at technical design stage.
- Turning a material palette or design intent into specifiable requirements.
- Comparing products for a client or for a substitution request.
- Rewriting a proprietary clause as a performance clause (or the reverse).

## Input

- **Jurisdiction and specification system.** Ask if not stated. See [references/systems.md](references/systems.md) for the common ones. Don't default to one country.
- The element or work section (e.g. external rainscreen cladding, internal timber doors, resin floor).
- Design intent: appearance, performance needs, location in the building, exposure.
- Proprietary, performance-based, or descriptive? Any client-mandated products?
- Sources: manufacturer datasheets, EPDs, test certificates, the practice's master spec, if available.

## Process

1. **Fix the system and the section.** Name the section reference in the practice's system (e.g. a Uniclass Ss code, a MasterFormat number). If you are not sure of a code, write "[section ref: confirm in master]". Never guess a code number.
2. **Write the design intent first,** in two or three lines: what this element must do and look like.
3. **Draft the clause** in the system's structure (see references). Typical parts: description/scope, performance requirements, products/materials, execution/workmanship, completion, submittals/samples/mock-ups.
4. **Mark every value and every standard.** A performance value (U-value, slip rating, fire classification, acoustic rating, durability class) or a standard number (EN, ISO, ASTM, BS, DIN) is written only if supplied in a source, with the source named. Otherwise write the requirement type and a placeholder: "Reaction to fire classification: [to confirm with fire engineer, against EN 13501-1 or local equivalent]".
5. **Products:** name a product only if the architect named it or you are working from its datasheet. When asked for alternatives, use web search if available and give the manufacturer URL for each. Otherwise say you can't verify products and give the selection criteria instead.
6. **Flag coordination.** List what the clause depends on: structural fixing design, fire strategy, acoustic report, M&E. Those are other people's decisions.

## Product comparison

Compare on the criteria that decide the choice for this project, not a generic list. Every cell is either sourced (datasheet, EPD, URL) or marked "not stated" or "to confirm". Include a "basis" column for cost or carbon figures (source and date), or leave them out.

## Domain knowledge

- **Performance vs proprietary.** Performance clauses keep competition open and push design responsibility to the contractor for that element. Say this so the architect chooses deliberately. Public procurement in many jurisdictions requires "or equivalent" wording with named products.
- **"Or equivalent"** needs the criteria for equivalence stated, or it is unenforceable in practice.
- **Samples, mock-ups, and benchmarks** belong in the clause for anything where appearance matters: stone, brick, timber finish, concrete finish.
- **Do not copy manufacturer marketing language** into a clause. "Premium", "high-performance", "eco" mean nothing in a contract.

## Output format

```
## Specification: [section title]
**System:** [NBS / MasterFormat / other] · **Section ref:** [code or "confirm in master"] · **Jurisdiction:** [ ]

**Design intent:** [2-3 lines]

### [Clause number / title]
- **Description:** ...
- **Performance:** [requirement, value only if sourced: (source)] / [to confirm against datasheet]
- **Products:** [named product + manufacturer URL] or "Performance-based: no product named"
- **Execution:** ...
- **Submittals / samples:** ...

**Depends on:** [fire strategy, structural design, acoustic report, ...]
**To confirm:** [every unsourced value and standard, in one list]

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't invent product names, product ranges, performance values, test standards, or section codes. Unsourced means "to confirm".
- Don't state that a product or system "complies with" or "meets" a regulation. "Manufacturer states [value] (datasheet, [date])" is the most you write.
- Don't make fire, structural, or acoustic performance decisions. Specify the requirement category and route the value to the responsible consultant.
- Don't paste a whole master specification. Write the clauses asked for.
