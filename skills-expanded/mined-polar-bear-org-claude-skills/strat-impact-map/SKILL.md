---
name: strat-impact-map
description: Builds an impact map from one strategy goal down to the actors, the behaviour changes marked seen or assumed, and the roadmap items that support them, with a cut-or-justify list and the first impact to work on. Use for "run strat-impact-map", "impact map", "impact mapping", "whose behaviour does this item change", "our roadmap is a feature list", "tie the roadmap to the strategy goal", "which roadmap items have no reason to exist", "audit the roadmap against the goal", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Impact Map

## When To Use
The roadmap is a feature list and nobody can say whose behaviour each item changes. The strategy is chosen, the goal has a measure, and the planned work was mostly written before either existed. Use this to answer one question: for the goal to move, who has to act differently, and which of our planned items help them do it?

## When Not To Use
The map tests whether an item has a reason to exist; it does not order or schedule anything, so for that run Product Roadmap (Now, Next, Later). If you start from interview notes and no roadmap yet, use Opportunity Solution Tree. With two goals, run it twice.

## Inputs
- The goal from the chosen strategy and how it is measured (the north star or one of its inputs works)
- The current roadmap, feature list or backlog headlines, pasted as they are
- What you know about who uses, buys, supports or blocks the product, with where each fact comes from
If you have none of this, I start from the goal alone and mark the output as a first draft, with every impact marked assumed.

## Approach
This is Impact Mapping as Gojko Adzic sets it out on impactmapping.org (https://www.impactmapping.org/): four levels in a fixed order, why, who, how and what. The chain reads one way only. A deliverable earns its place by supporting a change in what somebody does, and that change has to count toward the goal. The failure it prevents is the quarter where every item ships on time and the measure does not move, because nothing on the list changed anyone's behaviour. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: which one goal this map serves, how that goal is measured (you set the measure and any target), and who picks the first impact and by when.
2. Write the why: one goal with its measure at the top. One map serves one goal. If the list seems to serve a second goal, I say so and park those items for a second map instead of bending the first.
3. List the who: actors whose behaviour can help or hinder the goal, such as users, buyers, support and internal teams. Roles or groups only. An actor who can block the goal belongs here as much as one who helps.
4. Write the how: each impact is a change in an actor's behaviour, never a feature. Example of the form: "[actor] does [action] in [period] without [current workaround]". Each impact is marked "seen in data or interviews", with the source, or "assumed".
5. Place the what: every item from the pasted roadmap goes under the impact it supports. An item that hangs from no impact goes to "cut or justify", with the question its owner must answer. I do not invent an impact to rescue an item.
6. Prioritise from the goal down: propose one actor and one impact to work on first, with the reason, before any deliverable is ranked. Note impacts with no deliverable under them, since those are gaps in the roadmap.

## Output Format
```markdown
# Impact Map
## Goal (why)
[Goal from the strategy]. Measure: [measure], target [value set by the owner, or "not set"]. Source: [where the measure is read].
## Map
| Actor (who) | Impact (how their behaviour changes) | Seen or assumed | Source | Deliverables (what) |
|---|---|---|---|---|
| [role or group] | [behaviour change] | [seen / assumed] | [data pull, interview round, or none] | [roadmap item], [roadmap item] |
## Cut or justify
| Roadmap item | Why it hangs from no impact | Question for its owner |
|---|---|---|
| [item] | [no actor or behaviour named] | [whose behaviour does this change, and how would we see it?] |
## Impacts with no deliverable
- [actor, impact]: [nothing planned supports it]
## First impact to work on
[Actor and impact], because [reason]. Evidence status: [seen / assumed, and what would confirm it].
## Decision
[Role of the roadmap owner] picks the first impact and rules on each cut-or-justify item by [date].
```

## Done When
- One goal with a measure you set sits at the top
- Every impact reads as something an actor does, and carries "seen" with a source or "assumed"
- Every pasted roadmap item is either under an impact or on the cut-or-justify list
- One actor and one impact are proposed first, with the reason, before any deliverable is ranked

## Quality Bar
- Actors are roles or groups, never named individuals; internal teams are mapped, never assessed
- No target, baseline or customer finding is invented; unknowns stay as [placeholders]
- An assumed impact is never promoted to seen because it sounds likely
- The cut-or-justify list is a set of questions, not a verdict; the owner rules on it
- Impacts are behaviour changes seen with real users or marked assumed; a named person picks the first impact.

## Next
Run strat-product-roadmap (Product Roadmap (Now, Next, Later)) to order the surviving items and place them by horizon.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
