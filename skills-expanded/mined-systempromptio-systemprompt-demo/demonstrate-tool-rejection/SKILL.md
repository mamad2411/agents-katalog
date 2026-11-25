---
name: "demonstrate-tool-rejection"
description: "Attempt a tool call the policy chain refuses - an egress tool matching the blocklist - and read back the audited denial, proving the call was stopped before it executed rather than after"
---

# Demonstrate Tool Rejection

Show a tool call being **refused**, and show that the refusal is a fact in the
audit log rather than a promise in a system prompt. A capability can sit in the
catalog, be visible to the model, be attempted in good faith — and still be
impossible to use, because policy decides, not the agent's judgement.

## When to Use

Use this when someone asks "what happens when the agent tries something it
shouldn't?", or wants to see a refusal that is enforced rather than asked for.

## What makes this different from a refusal

A model declining to do something is a preference; it can be argued with, and it
fails silently when the model is wrong. This is not that. The call is issued,
suspends at the gate, and is denied by a policy that never consults the model.
There is no prompt phrasing that gets past it.

The order is fixed and not negotiable: **policy first, human second.** When a
human approval card appears, it appears only for calls policy has already
cleared. A person can be more restrictive than policy, never less.

## How to Use

### 1. Establish the baseline

First show that the hub works and that the agent is not simply broken:

```
mcp__systemprompt__list_topics {}
```

This clears every stage and records an `allow`.

### 2. Attempt the refused tool

The hub exposes `fetch_remote_docs`, which would fetch documentation from the
public internet. This deployment does not permit outbound egress, so
`fetch_remote` is a blocked pattern in `tool_blocklist`. Attempt it anyway —
that is the point:

```
mcp__systemprompt__fetch_remote_docs {"path": "/docs/governance"}
```

Expected: a denial naming `policy: tool_blocklist`, with the pattern that
matched. Say clearly what did **not** happen: no DNS lookup, no TCP connection,
no request. The tool body never executed.

### 3. Show the second layer

The policy is not the only thing standing there. This session runs inside a
sandbox that permits outbound TCP to exactly one port — the gateway's — so the
fetch would have failed at the kernel even with the policy removed. Two
independent layers, either sufficient. The policy layer is the one that produces
a reason a human can read; the sandbox is the one that holds when configuration
is wrong.

### 4. Show that it was recorded

```
mcp__systemprompt__governance_stats {}
```

Find the denied row. It carries the tool name, the deciding policy, the reason,
and the identity it was attributed to. Contrast it with the `allow` from step 1:
both are in the same table, because a governance spine that only records
refusals cannot answer "what did this agent actually do?".

## What to say at the end

The refusal cost nothing to obtain and cannot be talked around. It is legible
after the fact — someone reviewing this session tomorrow can see what was
attempted, what stopped it, and why — and it applies to every caller, including
the ones nobody thought to test.

## Related

- `demonstrate_governance` — the full four-stage pipeline this rejection is one stage of.
- `analyse_governance_stats` — the audit surface, read on its own terms.
