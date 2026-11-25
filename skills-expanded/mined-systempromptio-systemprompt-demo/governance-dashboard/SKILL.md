# Governance Dashboard

Turn the session's audit spine into something you can look at: a dashboard, a
chart, and a decision table, all rendered server-side from the same rows the
governance pipeline wrote. This is the "useful, not just refusing things" demo —
the spine is a data source, and the artifact shelf is its front end.

## When to Use

Use this when someone asks to *see* activity rather than read about it — "show
me a dashboard", "visualise the spend", "what's happening in this session?".
The artifacts are built from this session's own spine, so they get better as
the session gets busier. On a fresh session they render an illustrative row
that says so; offer to run a demonstration first if the visitor wants a fuller
picture.

## How to Use

### 1. Render the three spine-backed artifacts

In a **single turn**, issue all four calls as one parallel batch:

```
mcp__systemprompt__render_artifact {"artifact_type": "dashboard"}
mcp__systemprompt__render_artifact {"artifact_type": "chart"}
mcp__systemprompt__render_artifact {"artifact_type": "table"}
mcp__systemprompt__governance_stats {}
```

- **dashboard** — verdict totals, provider spend, and the four pipeline stages
  as status items.
- **chart** — allowed and denied counts per policy stage.
- **table** — the individual decisions: when, which tool, allow or deny, and
  the deciding policy.

Each call is itself governed — scope check, secret scan, blocklist, rate
limit — and lands its own row on the spine, so building the dashboard adds to
the data it displays. Say that out loud; it is the point.

### 2. Narrate against the numbers

Use the `governance_stats` result to caption what the artifacts show: total
spend, the allow/deny split, which policies fired. Every number you state must
come from the tool result in this conversation — never from the count of calls
you made or from this file. If a render was refused, name it, quote the reason
verbatim, and treat the denial as part of the dashboard's story rather than a
failure to route around.

### 3. Point at the shelf

Close by directing the visitor to the artifact shelf chip in the terminal
header and each tool row's **view result** button — the preview is the same
server-side render an MCP host would show, not a second renderer.

Then offer `audit_this_session` as the receipt: same spine, itemised.

## Related

- `demonstrate_artifacts` — every artifact type, including the curated ones.
- `analyse_governance_stats` — the written analysis of the same data.
- `audit_this_session` — the closing-beat receipt.
