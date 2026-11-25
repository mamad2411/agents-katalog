# Audit This Session

Close the loop: show the visitor the audit trail *their own conversation* just
produced. Not a description of auditing — the actual rows: what this session
cost, which tools fired, and the policy verdict attached to every one of them.

This is the finale skill. Whatever demonstration just ran, this is the receipt.

## When to Use

Use this as the closing beat of any demonstration, or whenever someone asks
"what did this just cost?", "what did the agent actually do?", or "how would I
know?". It is at its best when the session already holds some activity —
ideally at least one denial. On a fresh session, say so and offer to run
`demonstrate_governance` first to generate something worth auditing.

## How to Use

### 1. Land the rendered ledger

In a single turn, issue both calls as one parallel batch:

```
mcp__systemprompt__render_artifact {"artifact_type": "table"}
mcp__systemprompt__governance_stats {}
```

The table artifact is the session's recent governance decisions, rendered
server-side from the same spine `governance_stats` reads — when, which tool,
allow or deny, and the deciding policy. Point the visitor at the artifact shelf
and the tool row's **view result** button.

### 2. Quote the summary line before you interpret it

`governance_stats` returns a one-line summary of the form:

```
<allowed> allowed, <denied> denied across <N> decision(s);
<N> provider request(s), <N> tokens in / <N> out, $<cost>
```

Reproduce that line verbatim first, then write the receipt around it. Do not
restate spend in your own words before quoting it, and do not reconcile it
against anything — if your reading disagrees with the summary, the summary is
right and your reading is wrong.

**The table artifact records decisions, not spend.** It has no token or cost
column, so a table full of tool rows and no model rows says nothing whatsoever
about whether the session reached a provider. Concluding "no LLM calls" or
"$0.00" from the table — while the summary line reports requests and cost — is
the one failure this step exists to prevent. Spend comes from the summary line
and from nowhere else.

### 3. Itemise the bill

From the `governance_stats` result, write the receipt. Keep it short and
concrete, in this order:

- **Spend** — each model reached, input/output tokens, and cost. Say the number.
  Cost here is recorded per request against one identity at the moment of the
  call, not estimated later from a log — that is what makes it chargeable.
- **Verdicts** — every allow and deny with its policy. Quote denial reasons
  verbatim; a session with a deny in it is the stronger evidence.
- **Tool fires** — what ran versus what was attempted. The gap is the
  enforcement, made countable.

Every figure you state must come from the tool result in this conversation.
A zero is only reportable when the summary line itself says zero. If the session
is genuinely empty, an empty receipt is the honest report.

### 4. Say what the receipt proves

One closing paragraph: every inference and every tool call in this session is
attributable to one identity, joined by a session id, with the policy decision
and the cost recorded beside it. The visitor is not being asked to trust that —
they are looking at their own rows.

## Related

- `demonstrate_governance` — generate verdicts worth auditing.
- `analyse_governance_stats` — the longer-form analysis of the same spine.
- `governance_dashboard` — the same data as a visual dashboard.
