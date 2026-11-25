---
name: game-theory-negotiation
version: 1.1.2
description: >
  Prepare and run negotiations, procurement auctions, and incentive design.
  Use for BATNA/ZOPA, walk-away prices, opening offers, concession plans,
  fairness, bonus or profit-share structures, and game-theory diagrams of
  players and payoffs. Excludes game-theory homework unrelated to bargaining,
  auctions, or contracting.
---

# Game-theoretic negotiation and auctions

This skill turns game theory into a negotiation workflow: set the numbers, choose the tactic, run the concession plan, defend the close, and check the result. Use it when a negotiation needs structure instead of vibes.

Synthesizes standard negotiation-analysis and game-theory literature plus personal research. Best-effort per-term upstream credits (Fisher & Ury, Raiffa, Simon, Vickrey, Subramanian's negotiauction, and others) are in `README.md`.

---

## Prime directive: aim above your floor, never at it

Two findings anchor everything else in this skill:

1. **Your reservation price is a floor, never a target.** It is the worst outcome you would still accept. The other side would love to push you there. Keep it in the back of your mind as a hard boundary, not as a place to bargain.

2. **Focus on the Ambitious Target (AT), not the floor.** Negotiators who aim at an ambitious but plausible target tend to do better than negotiators who stare at their walk-away point. You usually end up near what you aim at.

Everything below keeps you in the useful zone between the Ambitious Target and the floor. The goal is simple: claim more of the surplus without blowing up the deal.

Read `references/core-concepts.md` before any non-trivial negotiation prep. It defines the numbers (reservation price, BATNA, ZOPA, surplus, aspiration levels) the rest of the skill manipulates.

---

## Who this is for

The playbook is field-neutral: the same five numbers and the same moves drive a salary talk, a security-control dispute, an auction design, an M&A earnout, or a vendor renewal. `references/domains.md` translates the vocabulary for specific roles — salary and compensation, security compliance / conflict management, quants and mechanism designers, M&A consultants, and business managers and leaders. If the user clearly fits one, read that section first for the vocabulary bridge and a worked example, then come back here.

## How to use this skill

1. **Frame the situation.** Is it distributive (one issue, fixed pie) or integrative (several issues, trade-offs possible)? One-shot or repeated? Bilateral negotiation, or a tender / negotiauction? Ask only if the answer changes the move.
2. **Set the numbers** (`references/core-concepts.md`). Establish your reservation price, sharpen your BATNA, estimate the ZOPA, and lay out the aspiration ladder: BPO, Ambitious Target, Target, Reservation Level, No-Deal Outcome. If the BATNA is uncertain, model it with a three- or four-point estimate (`references/frameworks.md`).
3. **Plan the bidding** (`references/tactics.md`). Choose **degressive bidding** by default; place the target price in the *middle* of the bargaining range, pick a plausible maximum opening position, and pre-compute the halving concession schedule plus the closing in-kind sweetener. Reject Boulwarism unless you understand exactly why you're using a take-it-or-leave-it offer.
4. **Hold the line with tactics** (`references/tactics.md`). Always answer with a counter-offer. Use a reversible no to buy time and escape the red zone. Keep higher authority in reserve for face-saving and rule enforcement.
5. **Value non-price terms** with a virtual price list (`references/frameworks.md`) so you can trade across issues and convert any concession into money.
6. **Defend the close.** Watch the window between handshake and signature for nibbles and holdup; apply price-tagging, counter-nibble, or the threat to reopen everything (`references/tactics.md`, `references/frameworks.md`).
7. **Verify the outcome.** Confirm it is genuinely **win-win**, not merely Pareto-tolerable; check the surplus split against your aspiration levels; for fairness disputes apply an explicit criterion such as Cut-and-Choose (`references/frameworks.md`).
8. **For auctions, procurement, and incentive design**, go to `references/frameworks.md` (negotiauctions, incentive-compatible mechanisms, incentivization / profit-share).
9. **For diagrams**, use `references/drawio-concepts.md`. Pick the diagram from the work product: player/incentive map for stakeholder alignment, information-asymmetry map when truthfulness is uncertain, move tree for sequences, payoff matrix for choices, and deal-architecture map for multi-issue trades.

Use the templates in `assets/` to capture the prep and run a live session.

When another skill has already analyzed the same situation, carry forward its context packet instead of starting over: actors, claims, evidence, assumptions, scenarios, constraints, options, payoffs, and open questions. Keep the same names for actors and claims so diagrams from different skills can be compared side by side.

For a new negotiator, do not start with tactics. Walk them through `references/prep-walkthrough.md` first. The output should be a ready-room brief: what they want, what they can accept, what they must verify, what they will open with, what they will concede, what they will say no to, and what diagram they should keep open during the conversation.

---

## Capability map

The course's capabilities sort into four layers. Each row points to where it lives.

### A. Core action capabilities (live tactical moves) -- `references/tactics.md`
- **Counter-offer** -- never just reject; propose a new number or term and flip yourself back into the proposer role.
- **Reversible no** -- reject one proposal without killing the deal, then use the pause to build a better counter.
- **Nibble defense** -- price-tag the late ask, counter-nibble, or threaten to reopen the whole negotiation.
- **Higher authority** -- bind yourself to an absent approver so you can buy time, save face, and enforce rules.

### B. Frameworks and analytical tools -- `references/frameworks.md`
- **Degressive bidding vs Boulwarism** -- use shrinking concessions by default; avoid rigid first-and-final offers unless the breakdown risk is acceptable.
- **Virtual price list** -- assign money values to non-price terms so you can trade across issues.
- **Scenario analysis** -- separate risk, uncertainty, and surprises instead of pretending one forecast covers everything.
- **Three-point / four-point estimates** -- model an uncertain BATNA instead of guessing one number.

### C. Strategic mindsets -- `references/core-concepts.md`
- **Target focus** -- anchor on the Ambitious Target, not the floor.
- **Risk-aversion modeling** -- discount uncertain outcomes by the decision-maker's risk attitude.
- **Win-win verification vs Pareto efficiency** -- a deal both sides accept is not automatically jointly optimal.

### D. Operational applications -- `references/frameworks.md`
- **Holdup protection** -- mutual exposure, automated triggers, milestones, and self-binding contracts.
- **Fairness-criterion negotiation** -- pick the criterion explicitly: contribution, productivity, voting, or Cut-and-Choose.
- **Incentive-compatible mechanisms and negotiauctions** -- Vickrey-style truthful auctions, strategic bidding, and rule-bound procurement.
- **Incentive design** -- profit-share and bonus sizing, with attention to the right variable component.

### E. Cross-skill and draw.io work -- `references/drawio-concepts.md`

This skill is one node in a four-skill analysis loop that shares a common context packet (actors, claims, evidence, assumptions, scenarios, options, payoffs, constraints, open questions — see `references/drawio-concepts.md`). Keep actor and claim names stable so diagrams from different skills line up. The handoffs run both ways: a negotiation surfaces a claim to test or a future to map; an investigation or foresight exercise surfaces a decision to negotiate.

- **Game-theory diagram selection** -- choose a player map, information map, move tree, payoff matrix, or deal map based on the decision. All render through the draw.io MCP (Mermaid for trees and simple maps, XML for matrices and multi-panel layouts).
- **Foresight handoff** (`strategic-foresight-viz`) -- import scenarios, weak signals, and external uncertainties before pricing risk or estimating BATNA; build one payoff matrix per future and pick the robust strategy. Send external drivers back the other way for scenario development.
- **Investigation handoff** (`investigation-theory`) -- import claims, evidence, gaps, and deception risks before trusting stated preferences or constraints; send disputed incentives and unverifiable promises out to be tested.
- **Hypothesis-testing handoff** (`intana-viz`) -- route contested assumptions through ACH, Red Teaming, Key Assumptions Check, or Pre-Mortem, and stakeholder maps for many-player situations; bring the verified picture back to price the options.

---

## When the negotiator is stuck

- **You keep landing near your floor.** You are fixating on the reservation price. Re-anchor on the Ambitious Target and use a Tactical No to climb out of the red zone.
- **They opened first and anchored high/low.** Don't argue the anchor. Make a counter-offer that re-anchors from your side; whoever issues the last credible ultimatum holds the power.
- **One non-price demand is blocking a money deal.** Put it on the virtual price list and trade it; isolate it from the agreed core.
- **Your BATNA feels weak.** Invest in improving it before conceding. Every better outside option shrinks the zone in your favor. If it's uncertain, estimate it with three or four points rather than guessing a single number.
- **They're nibbling at the altar.** Price-tag it, counter-nibble, or threaten to reopen everything. Nibblers fear a full reopening.
- **The "fair" split is contested.** Stop arguing fairness in the abstract; agree on a *criterion* first (Cut-and-Choose is self-enforcing for two parties).

---

## Reference index

- `references/core-concepts.md` -- reservation price, BATNA, ZOPA, surplus, bid-ask gap, aspiration levels, target focus, risk aversion, win-win vs Pareto, strategic vs incentive-compatible bidding.
- `references/tactics.md` -- counter-offer, reversible no, nibble defense, higher authority, and the degressive-bidding algorithm vs Boulwarism.
- `references/frameworks.md` -- virtual price list, scenario analysis, three-/four-point estimates, holdup protection, fairness criteria, negotiauctions, incentive-compatible mechanisms, incentive design.
- `references/drawio-concepts.md` -- game-theory diagram types and cross-skill handoff rules for draw.io work.
- `references/domains.md` -- role-specific entry points (salary, security compliance, quants, M&A, business leaders) with vocabulary bridges and worked examples.
- `references/prep-walkthrough.md` -- guided ready-room workflow for a new negotiator.
- `references/playbooks.md` -- worked playbooks for buy/sell, procurement auction, incentive design, and holdup defense.
- `assets/negotiation-prep-template.md` -- pre-negotiation worksheet: numbers, ladder, concession schedule.
- `assets/concession-plan-template.md` -- degressive concession schedule worksheet.
- `assets/virtual-price-list-template.md` -- multi-issue valuation grid.
- `evals/evals.json` -- regression scenarios.
