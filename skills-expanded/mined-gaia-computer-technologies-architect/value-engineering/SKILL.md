---
name: value-engineering
description: Weigh value-engineering and cost-reduction options against cost saving (from the QS or contractor), quality, embodied carbon, programme, risk, maintenance and design intent, protect the elements the concept depends on, and draft a response to the QS or contractor. Produces a scored options table and a recommendation. Use when the architect wants to "respond to VE proposals", "find savings", "cut the cost plan", "what can we lose without losing the scheme", "review contractor alternatives" or "defend the design against cost cuts". Pairs with concept-parti (what must survive), material-palette (substitutions) and client-pushback for the conversation.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Value Engineering

Real value engineering means getting the same value for less money. Cutting the cost by cutting the value is a different thing, and the two get confused. This skill separates the options that save money without hurting the scheme from the ones that remove the idea, and puts that trade-off on paper before anyone signs it off.

## When to use

- A tender has come in over budget and the QS or contractor has proposed savings.
- The client asks for a cost reduction at any stage.
- A contractor proposes alternative products or details.
- Before a VE workshop, to go in with a position.

## Input

- **The options:** each proposed change, with the saving as stated by the QS or contractor (source and date). Savings come from them, not from you.
- **The cost plan or tender** and the target reduction.
- **The design intent:** the parti or concept narrative, and the brief's priorities. What must survive?
- **Specification and drawings** for the affected elements.
- **Constraints:** planning conditions tied to materials or details, performance targets (energy, acoustic, carbon), warranties, programme.

## Process

1. **Name the non-negotiables.** From the parti and brief, list the three to five elements the scheme depends on, and why. These are tested first.
2. **Log each option.** What changes, the stated saving, who proposed it, and what it affects (element, drawing, spec clause).
3. **Assess each option** on the criteria below. Use evidence where it exists; where an impact needs a specialist (structure, fire, acoustics, energy), mark it "specialist to confirm" instead of guessing.
4. **Check for knock-ons.** Planning conditions (a material approved by condition may need re-approval), building regulations and fire performance of substitutes, warranties, maintenance and lifecycle cost, programme effects of redesign, and carbon.
5. **Classify.** Accept (saves cost, keeps value). Accept with conditions (e.g. an equivalent product with confirmed performance). Resist (removes design intent or shifts cost to the client later). Needs information.
6. **Look for better savings.** Where an option removes intent, suggest an alternative that saves similar money elsewhere, if one exists. Simplifying a junction often beats downgrading a material.
7. **Draft the response** to the QS or contractor: decisions, conditions, and information requested.

## Assessment criteria

- **Saving:** as stated, with its source. Note whether it is net of redesign fees and programme cost.
- **Design intent:** effect on the non-negotiables (none / minor / major / removes).
- **Quality and durability:** lifespan, appearance, robustness.
- **Performance:** thermal, acoustic, fire (specialist to confirm), daylight.
- **Embodied carbon:** direction of change, with the basis if a figure is given.
- **Programme:** lead times, redesign time, resubmissions.
- **Risk:** planning (condition re-approval), regulatory, warranty, maintenance, reputation.

## Output format

```
## Value Engineering Review — [Project], [date]

**Target reduction:** [amount] | **Options reviewed:** [n] | **Stated savings total:** [amount, source]

### Non-negotiables (from the concept)
1. [element] — [why the scheme depends on it]

### Options
| # | Option | Stated saving (source) | Design intent | Quality | Performance | Carbon | Programme | Risk | Verdict |
|---|---|---|---|---|---|---|---|---|---|

### Knock-on checks
- [option]: [planning condition / regs / warranty / maintenance] → [action]

### Alternatives proposed
- Instead of [option], [alternative] — [estimated saving to be priced by QS]

### Summary
Accepted: [amount] | Conditional: [amount] | Resisted: [amount] | Gap to target: [amount]

### Draft response to QS / contractor
...

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't invent savings or cost figures. Savings are priced by the QS or contractor; you assess them.
- Don't approve product substitutions on fire, structural or regulatory performance. Specialist to confirm, with the datasheet.
- Don't defend every element. A response that resists everything gets ignored. Concede the real savings.
- Don't treat carbon as an afterthought. A cheaper option can carry a higher carbon cost, and the client should see it.
