---
name: "analyse-governance-stats"
description: "Read back this session's own governance spine - model spend, latency, policy verdicts and tool fires - through the systemprompt MCP hub, and explain what the numbers say about how the agent behaved"
---

# Analyse Governance Statistics

Read this session's own governance spine and explain it. Not a dashboard tour —
an analysis: what was called, what was permitted, what was refused, what it
cost, and what that pattern says about how the agent behaved.

## When to Use

Use this after some activity has happened in the session — a few skills run, a
few tools called, ideally at least one denial. Use it when someone asks "how do
you know what the agent did?" or "what does this actually cost?".

Running it against an empty session is a fine demonstration of an empty table
and nothing else. Do something first.

## How to Use

### 1. Pull the numbers

```
mcp__systemprompt__governance_stats {}
```

The result covers only the calling identity's own activity. There is no
deployment-wide view here and that is deliberate: authority in this terminal
comes from one embed token that resolves to exactly one user.

### 2. Read it in four passes

**Spend.** Which model was actually reached, how many input and output tokens,
what it cost. Note that cost is recorded per request against an identity, not
estimated afterwards from a log — that is what makes it chargeable.

**Latency.** How long calls took. Say where the time went: provider latency is
not the same as governance latency, and the policy chain is synchronous and
fast. If the numbers show that, say so; if they don't, say that instead.

**Verdicts.** Every allow and every deny, with the deciding policy and reason.
Group them: which policies fired, how often, and against what. A session with
denials is healthier evidence than one without — it shows the chain is live
rather than merely configured.

**Tool fires.** Which tools ran, and how that compares to which were attempted.
The gap between the two is the enforcement, made countable.

### 3. Say what it means

Close with the thing the numbers are evidence *for*: every inference and every
tool call in this session is attributable to one identity, joined by a session
id, with the policy decision that permitted it recorded alongside its cost. That
is the claim, and the table is how you check it rather than take it on trust.

Be specific and cite the figures. If something in the data is surprising or
doesn't support the story, say that plainly — an analysis that only ever
confirms the pitch is not an analysis.

## Cross-checking

The pane beside this terminal renders the same underlying data. If the numbers
here and there disagree, that is worth reporting, not smoothing over.

## Related

- `demonstrate_governance` — generate some verdicts to analyse.
- `demonstrate_tool_rejection` — generate a denial in particular.
