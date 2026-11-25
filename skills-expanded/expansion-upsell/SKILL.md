---
name: expansion-upsell
description: "Grow an existing account — map whitespace, read expansion-readiness signals, run the land-and-expand play, and time the ask to value realization. Use when planning how to expand, upsell, or cross-sell into a current customer. Triggers on: expansion, upsell, grow this account, cross-sell, land and expand."
---

# Expansion & Upsell

## Purpose
Turn a happy (or quiet) existing account into the next deal: find what you
haven't sold yet, judge whether they're ready to buy more, attach the ask to a
moment of realized value, and produce a concrete expansion plan you can run.

## Inputs
- The account: current products/seats/teams sold, contract value, renewal date
- Usage and adoption signals (who's active, what's stuck, where they hit a limit)
- Sentiment and relationship health (champions, detractors, exec exposure)
- What else you *could* sell (other products, more seats, adjacent teams, tiers)

## Method
1. **Whitespace map.** Lay the account out as a grid: products you sell (rows) ×
   teams/business units in the account (columns). Mark each cell sold / not-sold /
   in-trial. The blank cells are your whitespace. Add three more dimensions:
   - **Seats:** licensed vs active vs total addressable headcount in sold teams.
   - **Tier/edition:** are they on a plan below what their usage justifies?
   - **Adjacent teams:** units using none of your product but with the same pain.
   Rank whitespace by (fit × reachability) — closest to an existing champion and
   most similar to a use case already winning wins first.

2. **Read expansion-readiness signals.** Do not pitch more to an account that
   hasn't realized value on what it already bought. Score readiness on:
   - **Adoption depth:** active-seat ratio, frequency, breadth of features used.
     Healthy = a beachhead worth widening. Low = fix adoption *before* upselling.
   - **Value realized:** has the customer hit the outcome you sold? Quantify it
     (time saved, deals influenced, cost avoided) — that number funds the next buy.
   - **Sentiment trend:** is it improving or souring? Expand on a rising curve.
   - **Champion strength:** is there someone who will advocate internally for spend?
   Green on adoption + value + sentiment = expand now. Any red = remediate first.

3. **Watch for expansion triggers.** The ask lands when something *changed*:
   - **New executive / new budget owner** — re-sell the value, ride a fresh agenda.
   - **New initiative / project / funding round** — attach your product to their plan.
   - **Hitting a limit** — seats maxed, usage capped, a tier ceiling reached. The
     limit is the pitch: they're already feeling the constraint.
   - **A new use case surfacing in conversation** — a team or pain you don't yet serve.
   - **Renewal approaching** — natural commercial moment to repackage and grow.
   Map each live trigger to the whitespace cell it unlocks.

4. **Run the land-and-expand play.** Use the beachhead, don't restart cold:
   - **Prove** the win in the landed team — get the metric and the champion quote.
   - **Reference internally** — have the champion introduce you to the adjacent
     team/exec; warm intro beats outbound inside the same logo every time.
   - **Replicate** the proven use case into the new team (same playbook, new owner).
   - **Repackage** at renewal — consolidate seats/teams/products into a larger,
     simpler commercial that's cheaper per-unit and stickier.
   Each loop: land small → prove → expand to the next cell.

5. **Time the ask to value realization.** Plot the ask against the value curve:
   - Pre-value (still onboarding, no outcome yet): **do not ask** — secure adoption.
   - At first realized win: **ask for the adjacent team / next use case** — momentum.
   - Sustained value + a trigger: **ask for tier/seats/cross-sell** — strongest moment.
   - At renewal with proven value: **repackage and grow the whole contract.**
   The rule: the ask size should track the value already delivered, not your quota.

6. **Output the expansion plan.** One page, decision-ready:

```
Account: <name>   |  Current ARR: <$>  |  Renewal: <date>

Whitespace map (sold / not sold / trial):
              | Team A | Team B | Team C
  Product 1   |  sold  |   —    |  —
  Product 2   |   —    |  sold  | trial
  Seats: <licensed>/<active>/<addressable>   Tier: <current → target>

Readiness: adoption <H/M/L> · value realized <metric> · sentiment <trend> · champion <name>

Live trigger: <new exec / initiative / limit hit / use case / renewal>

Expansion targets (ranked):
  1. <product/seats/team> — why now: <trigger> — value hook: <metric> — owner: <champion>
  2. ...

Play: <land-and-expand step> — next ask: <what> to <whom> by <date>
Timing: <pre-value / first win / sustained / renewal>
```

**Both-sided rule:** an expansion plan names what *they* get (the outcome) before
what *you* get (the ARR). If the plan only grows your number, it won't close.

## Tool binding
This skill works from a verbal account description alone. It gets sharper when
connected to your stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, resolve the account and its
deals directly instead of asking the user to describe the account:
- `ontology_resolve("account", id, expand=["deals","sentiment","activity","contacts"])`
  — `deals` gives you what's sold and open across the logo (the whitespace
  baseline), `sentiment` and `activity` give the readiness trend, `contacts` give
  champions and the new-exec signal.
- For each won/expansion deal, `ontology_resolve("deal", id, expand=["outcome","closure_strategies","products"])`
  — `products` is what's actually sold (rows of the whitespace grid), `outcome`
  is the realized value that funds the next ask, `closure_strategies` shows the
  plays that won before so you can replicate them.
- `ontology_search` / `ontology_list` to find adjacent teams, contacts, or open
  deals in the account; `ontology_traverse` to walk account → deals → contacts
  relationships; `ontology_aggregate` to roll up seats/products across teams.
- `search_transcripts(...)` to surface a new use case, a hit limit, or a new
  initiative mentioned on a call — the trigger language straight from the buyer.
Prefer Doris's extracted outcomes, sentiment, and products over re-deriving them.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull current products, ARR, open opps, renewal
  date, and contacts to build the whitespace grid and write the expansion opp back.
- Product-usage / analytics MCP (Pendo, Amplitude, a usage warehouse) → adoption
  and seat-utilization signals for the readiness score and the "hit a limit" trigger.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) → mine calls for new use
  cases, new execs, and initiatives that signal expansion.

### With nothing connected
Ask the user to describe the account: what's sold today (products, seats, teams),
contract value and renewal date, who the champion is, how adoption and sentiment
feel, and anything that recently changed. From that, build the whitespace map
yourself, score readiness, identify the live trigger, and output the full
expansion plan + whitespace grid as a copy-paste block. No integration required.

## Works without Doris
Fully functional from a verbal account description — Doris only removes the
description step and supplies evidence-backed products, realized outcomes,
sentiment trends, and trigger language from real calls.

## Common mistakes
- Pitching more product before the customer has realized value on what they bought.
- Treating the whole logo as one account — missing team-by-team whitespace.
- Asking at the wrong moment (pre-value or away from any trigger).
- Restarting cold in an adjacent team instead of riding the champion's warm intro.
- An expansion plan that grows your ARR but never states the customer's outcome.
