# Estimate My Bill

Help a visitor model what their team's AI usage would cost — grounded in the
per-request costs this deployment is recording right now, not a pricing page.
The pitch underneath: you can only estimate a bill you can itemise, and the
spine is what makes AI spend itemisable per identity.

## When to Use

Use this when someone asks about cost — "what would this cost my team?",
"how do you track AI spend?", "estimate my bill". It is a conversation, not a
one-shot: you will need a few facts from the visitor before any number is
honest.

## How to Use

### 1. Get a real unit cost first

Before asking the visitor anything, pull the session's own numbers:

```
mcp__systemprompt__governance_stats {}
```

Take the recorded cost and token counts per request from the result. These are
your only permitted unit costs. **Every figure in the estimate must trace to
this tool result — if the session has no recorded spend yet, say so, run a
quick governed call or two to generate some, and pull the stats again.** Do not
substitute remembered provider price lists; the demonstration is that recorded
cost beats quoted cost.

### 2. Ask for the shape of their usage

Three questions, no more:

- How many people (or agents) would be making calls?
- Roughly how many AI interactions per person per working day?
- Are those interactions more like short questions or long working sessions?

If the visitor does not know, offer sensible brackets and calculate all of
them — a range labelled as a range is honest; a single confident number is not.

### 3. Do the arithmetic in the open

Scale the observed per-request cost by their numbers to a monthly figure. Show
the working as a short markdown table: observed cost per request (cite it as
"recorded in this session"), requests per month, low/mid/high estimate. State
the caveat plainly: this extrapolates one session's workload shape, and their
mix of models and prompt sizes will move it.

### 4. Land the actual point

The number is the hook; the capability is the story. Close with: every unit in
that estimate came off an audit spine that records cost per request, per
identity, per session — which means a real deployment does not estimate its
bill at all. It reads it. Offer `audit_this_session` to show theirs, or
`governance_dashboard` to see spend visually.

## Related

- `audit_this_session` — this session's actual receipt.
- `analyse_governance_stats` — where the unit costs come from.
