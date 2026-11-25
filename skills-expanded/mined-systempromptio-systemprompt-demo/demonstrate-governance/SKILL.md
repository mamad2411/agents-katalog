---
name: "demonstrate-governance"
description: "Exercise the four-stage governance pipeline - scope check, secret scan, blocklist, rate limit - through the systemprompt MCP hub, then read back the audited decisions"
---

# Demonstrate Governance

Explain the four-stage governance pipeline and **prove two of its stages live**,
using only the `systemprompt` MCP documentation hub. Every tool call in this
session — including each one below — passes through the same synchronous check
before it executes.

## When to Use

Use this to show that governance is enforcement rather than description: that a
call is stopped *before* it runs, that the reason is specific, and that the
decision is written down.

## The pipeline

Four policies run in order on every tool call, configured in
`services/governance/config.yaml`:

| Stage | Policy id | What it blocks |
|-------|-----------|----------------|
| Scope check | `scope_check` | A non-admin caller reaching for an admin-only tool prefix (`mcp__admin__*`) |
| Secret scan | `secret_scan` | Plaintext credentials in any tool input (35+ patterns), any scope |
| Blocklist | `tool_blocklist` | Tool names matching a blocked pattern, for non-admin scope |
| Rate limit | `rate_limit` | More than 300 calls per 60s for one identity |

Scope comes from the caller's live database roles, not from anything the agent
says about itself. `admin` callers are exempt from `scope_check` and
`tool_blocklist` — but **this terminal caps every caller at `user` scope**,
whatever their roles say, so those exemptions never apply here. It is a
sandboxed demo surface, not an admin console; an operator signed in as admin
sees exactly the enforcement a visitor sees. `secret_scan` and `rate_limit`
apply to every identity regardless.

Evaluation does not stop recording at the first failure — stages after a deny
are recorded as skipped, so the audit row keeps the whole trace rather than a
single line of it.

**Be honest about what is demonstrable here.** In this terminal the agent's tool
allowlist holds only the hub's own tools, so there is no admin-prefixed tool to
reach for (`scope_check`), and no plausible way to make 300 calls in a minute
(`rate_limit`). Those two are explained, not performed. The two below are real.

## How to Use

### 1. The allowed path

A normal hub call clears all four stages and records an `allow`:

```
mcp__systemprompt__search_docs {"query": "governance pipeline"}
```

Point out the approval card and the audited allow. Governance is not only about
refusal — the same spine records what was permitted, by whom, and at what cost.

### 2. A live `secret_scan` deny

`secret_scan` reads the whole tool input. Call `search_docs` with a query
carrying a credential-shaped string and the call is denied before it executes,
for any caller, admin included. Use this string exactly:

```
mcp__systemprompt__search_docs {"query": "SPDEMOKEY-0000000000000000"}
```

Expect a deny naming `policy: secret_scan` and the pattern it matched,
`Demo Credential`. Nothing was searched — the tool never ran.

Worth saying out loud: `SPDEMOKEY-` is not a vendor prefix. It is an operator
pattern this deployment added under `policies[id=secret_scan].extra_patterns`
in `services/governance/config.yaml`, alongside the 35+ built-in ones (AWS,
GitHub, Stripe, Slack…). So this step demonstrates two things — that the scan
stops a call before it runs, and that the pattern set is the operator's to
extend.

> **Do not point this step at a real vendor prefix, and do not ask the model to
> invent one.** The constraint is not that this file avoids credential-shaped
> text — it is that *nothing the skill causes to exist* may match the gateway's
> built-in patterns. A tool call's arguments stay in the transcript, and the
> assistant's turns are re-scanned along with everything else, so a real prefix
> in a denied call keeps matching after the deny: the session 403s on every
> later turn and looks exactly like a broken terminal. Both halves of the fix
> matter — the demo prefix is invisible to the gateway scanner, *and* that
> scanner now judges only the newest user turn. Either one alone would leave
> this fragile. Tests pin both; see `handlers/pi/skills.rs`.

### 3. A live `tool_blocklist` deny

The hub exposes `fetch_remote_docs`, which would reach the public internet for
upstream documentation. This deployment does not permit outbound egress, so
`fetch_remote` is a blocked pattern. Attempt it:

```
mcp__systemprompt__fetch_remote_docs {"path": "/docs/governance"}
```

Expect a deny naming `policy: tool_blocklist`, whoever you are signed in as —
the terminal's `user` scope ceiling means the admin exemption cannot apply here.
Two more things are worth saying out loud. The deny happened at the policy gate,
before any network call was attempted. And even with the policy absent, this
session's sandbox permits outbound TCP to exactly one port, so the connection
would have failed anyway — defence in depth, with the policy layer supplying the
legible reason.

### 4. Read the decisions back

```
mcp__systemprompt__governance_stats {}
```

Every allow and every deny above is in the result, each with its policy and
reason. Walk them in order and tie each row to the call that produced it.

## Typical workflow

1. Allowed hub call (step 1) — it runs, and is recorded.
2. Credential-shaped query (step 2) — denied at `secret_scan`.
3. Remote fetch (step 3) — denied at `tool_blocklist`.
4. `governance_stats` (step 4) — all three, audited, with reasons.

Keep that order, and make step 4 the last thing you do. Reading the decisions
back is what turns the two denials into evidence, and ending there means the
demonstration is complete at the moment the session is quietest.

## Related

- `demonstrate_tool_rejection` — the rejection path on its own, in more detail.
- `analyse_governance_stats` — spend and latency alongside the verdicts.
